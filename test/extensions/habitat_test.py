from hk2.types import interface
from hk2.annotations import Contract, Service
from hk2.injection import inject
from hk2.kernel import Habitat
import unittest

#===========================================================

@interface
@Contract()
class ISingle(object):
    def foo(self):
        '''does foo'''

@Service()
class SingleImpl(ISingle):
    def foo(self):
        return "foo"

#===========================================================

@interface
@Contract()
class IMulti(object):
    def foo(self):
        '''does foo'''

@Service()
class MultiImpl1(IMulti):
    def foo(self):
        return 'foo1'

@Service()
class MultiImpl2(IMulti):
    def foo(self):
        return 'foo2'

#===========================================================

@interface
@Contract()
class IDepends(object):
    def foo(self):
        '''does foo'''

@Service()
class DependsImpl(IDepends):
    
    @inject(ISingle)
    def __init__(self, fooer):
        self._fooer = fooer
    
    def foo(self):
        return 'depends ' + self._fooer.foo()

#===========================================================

class HabitatTest(unittest.TestCase):
    def testGetByContractSingle(self):
        h = Habitat()
        svs = h.getAllByContract(ISingle)
        self.assertEqual(len(svs), 1)
        self.assertIsInstance(svs[0], SingleImpl)
    
    def testGetByContractMulti(self):
        h = Habitat()
        svs = h.getAllByContract(IMulti)
        self.assertEqual(len(svs), 2)
        self.assertTrue(any([isinstance(s, MultiImpl1) for s in svs]))
        self.assertTrue(any([isinstance(s, MultiImpl2) for s in svs]))
        self.assertSetEqual(set((s.foo() for s in svs)), set(('foo1', 'foo2')))
    
    def testGetByContractInjection(self):
        h = Habitat()
        svs = h.getAllByContract(IDepends)
        self.assertEqual(len(svs), 1)
        self.assertIsInstance(svs[0], DependsImpl)
        self.assertEqual(svs[0].foo(), 'depends foo')


