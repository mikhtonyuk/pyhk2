from interface import interface

#===========================================================

@interface
class IAnnotationRegistry(object):
    def add(self, clazz, ann):
        """Associates annotation with specified class"""
    
    def getByClass(self, clazz):
        """Returns all associated annotations"""

#===========================================================

class DictAnnotationRegistry(IAnnotationRegistry):
    def __init__(self):
        self._annotations = {}
    
    def add(self, clazz, ann):
        annl = self._annotations.get(clazz)
        if not annl:
            annl = []
            self._annotations[clazz] = annl
        annl.append(ann)
    
    def getByClass(self, clazz):
        return list(self._annotations.get(clazz, []))
    
    def find(self, pred):
        return [(a,c) for c, anns in self._annotations.iteritems()
                        for a in anns
                          if pred(a,c)]

#===========================================================

class Annotations(object):
    _registry = DictAnnotationRegistry()
    
    @staticmethod
    def getAnnotations(clazz):
        return Annotations._registry.getByClass(clazz)
    
    @staticmethod
    def addAnnotation(clazz, ann):
        Annotations._registry.add(clazz, ann)
    
    @staticmethod
    def getAnnotatedClasses(ann_type):
        return Annotations._registry.find(lambda a,c: isinstance(a, ann_type))

#===========================================================

class ClassAnnotation(object):
    def __init__(self, *va, **ka):
        self.args = (va, ka)
    
    def __call__(self, t):
        self.apply(t, *self.args[0], **self.args[1])
        Annotations.addAnnotation(t, self)
        return t
    
    def apply(self, t):
        pass