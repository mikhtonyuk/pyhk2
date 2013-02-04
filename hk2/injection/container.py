from bindings import Bindings, InstanceBinding
from injection_context import InjectionContext
from exceptions import InjectionError
from internal import internal
from inject import inject_param, allof

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
        ctx = InjectionContext(self._binds, InstanceBinding(into), ip)
        ctx.inject(into)
