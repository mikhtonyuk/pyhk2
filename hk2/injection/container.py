from bindings import Bindings
from internal import internal

#===========================================================

class Container(object):
    def __init__(self, bindings = None):
        self._binds = bindings or Bindings()
    
    def get(self, what, default = internal.raiseOnMissing):
        bind = self._binds.get(what, default)
        if bind == default:
            return bind
        return self._getInstance(bind, [what])
    
    def getAll(self, what):
        binds = self._binds.getAll(what)
        instances = [self._getInstance(t, [what]) for t in binds]
        return instances
    
    def _getInstance(self, t, resolving):
        inject = self._getInjectParams(t)
        
        cyclic = set((p.type for p in inject)).intersection(resolving)
        if cyclic:
            self._raiseCyclicDepsError(cyclic, resolving)
        
        params = []
        for ip in inject:
            newResolving = resolving + [ip.type]
            if not ip.multi:
                bind = self._binds.get(ip.type)
                params.append(self._getInstance(bind, newResolving))
            else:
                binds = self._binds.getAll(ip.type)
                params.append([self._getInstance(b, newResolving) for b in binds])
        
        return t(*params)
    
    def _getInjectParams(self, t):
        init = t.__init__
        return getattr(init, internal.INJECT_ATTR) if hasattr(init, internal.INJECT_ATTR) else []
    
    def _raiseCyclicDepsError(self, on_what, path):
        swhat = ','.join((internal.className(w) for w in on_what))
        spath = ['%d. %s' % (i+1, internal.className(c)) for i, c in enumerate(path)]
        spath = '\n'.join(spath)
        raise Exception("Cyclic dependency detected on '%s', injection path:\n%s" % (swhat, spath))
    
    def bind(self, what, to):
        return self._binds.bind(what, to)