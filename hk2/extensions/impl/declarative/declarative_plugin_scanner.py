from hk2.extensions.interfaces import IPluginScanner, PluginBase

from hk2.extensions.impl.declarative.plugin_desc_parser import PluginDescParser
from hk2.utils.pathutil import listdir_recursive

import os, sys
import logging
log = logging.getLogger('hk2.extensions')

#===========================================================

class DeclarativePluginScanner(IPluginScanner):
    PLUGIN_DESC_FILE = '__plugin__.py'
    
    def __init__(self):
        self.plugin_dirs = []
        self.loadedPlugins = set()
        self.resolvedModules = set()
    
    def addDir(self, path, recursive=False):
        self.plugin_dirs.append((os.path.abspath(path), recursive))
    
    def scan(self):
        candidates = self._scanDirs()
        all_descs = ( self._loadPluginDesc(c) for c in candidates )
        plugin_descs = [ d for d in all_descs if d ]
        return plugin_descs
    
    def getType(self, shadow, typeName):
        module, clazz = self._splitTypeName(typeName)
        
        if shadow not in self.loadedPlugins:
            if shadow.path() not in sys.path:
                sys.path.insert(0, shadow.path())
            self.loadedPlugins.add(shadow)
        
        mod = self._loadModule(shadow, module)
        typ = mod.__dict__.get(clazz)
        
        if not typ:
            raise Exception("Type '%s' not found in module '%s'" % (clazz, module))
        
        return typ
    
    def _scanDirs(self):
        candidates = []
        plugin_dirs = self.plugin_dirs or [('.', None, False)]
        
        for path, recursive in plugin_dirs:
            ld = os.listdir if not recursive else listdir_recursive
            listdir = ( os.path.join(p) for p in ld(path) )
            plugindirs = ( p for p in listdir if self._isPlugin(p) )
            
            candidates.extend(plugindirs)
        
        return candidates
    
    def _isPlugin(self, path):
        return os.path.isdir(path) and os.path.isfile(os.path.join(path, DeclarativePluginScanner.PLUGIN_DESC_FILE))
    
    def _loadPluginDesc(self, path):
        try:
            desc_path = os.path.join(path, DeclarativePluginScanner.PLUGIN_DESC_FILE)
            desc = PluginDescParser.parse_file(desc_path)
            desc._path = path
            log.debug("Loaded plugin desc '%s'", desc.name())
            return desc
        except:
            log.exception("Failed to load plugin desc in '%s'", path)
    
    def _loadModule(self, shadow, module):
        mod = __import__(module, {}, {}, ['*'])
        if mod not in self.resolvedModules:
            pl_t = self._findSubclass(PluginBase, mod)
            if pl_t:
                pl = pl_t()
                pl.init(shadow)
            
            self.resolvedModules.add(mod)
        
        return mod
    
    def _splitTypeName(self, typeName):
        p = typeName.split('.')
        module = '.'.join(p[:-1])
        clazz = p[-1]
        return module, clazz
    
    def _findSubclass(self, base, mod):
        mn = mod.__name__
        sc = base.__subclasses__()
        for c in sc:
            if c.__module__ == mn:
                return c
        return None



