from internal import internal

import inspect
import types

#===========================================================

class inject_param(object):
    def __init__(self, v):
        if isinstance(v, type):
            self.type = v
            self.multi = False
        elif isinstance(v, allof):
            self.type = v.t
            self.multi = True
        else:
            raise Exception("Invalid parameter '%s' to @inject, only types and allof are allowed" % (v))

#===========================================================

class inject(object):
    def __init__(self, *vargs):
        self._inject = [inject_param(v) for v in vargs]

    def __call__(self, m):
        if not isinstance(m, types.FunctionType) or m.__name__ != '__init__':
            raise Exception("@inject can only be applied to __init__ methods")

        argspec = inspect.getargspec(m)
        pargs = argspec.args[1:]

        if len(pargs) != len(self._inject):
            raise Exception("Invalid injection params, injects %s but constructs with %s"
                            % (self._inject, pargs))

        setattr(m, internal.INJECT_ATTR, self._inject)
        return m

#===========================================================

class allof(object):
    def __init__(self, t):
        assert isinstance(t, type)
        self.t = t
