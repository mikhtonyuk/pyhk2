from hk2.types import ClassAnnotation, Annotations

import unittest, sys

#===========================================================

class TestAnnotation(object):
    def __init__(self, data = None):
        self.data = data

class Test2Annotation(object):
    def __init__(self, clazz):
        self.clazz = clazz

test = ClassAnnotation(TestAnnotation)
test2 = ClassAnnotation(Test2Annotation)

#===========================================================

@test
class Foo(object):
    pass

@test('bar')
class Bar(object):
    pass

@test2(Bar)
class Bazz(object):
    pass

#===========================================================

class AnnotationsTest(unittest.TestCase):
    def testClassAnnontationsList(self):
        self.assertEqual(len(Annotations.getAnnotations(Foo)), 1)
    
    def testClassAnnotationsParams(self):
        self.assertEqual(len(Annotations.getAnnotations(Bar)), 1)
        self.assertEqual(Annotations.getAnnotations(Bar)[0].data, 'bar')
    
    def testGettingClassesByAnnotations(self):
        module = sys.modules[__name__]
        ats = list(Annotations.getAnnotatedClasses(module, TestAnnotation))
        self.assertEqual(len(ats), 2)
        self.assertEqual(ats[0][0].data, 'bar')

