from internal import internal
from bindings import InstanceBinding, ClassBinding
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

class ClassInitInjector(Injector):
    def __init__(self, clazz, ips):
        self.clazz = clazz
        self.ips = ips

    def getDependencies(self):
        return self.ips

    def inject(self, inst, dependencies):
        assert inst is None
        return self.clazz(*dependencies)

#===========================================================

class InstanceInitInjector(Injector):
    def __init__(self, inst):
        self.inst = inst

    def getDependencies(self):
        return []

    def inject(self, inst, dependencies):
        return self.inst

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

class PropertyInjector(Injector):
    def __init__(self, clazz, name, prop, ips):
        self.clazz = clazz
        self.name = name
        self.prop = prop
        self.ips = ips

    def getDependencies(self):
        return self.ips

    def inject(self, inst, dependencies):
        setattr(inst, self.name, *dependencies)

#===========================================================

class InjectorFactory(object):

    @staticmethod
    def getInitInjector(bind):
        if isinstance(bind, InstanceBinding):
            return InstanceInitInjector(bind.value)
        elif isinstance(bind, ClassBinding):
            clazz = bind.value
            ips = inject.getParams(clazz.__init__)
            return ClassInitInjector(clazz, ips)
        else:
            raise NotImplemented("Unsupported binding type")

    @staticmethod
    def getInstanceInjectors(bind):
        clazz = None
        if isinstance(bind, ClassBinding):
            clazz = bind.value
        elif isinstance(bind, InstanceBinding):
            clazz = bind.value.__class__

        ret = []
        ret.extend(InjectorFactory.getMethodInjectors(clazz))
        ret.extend(InjectorFactory.getPropertyInjectors(clazz))
        return ret

    @staticmethod
    def getMethodInjectors(clazz):
        members = (m for n, m in inspect.getmembers(clazz, inspect.ismethod))
        methods = (m for m in members if m.__name__ != '__init__')
        setters = (m for m in methods if hasattr(m, internal.INJECT_ATTR))
        return [MethodInjector(clazz, m, inject.getParams(m)) for m in setters]

    @staticmethod
    def getPropertyInjectors(clazz):
        props = [(n,p) for n, p in inspect.getmembers(clazz) if isinstance(p, property)]
        setters = ((n, p) for n, p in props if p.fset and hasattr(p.fset, internal.INJECT_ATTR))
        return [PropertyInjector(clazz, n, p, inject.getParams(p.fset)) for n, p in setters]