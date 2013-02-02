from hk2.types import interface

from module_scanner import ModuleScanner

import os
import logging
log = logging.getLogger(__name__)

#===========================================================

PLUGIN_FILE = '__plugin__.py'

#===========================================================

@interface
class IPluginLoader(object):
    def getPlugins(self):
        """Returns list of plugin names"""

    def scanPlugins(self, plugins=None):
        """Scans all or specified plugins, returns lists of (contracts, services)"""

#===========================================================

class FilePluginLoader(IPluginLoader):
    def __init__(self, scan_dirs=None):
        self._scan_dirs = scan_dirs or ['.']
        self._plugin_dirs = []
        self._moduleScanner = ModuleScanner()

    def getPlugins(self):
        if len(self._plugin_dirs) == 0:
            self._plugin_dirs = self._searchPlugins()

        return self._plugin_dirs

    def scanPlugins(self, plugins=None):
        modules = []
        contracts = []
        services = []

        plugins = plugins or self.getPlugins()

        for p in plugins:
            for m in self._getPluginModules(p):
                module = self._loadModule(m)
                if module:
                    cts, svc = self._moduleScanner.scan(module)
                    modules.append(module)
                    contracts.extend(cts)
                    services.extend(svc)

        return modules, contracts, services

    def _searchPlugins(self):
        return [d for d in self._scan_dirs if self._isPluginDir(d)]

    def _isPluginDir(self, dir):
        pf = os.path.join(dir, PLUGIN_FILE)
        return os.path.isfile(pf)

    def _getPluginModules(self, plugin_dir):
        candidate_modules = [os.path.join(plugin_dir, ld) for ld in os.listdir(plugin_dir)]
        return [cm for cm in candidate_modules if self._isModuleCandidate(cm)]

    def _isModuleCandidate(self, path):
        _d, fn = os.path.split(path)
        base, ext = os.path.splitext(fn)
        return os.path.isfile(path) and not base.startswith('__') and ext == '.py'

    def _loadModule(self, module_path):
        module_import = self._pathToImport(module_path)
        try:
            module = __import__(module_import)
            module = self._navigateToModule(module_import, module)
            return module
        except:
            log.exception("Error wile scanning module '%s'" % (module_import))
            return None

    def _pathToImport(self, path):
        return os.path.splitext(path)[0].replace(os.sep, '.')

    def _navigateToModule(self, import_path, root):
        navi = import_path.split('.')
        if len(navi) == 1:
            return root
        module = root
        for n in navi[1:]:
            module = module.__dict__[n]
        return module
