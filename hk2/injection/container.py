from bindings import Bindings
from internal import internal

#===========================================================

class Container(object):
    def __init__(self, bindings = None):
        self._binds = bindings or Bindings()
    
    def get(self, what):
        return self._getImpl(what, [what])
    
    def _getImpl(self, what, resolving):
        t = self._binds.get(what)
        inject = t.__inject__ if hasattr(t, internal.INJECT_ATTR) else []
        
        cyclic = set(inject).intersection(resolving)
        if cyclic:
            self._raiseCyclicDepsError(cyclic, resolving)
        
        params = [self._getImpl(i, resolving + [i]) for i in inject]
        return t(*params)
    
    def _raiseCyclicDepsError(self, on_what, path):
        swhat = ','.join((internal.className(w) for w in on_what))
        spath = ['%d. %s' % (i+1, internal.className(c)) for i, c in enumerate(path)]
        spath = '\n'.join(spath)
        raise Exception("Cyclic dependency detected on '%s', injection path:\n%s" % (swhat, spath))
    
    def bind(self, what, to):
        return self._binds.bind(what, to)