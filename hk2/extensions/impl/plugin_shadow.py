from hk2.extensions import IPluginShadow

#===========================================================

class PluginShadow(IPluginShadow):
    def __init__(self):
        self._name = None
        self._path = None
        self._desc = None
        self._author = None
        self._version = None
        self._extensionPoints = []
        self._extensions = []
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def description(self):
        return self._desc
    
    def author(self):
        return self._author
    
    def version(self):
        return self._version
    
    def extensionPoints(self):
        return self._extensionPoints
    
    def getExtensionPoint(self, shortName):
        for ep in self._extensionPoints:
            if ep.name() == shortName:
                return ep
        return None
    
    def extensions(self):
        return self._extensions
    
    '''
    def _getType(self, mod, cls):
        m = self._mod_cache.get(mod, None)
        if not m:
            m = mod = __import__(mod, {}, {}, ['*'])
            self._mod_cache[mod] = m
            pl_t = self._findSubclass(PluginBase, m)
            if pl_t:
                pl = pl_t()
                pl.Init(self._manager, self._manager.ServiceRegistry(), self)
        return m.__dict__[cls]

    def _findSubclass(self, base, mod):
        mn = mod.__name__
        sc = base.__subclasses__()
        for c in sc:
            if c.__module__ == mn:
                return c
        return None'''
