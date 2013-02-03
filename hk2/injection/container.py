from bindings import Bindings
from exceptions import InjectionError, DeepInjectionError
from internal import internal
from inject import inject_param, allof
from injectors import InjectorFactory

#===========================================================

class InjectionContext(object):
    def __init__(self, bindings, clazz, resolving, parent=None):
        """:type bindings: Bindings"""
        self.binds = bindings
        self.clazz = clazz
        self.resolving = resolving
        self.parent = parent

        self.checkCyclic()

        self.activator = InjectorFactory.getInitInjector(clazz)
        self.injectors = InjectorFactory.getMethodInjectors(clazz)

        self.activator_deps = self.collectDependencies(self.activator)
        self.other_deps = [self.collectDependencies(inj) for inj in self.injectors]

    def activate(self):
        activator_deps = self.activateDependencies(self.activator_deps)
        inst = self.activator.inject(None, activator_deps)
        self.inject(inst)
        return inst

    def inject(self, inst):
        other_deps = [self.activateDependencies(deps) for deps in self.other_deps]
        for inj, deps in zip(self.injectors, other_deps):
            inj.inject(inst, deps)

    def collectDependencies(self, injector):
        ips = injector.getDependencies()

        deps = []
        for ip in ips:
            try:
                if not ip.multi:
                    bound = self.binds.get(ip.type)
                    ctx = InjectionContext(self.binds, bound, ip, self)
                    deps.append((ip, ctx))
                else:
                    bound = self.binds.getAll(ip.type)
                    ctxz = [InjectionContext(self.binds, b, ip, self) for b in bound]
                    deps.append((ip, ctxz))
            except DeepInjectionError:
                raise
            except InjectionError, iex:
                raise DeepInjectionError(iex.message, self, ip)

        return deps

    def activateDependencies(self, deps):
        ret = []
        for ip, dep in deps:
            if not ip.multi:
                ret.append(dep.activate())
            else:
                ret.append([ctx.activate() for ctx in dep])
        return ret

    def checkCyclic(self):
        ctx = self.parent
        while ctx:
            if self.resolving.type == ctx.resolving.type:
                raise DeepInjectionError("Cyclic dependency on '%s'" % (internal.className(self.resolving.type)),
                                         self)
            ctx = ctx.parent

#===========================================================

class Container(object):
    def __init__(self, bindings=None):
        self._binds = bindings or Bindings()

    def bind(self, what, to):
        return self._binds.bind(what, to)

    def get(self, what, default=internal.raiseOnMissing):
        try:
            ip = inject_param(what)
            bound = self._binds.get(what)
            ctx = InjectionContext(self._binds, bound, ip)
            return ctx.activate()
        except InjectionError:
            if default == internal.raiseOnMissing:
                raise
        return default

    def getAll(self, what):
        ip = inject_param(allof(what))
        bound = self._binds.getAll(what)
        ctxz = [InjectionContext(self._binds, b, ip) for b in bound]
        return [ctx.activate() for ctx in ctxz]

    def inject(self, into):
        ip = inject_param(into.__class__)
        ctx = InjectionContext(self._binds, into.__class__, ip)
        ctx.inject(into)
