from exceptions import InjectionError
from internal import internal

import inspect

#===========================================================

class InstanceBinding(object):
    def __init__(self, val):
        self.value = val
    
    def __str__(self):
        return "instance binding: %s" % (self.value)

#===========================================================

class ClassBinding(object):
    def __init__(self, val):
        self.value = val
        if val.__init__ != object.__init__ \
                and len(inspect.getargspec(val.__init__).args) != 1 \
                and not hasattr(val.__init__, internal.INJECT_ATTR):
            raise InjectionError("'%s' has non-trivial ctor so should be decorated with @inject"
                                 % (internal.className(val)))
    
    def __str__(self):
        return "class binding: %s" % (internal.className(self.value))

#===========================================================

class Bindings(object):
    def __init__(self):
        self._bindings = {}

    def bind(self, what, to=None):
        assert isinstance(what, type)
        bind = self._createBinding(to if to is not None else what)

        binds = list(self._bindings.get(what, []))
        binds.append(bind)

        self._bindings[what] = binds

    def _createBinding(self, to):
        if isinstance(to, type):
            return ClassBinding(to)
        else:
            return InstanceBinding(to)

    def get(self, what, default=internal.raiseOnMissing):
        binds = self._bindings.get(what)
        if not binds:
            if internal.raiseOnMissing == default:
                raise InjectionError("'%s' not bound" % (internal.className(what)))
            return default
        elif len(binds) > 1:
            raise InjectionError("Get is ambiguous, '%s' has multiple bindings"
                                 % (internal.className(what)))
        return binds[0]

    def getAll(self, what):
        return self._bindings.get(what, [])
