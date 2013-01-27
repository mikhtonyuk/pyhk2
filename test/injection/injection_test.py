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

@inject(B)
class ImplA(A):
    def __init__(self, b):
        self.b = b
    
    def foo(self):
        return 'foo ' + self.b.bar()

class ImplB(B):
    def bar(self):
        return 'bar'

class ImplBNoInjectDecl(B):
    def __init__(self, c):
        self.c = c

@inject(A)
class ImplBCyclic(B):
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
    
    def testRaisesOnNotBound(self):
        c = Container()
        c.bind(B, ImplB)
        self.assertRaises(Exception, lambda:c.get(A))
    
    def testRaisesOnRepeatedBinding(self):
        c = Container()
        c.bind(A, ImplA)
        self.assertRaises(Exception, lambda:c.bind(A,ImplA))
    
    def testRaisesOnCtorWithoutInjectParams(self):
        c = Container()
        self.assertRaises(Exception, lambda:c.bind(B, ImplBNoInjectDecl))
    
    def testRaisesOnCyclicDependencies(self):
        c = Container()
        c.bind(A, ImplA)
        c.bind(B, ImplBCyclic)
        self.assertRaises(Exception, lambda:c.get(A))





