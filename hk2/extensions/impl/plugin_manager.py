from hk2.extensions.interfaces import IPluginManager, ExtParamConstraint

from hk2.extensions.impl.plugin_shadow import PluginShadow
from hk2.extensions.impl.extension_point import ExtensionPoint
from hk2.extensions.impl.plugin_graph import PluginGraph

from hk2.utils.version import Version

import logging
log = logging.getLogger('hk2.extensions') 

#===========================================================

class PluginManager(IPluginManager):
    def __init__(self, scanner):
        self._scanner = scanner
        self._plugins = {}
        self._extensionPoints = {}
        self._loadedPlugins = set()
        
        self._loadGraph()
    
    def plugins(self):
        return self._plugins
    
    def extensionPoints(self):
        return self._extensionPoints
    
    def createInstance(self, ext):
        ep = ext.extensionPoint()
        
        try:
            iface = self._scanner.getType(ep.plugin(), ep.interfaceName())
            clazz = self._scanner.getType(ext.plugin(), ext.className())
            inst = clazz()
        except:
            log.exception("Extension instantiation failed EP=%s, Ext=%s" \
                          % (ext.extensionPoint().fullName(), ext.plugin().name()))
            raise
        
        if not isinstance(inst, iface):
            raise Exception("Extension does not implement required interface EP=%s, Ext=%s" \
                            % (ext.extensionPoint().fullName(), ext.plugin().name()))
        
        return inst
    
    def start(self, args=None):
        log.info("Running hk2::start_listeners extensions")
        
        stl = self._extensionPoints['hk2::start_listeners']
        exts = list(stl.extensions())
        exts.sort(key = lambda x: x.parameters().get('priority', 50))
        
        for ext in exts:
            inst = self.createInstance(ext)
            inst.start(args)
        
        log.info("Shutting down hk2")
    
    def _getKernelPlugin(self):
        kpl = PluginShadow()
        kpl._name = 'hk2'
        kpl._desc = 'pyhk2 kernel plugin'
        kpl._author = 'Sergii Mikhtoniuk (mikhtoniuk@gmail.com)'
        kpl._version = Version('1.0.0')
        
        stl = ExtensionPoint()
        stl._plugin = kpl
        stl._name = 'start_listeners'
        stl._interface = 'hk2.extensions.IStartListener'
        stl._params = { "priority" : ExtParamConstraint.Optional }
        
        kpl._extensionPoints.append(stl)
        return kpl
    
    def _loadGraph(self):
        log.info("Loading plugins")
        shadows = self._scanner.scan()
        shadows.append(self._getKernelPlugin())
        
        log.info("Resolving plugin graph")
        pg = PluginGraph()
        self._plugins, self._extensionPoints = pg.resolve(shadows)

