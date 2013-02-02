from hk2.types import Annotations
from hk2.annotations import Contract, Service

import logging
log = logging.getLogger(__name__)

#===========================================================

class ModuleScanner(object):
    def scan(self, module):
        contracts = [c for c, a in Annotations.getAnnotatedClasses(module, Contract)]
        services = [c for c, a in Annotations.getAnnotatedClasses(module, Service)]
        return contracts, services
