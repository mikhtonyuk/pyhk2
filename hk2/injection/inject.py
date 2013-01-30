from internal import internal

import inspect
import types

#===========================================================

class inject(object):
    def __init__(self, *vargs):
        self._inject = list(vargs)
    
    def __call__(self, m):
        if not isinstance(m, types.FunctionType) or m.__name__ != '__init__':
            raise Exception("@inject can only be applied to __init__ methods")
        
        argspec = inspect.getargspec(m)
        pargs = argspec.args[1:]
        
        if len(pargs) != len(self._inject):
            raise Exception("Invalid injection params, "\
                            "injects %s but constructs with %s" \
                            % (self._inject, pargs))
        
        setattr(m, internal.INJECT_ATTR, self._inject)
        return m
