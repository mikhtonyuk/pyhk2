from internal import internal

import inspect

#===========================================================

class Bindings(object):
    def __init__(self):
        self._bindings = {}
    
    def bind(self, what, to):
        assert isinstance(what, type)
        assert isinstance(to, type)
        
        if what in self._bindings:
            raise Exception("'%s' is already bound to '%s'" % (what, self._bindings[what]))
        
        if to.__init__ != object.__init__ and \
           len(inspect.getargspec(to.__init__).args) != 1 and \
           not hasattr(to, internal.INJECT_ATTR):
            raise Exception("'%s' has non-trivial ctor so should be decorated with @inject" % (to))
        
        self._bindings[what] = to
    
    def get(self, what, default = internal.raiseOnMissing):
        ret = self._bindings.get(what)
        if not ret:
            if internal.raiseOnMissing == default:
                raise Exception("'%s' not bound" % (what))
            return default
        return ret