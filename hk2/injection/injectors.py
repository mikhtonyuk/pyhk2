from internal import internal
from inject import inject

from hk2.types import interface

import inspect

#===========================================================

@interface
class Injector(object):
    def getDependencies(self):
        """Returns list of inject_param
        :rtype : list(inject_param)"""

    def inject(self, inst, dependencies):
        """Applies injector with resolved dependencies"""

#===========================================================

class InitInjector(Injector):
    def __init__(self, clazz, ips):
        self.clazz = clazz
        self.ips = ips

    def getDependencies(self):
        return self.ips

    def inject(self, inst, dependencies):
        assert inst is None
        return self.clazz(*dependencies)

#===========================================================

class MethodInjector(Injector):
    def __init__(self, clazz, method, ips):
        self.clazz = clazz
        self.method = method
        self.ips = ips

    def getDependencies(self):
        return self.ips

    def inject(self, inst, dependencies):
        self.method(inst, *dependencies)

#===========================================================

class InjectorFactory(object):

    @staticmethod
    def getInitInjector(clazz):
        ips = inject.getParams(clazz.__init__)
        return InitInjector(clazz, ips)

    @staticmethod
    def getMethodInjectors(clazz):
        members = (m for n, m in inspect.getmembers(clazz))
        methods = (m for m in members if inspect.ismethod(m) and m.__name__ != '__init__')
        setters = (m for m in methods if hasattr(m, internal.INJECT_ATTR))
        return [MethodInjector(clazz, m, inject.getParams(m)) for m in setters]
