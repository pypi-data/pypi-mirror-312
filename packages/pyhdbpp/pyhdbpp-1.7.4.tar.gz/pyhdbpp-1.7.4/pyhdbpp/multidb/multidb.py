    #!/usr/bin/env python3

import sys, re, traceback, time
from concurrent.futures import ThreadPoolExecutor
from ..abstract import AbstractReader
from ..utils import *
from ..reader import reader

# MultiDB schema is now tango-dependent
# future releases .yaml based to be implemented
try:
    import tango
except:
    tango = None

DEBUG = os.getenv('PYHDBPP_DEBUG') or '-v4' in sys.argv
if DEBUG:
    #logger.setLogLevel('DEBUG')
    logger.setLevel(logging.DEBUG)

# MultiDBReader

class MultiDBReader(AbstractReader):
    
    def __init__(self, config='',**kwargs):
        """
        config would be:
         - a list of dbnames
         - a comma-separated string
         - a {dbname:config} dictionary
        
        if just names are given, config for each db 
        will be read from tango db
        """
        logger.debug('MultiDBReader(config={},kwargs={})'.format(
            config, kwargs))
        self.readers = {}
        self.attributes = {}
        self.configs = {}
        self.aliases = {}
        self.alias_file = kwargs.get('alias_file','')
        self.threaded = kwargs.get('threaded',False)
        self.timeout_s = kwargs.get('timeout_s',0)
        self.tangodb = tango.Database()

        # List of schemas in string format
        if isinstance(config,str):# and ',' in config:
            config = [s.strip() for s in config.split(',')]
            props = [s for s in config if s.startswith('$')]
            # replace $PROP by PROP_VALUE
            for p in props:
                config.remove(p)
                p = p.strip('$')
                v = self.tangodb.get_property('HDB++',p)[p]
                v = [v] if isinstance(v,(str,bytes)) else v
                config.extend(v)
                logger.debug('MultiDBReader(...): {} = {}'.format(p,v))

        # List of schemas to load
        if isinstance(config,list):
            config = dict((s, load_config_from_tango(s,tangodb=self.tangodb))
                for s in config)
            
        # Dict of {schema:config}
        if isinstance(config,dict):
            for k,data in config.items():
                try:
                    if isinstance(data, str):
                        data = load_config_from_tango(v,tangodb=self.tangodb)
                    data['persistent'] = ''
                    self._trace('reader(',data,')')
                    rd = reader(apiclass=data['apiclass'],
                                config=data,)
                                #persistent=False)
                    ct = rd.get_connection()
                    if ct is not None:
                        self.configs[k] = data
                        self.readers[k] = rd
                except Exception as e:
                    msg = 'Unable to load %s schema' % k
                    logger.warning(msg)
                    logger.warning(traceback.format_exc())
                    #raise e

        if self.alias_file:
            try:
                logger.info('loading aliases from %s' % self.alias_file)
                with open(self.alias_file) as ff:
                    for t in ff.readlines()[1:]:
                        sep = '\t' if '\t' in t else ','
                        t = t.strip().lower().split(sep)
                        self.aliases[t[0]] = t[1]
            except:
                logger.warning('Unable to load %s' % self.alias_file)
                logger.warning(traceback.format_exc())

        if self.threaded:
            self.executor = ThreadPoolExecutor(max_workers=len(self.readers) or 1)
        else:
            self.executor = None
        
        self._trace('configs',self.readers.keys())
        self.get_attributes(load=True)
        
    def __del__(self):
        for k,rd in self.readers.items():
            del rd
        
    def _trace(self,*args,**kwargs):
        if DEBUG or kwargs.get('force',False):
            print(time2str(time.time()),'MultiDB',*args)


    def get_connection(self, attribute=None, schema=None, epoch=None):
        """
        Return the db connections used to acquire an attribute or schema
        at a given date(s). 
        
        :param: epoch can be a fixed time or an interval tuple (start, stop)
        
        If no schema or attribute is provided, returns all connections.
        The returned object will be implementation specific.
        
        
        """
        self._trace('get_connection', attribute, schema, epoch)
        try:
            if epoch is not None:
                epoch = [epoch] if not isSequence(epoch) else epoch
                epoch = [time2type(e,float) for e in epoch]

            if attribute and not schema:
                # this call gets the attribute name as it is archived
                attribute = self.get_attribute_name(attribute)
                schemas = {}
                
                for k in self.readers:
                    reader = self.readers[k]
                    attrs = self.attributes[k]
                    
                    # if reader.is_attribute_archived(attribute):
                    if attribute in attrs:
                        if epoch is not None:
                            rdc = reader.config
                            start = rdc.get('start_date',0) or 0
                            stop = rdc.get('stop_date',0) or 0
                            start = time2type(start,float)
                            stop = time2type(stop,float)
                            if start < 0:
                                start = now() + start
                            if stop < 0:
                                stop = now() + stop
                            elif not stop:
                                stop = END_OF_TIME

                            if not any(start <= e <= stop for e in epoch):
                                continue
                            
                            self._trace(k, start, epoch, stop)

                        schemas[k] = reader

                return schemas

            elif schema and attribute:
                return self.readers.get(schema).is_attribute_archived(attribute)
            
            elif schema:
                return self.readers.get(schema,None)
            
            else:
                return self.readers
            
        except Exception as e:
            msg = "get_connection({},{},{}):{}".format(attribute,schema,epoch,e)
            logger.error(msg)
            if not isinstance(e, ArchivingException):
                logger.error(traceback.format_exc())
            return {}


    def get_attributes(self, active=False, pattern='', load=False, timeout_s=0):
        """
        Queries the database for the current list of archived attributes.
        
        Once it has been queried, result is cached unless load=True is passed.
        
        arguments:
            active: True: only attributes currently archived
                    False: all attributes, even the one not archiving anymore
            regexp: '' :filter for attributes to retrieve
        """
        timeout_s = timeout_s or self.timeout_s

        if load or not self.attributes:

            if not self.threaded:
                for k,v in self.readers.items():
                    try:
                        self.attributes[k] = [a.lower() for a in v.get_attributes()]
                    except:
                        logger.warning('Unable to obtain {} attributes'.format(k))
                        self.attributes[k] = []

            else:
                methods = {k:db.get_attributes for k,db in self.readers.items()}
                data = TimedThreadPoolExecution(methods,executor=self.executor,default=[],workers=None)
                for k,v in data.items():
                    self.attributes[k] = [a.lower() for a in v]

                #with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.readers)) as ex:
                #ex = self.executor
                #results = {k: ex.submit(db.get_attributes)
                #        for k,db in self.readers.items()}
                #for k,v in results.items():
                #    self.attributes[k] = [a.lower() for a in v.result()]

                #     ex = self.executor
                #     results = {}
                #     t0 = time.time()
                #     for k,db in self.readers.items():
                #         results[k] = ex.submit(db.get_attributes)
                #     pending = list(self.readers.keys())
                #     while pending and time.time() < (t0 + timeout_s):
                #         for k,v in results.items():
                #             if v.done():
                #                 self.attributes[k] = [a.lower() for a in v.result()]
                #                 pending.remove(k)
                #         time.sleep(1e-3)
                #     if pending:
                #         for k in pending:
                #             self.attributes[k] = []
                #         print('multidb.get_attributes():Unable to get {} attributes in less than {} seconds'
                #               .format(pending,timeout_s))

        # self._trace('get_attributes',pattern)

        return sorted(set(a for k,v in self.attributes.items() for a in v
                    if not pattern or attr_match(pattern,a)))
    
    def get_attribute_name(self,attribute):
        """
        get attribute name as it is used in hdb++ (e.g. FQDN)
        """
        fqdn = attr_translate(attribute)
        brief = attr_translate(attribute, brief=True)
        pattern = "(%s$)|(%s$)" % (fqdn,brief)
        self._trace('get_attribute_name', attribute, pattern)
        attrs = self.get_attributes(pattern=pattern, load=False)
        if not attrs:
            alias = [v for a,v in self.aliases.items() if attr_match(pattern,a)]
            if alias:
                if alias[0] in self.aliases:
                    raise ArchivingException('RecursiveAlias:{}'.format(alias[0]))
                return self.get_attribute_name(alias[0])
        if fqdn in attrs:
            return fqdn
        elif len(attrs)>1:
            logger.warning('{} matches: {}'.format(attribute,attrs))
            raise ArchivingException('MultipleAttributeMatches:{}'.format(attrs))
        elif not len(attrs):
            raise ArchivingException('AttributeNotArchived:{}'.format(attribute))
        r =  attrs[0]
        self._trace('get_attribute_name', attribute, ':', r)
        return r

    def is_attribute_archived(self, attribute, *args, **kwargs):
        """
        Returns if an attribute has values in DB.

        arguments:
            attribute: fqdn for the attribute.
            active: if true, only check for active attributes,
                    otherwise check all.
            brief: returns bool instead of list of dbs
        """
        try:
            brief = kwargs.get('brief',False)
            if brief:
                return bool(self.get_attribute_name(attribute))
            else:
                return list(self.get_connection(attribute).keys())
        except Exception as e:
            logger.info('is_attribute_archived({}): {}'.format(
                attribute, e))
            return False if brief else []

    def get_closer_attributes_values(self, attributes, time_ref=None, n=1, columns=["data_time", "value_r"]):
        """
        Returns the n closer values inserted around time in DB for a list of attributes.
        If n is negative it will get the last inserted values, if positive it will get the next.

        arguments:
            attribute: fqdn for the attribute.
            columns: list of columns to query, default to data_time and value_r.
            time_ref: lower bound for data_time, if None should default to now()
            n: number of samples, default to 1.
        returns:
            [(epoch, r_value, w_value, quality, error_desc)]
        """
        logger.debug('multidb.get_closer_attributes_values({},{},{})'
                     .format(attributes,time_ref,n))
        result = {}
        if time_ref is None and n > 0:
            n = -n #defaults to last value
            
        for attribute in attributes:
            try:
                dbs = self.get_connection(attribute, epoch = time_ref)
                logger.debug('multidb: {} archived by {}'.format(attribute,dbs.keys()))
                if self.threaded:
                    methods = {k:db.get_closer_attributes_values for k,db in dbs.items()}
                    args = {k:(([attribute],),{'time_ref':time_ref,'n':n}) for k in methods}
                    values = TimedThreadPoolExecution(methods,args,self.executor,default=None,timeout_s=60)
                    values = {k:v[attribute] for k,v in values.items()}
                else:
                    values = {k:db.get_closer_attributes_values([attribute],time_ref=time_ref,n=n)[attribute]
                              for k,db in dbs.items()}

                result[attribute] = (lambda t:t and t[-1])(sorted(values.values()))
                
            except:
                traceback.print_exc()
                result[attribute] = None
                
        return result

    def get_attribute_values(self, attribute, \
            start_date, stop_date=None, \
            decimate = None, \
            **params):
        """
        Returns attribute values between start and stop dates.

        arguments:
            attribute: fqdn for the attribute.
            start_date: datetime, beginning of the period to query.
            stop_date: datetime, end of the period to query.
                       if None, now() is used.
            decimate: aggregation function to use in the form:
                      {'timedelta0':(MIN, MAX, ...)
                      , 'timedelta1':(AVG, COUNT, ...)
                      , ...}
                      if None, returns raw data.
        returns:
            [(epoch0, r_value, w_value, quality, error_desc),
            (epoch1, r_value, w_value, quality, error_desc),
            ... ]
        """
        attribute = self.get_attribute_name(attribute)
        if isinstance(start_date,(int,float)) and start_date < 0:
            start_date = now() + start_date
        stop_date = stop_date or now()
        
        #db = self.get_connection(attribute)
        #return db.get_attribute_values(attribute, start_date, stop_date, 
                                       #decimate, **params)
    
        dbs = self.get_connection(attribute, epoch = (start_date, stop_date))
        if not dbs.values():
            msg = 'AttributeNotArchivedAt({},{})'.format(attribute, time2str(stop_date))
            self._trace(msg, force=True)
            raise ArchivingException(msg)

        elif not self.threaded:
            db = list(dbs.values())[0]
            return db.get_attribute_values(attribute, start_date, stop_date,
                                       decimate, **params)
        else:
            #with concurrent.futures.ThreadPoolExecutor(max_workers=len(dbs)) as ex:
            ex = self.executor
            results = {k:
                    ex.submit(db.get_attribute_values,
                        attribute, start_date, stop_date, decimate, **params)
                    for k,db in dbs.items()}
            values = {k:results[k].result() for k,db in dbs.items()}

            ks = [k for k,v in values.items() if len(v)]
            self._trace({k:len(v) for k,v in values.items()})
            if len(ks)==1:
                return values[ks[0]]
            else:
                result = [] #sorted(t for k in ks for t in values[k])
                ts = sorted((values[k][0][0],k) for k in ks)
                for t,k in ts:
                    if not result or t > result[-1][0]:
                        result.extend(values[k])
                return result

    def get_attributes_values(self, attributes, \
            start_date, stop_date=None, \
            decimate = None, \
            correlate = False, \
            **params):
        """
        Returns attributes values between start and stop dates
        , using decimation or not, correlating the values or not.

        arguments:
            attributes: a list of the attributes' fqdn
            start_date: datetime, beginning of the period to query.
            stop_date: datetime, end of the period to query.
                       if None, now() is used.
            decimate: aggregation function to use in the form:
                      {'timedelta0':(MIN, MAX, ...)
                      , 'timedelta1':(AVG, COUNT, ...)
                      , ...}
                      if None, returns raw data.
            correlate: if True, data is generated so that
                       there is available data for each timestamp of
                       each attribute.
            columns: columns separated by commas
                    time, r_value, w_value, quality, error_desc                       

        returns:
            {'attr0':[(epoch0, r_value, w_value, quality, error_desc),
            (epoch1, r_value, w_value, quality, error_desc),
            ... ],
            'attr1':[(...),(...)]}
        """

        if not self.threaded:
            return dict((a, self.get_attribute_values(
                            a, start_date, stop_date, decimate))
                            for a in attributes
                        )
        else:
            results,data = {},{}
            with ThreadPoolExecutor(max_workers=len(attributes)) as ex:
                for a in attributes:
                    results[a] = ex.submit(
                        self.get_attribute_values, a,
                        start_date, stop_date, decimate=decimate,
                        correlate=correlate,
                        **params)

                for a in attributes:
                    data[a] = results[a].result()
                    self._trace(a,len(data[a]))
        
        return data
