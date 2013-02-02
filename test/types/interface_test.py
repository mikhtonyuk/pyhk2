from hk2.types import interface
import unittest

@interface
class IFoo(object):
    def foo(self):
        '''does foo'''

class Foo(IFoo):
    def foo(self):
        return "foo"

class PseudoFoo(IFoo):
    pass

class InterfaceTest(unittest.TestCase):
    def testTypeID(self):
        f = Foo()
        self.assertEqual(f.foo(), 'foo')
        self.assertTrue(isinstance(f, IFoo))
    
    def testRaisesNotImplementedError(self):
        f = PseudoFoo()
        self.assertRaises(NotImplementedError, f.foo)
    