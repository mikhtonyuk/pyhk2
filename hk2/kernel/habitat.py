from hk2.injection import Container

from sysmod_plugin_loader import SysmodPluginLoader

#===========================================================

class Habitat(object):
    def __init__(self, plugin_loader=None):
        """
        :type plugin_loader: IPluginLoader
        """
        self._loader = plugin_loader or SysmodPluginLoader()
        self._ioc = Container()
        self._services = set()
        self._contracts = set()
        self._servicesToContracts = {}

        self._scan()
        self._regInIoC()

    def _scan(self):
        m, c, s = self._loader.scanPlugins()
        self._contracts = set(c)
        self._services = set(s)
        self._servicesToContracts = {}
        for s in self._services:
            cts = self._getServiceContracts(s, self._contracts)
            if not cts:
                raise Exception("Service '%s' does not implement any contracts" % (s))
            self._servicesToContracts[s] = cts

    def _regInIoC(self):
        for s, cts in self._servicesToContracts.iteritems():
            for c in cts:
                self._ioc.bind(c, s)

    def _getServiceContracts(self, svc, contracts):
        return [c for c in contracts if issubclass(svc, c)]

    def getAllByContract(self, contract):
        return self._ioc.getAll(contract)
