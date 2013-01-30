from hk2.types import ClassAnnotation, Annotations

import unittest

#===========================================================

class Test(ClassAnnotation):
    def apply(self, t, data = None):
        self.data = data

class Test2(ClassAnnotation):
    def apply(self, t, clazz):
        self.clazz = clazz

#===========================================================

@Test()
class Foo(object):
    pass

@Test('bar')
class Bar(object):
    pass

@Test2(Bar)
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
        ats = Annotations.getAnnotatedClasses(Test)
        self.assertEqual(len(ats), 2)
        self.assertEqual(ats[0][0].data, 'bar')

