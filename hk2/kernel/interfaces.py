from hk2.types import interface

#===========================================================

@interface
class IModuleScanner(object):
    def scan(self, module):
        """Scans module for defined contracts and services
        :returns: tuple of lists (contracts, services)"""

#===========================================================

@interface
class IPluginLoader(object):
    def getPlugins(self):
        """Returns list of plugin names"""

    def scanPlugins(self):
        """Scans plugins for services and contracts
        :returns: tuple of lists (modules, contracts, services)"""

#===========================================================
