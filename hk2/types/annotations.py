import inspect

#===========================================================

class Annotations(object):
    
    @staticmethod
    def getAnnotations(clazz):
        return clazz.__annots__ if hasattr(clazz, '__annots__') else []
    
    @staticmethod
    def addAnnotation(clazz, ann):
        anns = []
        if hasattr(clazz, '__annots__'):
            anns = clazz.__annots__
        else:
            setattr(clazz, '__annots__', anns)
        anns.append(ann)
    
    @staticmethod
    def getAnnotatedClasses(module, annotation):
        annotations = annotation if isinstance(annotation, list) else [annotation]
        types = (v for v in module.__dict__.itervalues() if isinstance(v, type))
        return ((a,t) for t in types \
                         for a in Annotations.getAnnotations(t) \
                            if a.__class__ in annotations)

#===========================================================

def ClassAnnotation(t):
    spec = inspect.getargspec(t.__init__) if t.__init__ != object.__init__ else None
    only_ctor = spec and (len(spec.args) - 1) != len(spec.defaults or [])
    
    def _apply_(*va, **ka):
        if not only_ctor and len(va) == 1 and isinstance(va[0], type):
            Annotations.addAnnotation(va[0], t())
            return va[0]
        else:
            ann = t(*va, **ka)
            def _attach_(c):
                Annotations.addAnnotation(c, ann)
                return c
            return _attach_
    
    return _apply_

#===========================================================
