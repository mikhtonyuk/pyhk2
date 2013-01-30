from hk2.annotations import Contract, Service
from hk2.injection import Container
from hk2.types import Annotations

#===========================================================

class Habitat(object):
    def __init__(self):
        self._ioc = Container()
        self._services = set()
        self._contracts = set()
        self._servicesToContracts = {}
        
        self._scan()
        self._regInIoC()
    
    def _scan(self):
        self._contracts = set((c for _a,c in Annotations.getAnnotatedClasses(Contract)))
        self._services = set((c for _a,c in Annotations.getAnnotatedClasses(Service)))
        self._servicesToContracts = { s : self._getServiceContracts(s, self._contracts) for s in self._services}
    
    def _regInIoC(self):
        for s, cts in self._servicesToContracts.iteritems():
            for c in cts:
                self._ioc.bind(c, s)
    
    def _getServiceContracts(self, svc, contracts):
        return [c for c in contracts if issubclass(svc, c)]
    
    def getAllByContract(self, contract):
        return self._ioc.getAll(contract)
