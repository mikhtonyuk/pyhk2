from internal import internal

import inspect

#===========================================================

class Bindings(object):
    def __init__(self):
        self._bindings = {}
    
    def bind(self, what, to):
        assert isinstance(what, type)
        assert isinstance(to, type)
        
        binds = list(self._bindings.get(what, []))
        if to in binds:
            raise Exception("'%s' is already bound to '%s'" \
                            % (internal.className(self._bindings[what]), internal.className(what)))
        
        self._validateInject(to)
        binds.append(to)
        
        self._bindings[what] = binds
    
    def _validateInject(self, clazz):
        if clazz.__init__ != object.__init__ and \
           len(inspect.getargspec(clazz.__init__).args) != 1 and \
           not hasattr(clazz.__init__, internal.INJECT_ATTR):
            raise Exception("'%s' has non-trivial ctor so should be decorated with @inject" \
                            % (internal.className(clazz)))
    
    def get(self, what, default = internal.raiseOnMissing):
        binds = self._bindings.get(what)
        if not binds:
            if internal.raiseOnMissing == default:
                raise Exception("'%s' not bound" % (internal.className(what)))
            return default
        elif len(binds) > 1:
            raise Exception("Get is ambiguous, '%s' has multiple bindings" \
                            % (internal.className(what)))
        return binds[0]
    
    def getAll(self, what):
        return self._bindings.get(what, [])


