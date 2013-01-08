from hk2.utils.version import Version

import imp
from hk2.extensions.interfaces import ExtensionPointDesc, EPParam

#===========================================================

class ExtensionPointDesc(object):
    def __init__(self):
        pass

#===========================================================

class ExtensionDesc(object):
    def __init__(self):
        pass

#===========================================================

class PluginDescParser(object):
    def __init__(self, config):
        self._validate(config)
        
        self._loadDescription(config)
        
        provides_sec = config.get('provides', [])
        if isinstance(provides_sec, dict):
            provides_sec = [provides_sec]
        self._loadProvides(provides_sec)
        
        extends_sec = config.get('extends', [])
        if isinstance(extends_sec, dict):
            extends_sec = [extends_sec]
        self._loadExtends(extends_sec)
    
    @staticmethod
    def parse(stream):
        loader = imp.new_module('hk2.extensions.loader')
        exec 'from hk2.extensions import *' in loader.__dict__
        exec stream.read() in loader.__dict__
        return PluginDescParser(loader.plugin)
    
    @staticmethod
    def parse_file(filename):
        with open(filename, 'r') as f:
            return PluginDescParser.parse(f)
    
    def _validate(self, config):
        root_els = ['name', 'version', 'author', 'extends', 'provides']
        unknown = [k for k in config if k not in root_els]
        
        if len(unknown):
            raise Exception('Unknown root parameters: %s' % (', '.join(unknown)))
    
    def _loadDescription(self, config):
        self.name = config.get('name')
        self.version = Version(config.get('version', '0.0.0'))
        self.author = config.get('author', None)
    
    def _loadProvides(self, prv):
        self.provides = []
        
        for ep in prv:
            epd = ExtensionPointDesc()
            epd.name = ep['point']
            epd.interface = ep['interface']
            epd.params = self._loadProvidesParams(ep.get('params', {}))
            
            self.provides.append(epd)
    
    def _loadProvidesParams(self, params):
        for _, prop in params.iteritems():
            assert prop in EPParam.values
        
        return params
    
    def _loadExtends(self, exts):
        self.extends = []
        
        for ext in exts:
            etd = ExtensionPointDesc()
            etd.name = ext['point']
            etd.clazz = ext['class']
            etd.params = ext.get('params', {})
            
            self.extends.append(etd)
    
    