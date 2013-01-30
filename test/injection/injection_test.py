from hk2.types import interface
from hk2.injection import inject, Container

import unittest

#===========================================================

@interface
class A(object):
    def foo(self):
        pass

@interface
class B(object):
    def bar(self):
        pass

class ImplA(A):
    
    @inject(B)
    def __init__(self, b):
        self.b = b
    
    def foo(self):
        return 'foo ' + self.b.bar()

class ImplB(B):
    def bar(self):
        return 'bar'

class ImplB2(B):
    def bar(self):
        return 'bar2'

class ImplBNoInjectDecl(B):
    def __init__(self, c):
        self.c = c

class ImplBCyclic(B):
    
    @inject(A)
    def __init__(self, a):
        self.a = a
    
    def bar(self):
        return 'cyclobar'

#===========================================================

class InjectionTest(unittest.TestCase):
    
    def testBasicGet(self):
        c = Container()
        c.bind(B, ImplB)
        b = c.get(B)
        self.assertIsInstance(b, ImplB)
    
    def testInjectionGet(self):
        c = Container()
        c.bind(A, ImplA)
        c.bind(B, ImplB)
        a = c.get(A)
        self.assertIsInstance(a, ImplA)
        self.assertEqual(a.foo(), 'foo bar')
    
    def testMultiBind(self):
        c = Container()
        c.bind(B, ImplB)
        c.bind(B, ImplB2)
        insts = c.getAll(B)
        self.assertEqual(len(insts), 2)
        self.assertIsInstance(insts[0], ImplB)
        self.assertIsInstance(insts[1], ImplB2)
    
    def testRaisesOnNotBound(self):
        c = Container()
        c.bind(B, ImplB)
        self.assertRaises(Exception, lambda:c.get(A))
    
    def testRaisesOnRepeatedBinding(self):
        c = Container()
        c.bind(A, ImplA)
        self.assertRaises(Exception, lambda:c.bind(A,ImplA))
    
    def testRaisesOnAmbiguity(self):
        c = Container()
        c.bind(B, ImplB)
        c.bind(B, ImplB2)
        self.assertRaises(Exception, lambda:c.get(B))
    
    def testRaisesOnCtorWithoutInjectParams(self):
        c = Container()
        self.assertRaises(Exception, lambda:c.bind(B, ImplBNoInjectDecl))
    
    def testRaisesOnCyclicDependencies(self):
        c = Container()
        c.bind(A, ImplA)
        c.bind(B, ImplBCyclic)
        self.assertRaises(Exception, lambda:c.get(A))





