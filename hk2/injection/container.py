from bindings import Bindings
from internal import internal

import inspect

#===========================================================

class Container(object):
    def __init__(self, bindings=None):
        self._binds = bindings or Bindings()

    def bind(self, what, to):
        return self._binds.bind(what, to)

    def get(self, what, default=internal.raiseOnMissing):
        bind = self._binds.get(what, default)
        if bind == default:
            return bind
        return self._getInstance(bind, [what])

    def getAll(self, what):
        binds = self._binds.getAll(what)
        instances = [self._getInstance(t, [what]) for t in binds]
        return instances

    def inject(self, into):
        members = (m for n, m in inspect.getmembers(into))
        methods = (m for m in members if inspect.ismethod(m) and m.__name__ != '__init__')
        setters = (m for m in methods if hasattr(m, internal.INJECT_ATTR))
        for s in setters:
            inject = self._getInjectParams(s)
            params = [self._resolve(ip, []) for ip in inject]
            s(*params)

    def _getInstance(self, t, resolving):
        inject = self._getInjectParams(t.__init__)

        cyclic = set((p.type for p in inject)).intersection(resolving)
        if cyclic:
            self._raiseCyclicDepsError(cyclic, resolving)

        params = [self._resolve(ip, resolving) for ip in inject]
        return t(*params)

    def _resolve(self, inject_param, resolving):
        newResolving = resolving + [inject_param.type]
        if not inject_param.multi:
            bind = self._binds.get(inject_param.type)
            return self._getInstance(bind, newResolving)
        else:
            binds = self._binds.getAll(inject_param.type)
            return [self._getInstance(b, newResolving) for b in binds]

    def _getInjectParams(self, x):
        return getattr(x, internal.INJECT_ATTR) if hasattr(x, internal.INJECT_ATTR) else []

    def _raiseCyclicDepsError(self, on_what, path):
        swhat = ','.join((internal.className(w) for w in on_what))
        spath = ['%d. %s' % (i + 1, internal.className(c)) for i, c in enumerate(path)]
        spath = '\n'.join(spath)
        raise Exception("Cyclic dependency detected on '%s', injection path:\n%s" % (swhat, spath))
