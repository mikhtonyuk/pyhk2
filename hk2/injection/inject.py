from internal import internal

import inspect

#===========================================================

class inject(object):
    def __init__(self, *vargs):
        self._inject = list(vargs)
        assert all((isinstance(x, type) for x in self._inject))
    
    def __call__(self, c):
        m = c.__init__
        argspec = inspect.getargspec(m)
        pargs = argspec.args[1:]
        
        if len(pargs) != len(self._inject):
            raise Exception("Invalid injection params of '%s', "\
                            "injects %s but constructs with %s" \
                            % (c, self._inject, pargs))
        
        setattr(c, internal.INJECT_ATTR, self._inject)
        return c
