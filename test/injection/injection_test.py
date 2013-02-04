from hk2.types import interface
from hk2.injection import inject, allof, Container, InjectionError

import unittest

#===========================================================

@interface
class L1(object):
    def do1(self):
        """"""

@interface
class L2(object):
    def do2(self):
        """"""

@interface
class L3(object):
    def do3(self):
        """"""

#===========================================================

class L1_1(L1):
    def do1(self):
        return 'l1_1'

class L1_2(L1):
    def do1(self):
        return 'l1_2'

class L2_1(L2):

    @inject(L1)
    def __init__(self, l1):
        self.l1 = l1

    def do2(self):
        return 'l2_1 ' + self.l1.do1()

class L2_Multi(L2):

    @inject(allof(L1))
    def __init__(self, l1s):
        self.l1s = l1s

    def do2(self):
        ll = ['l2_multi']
        ll.extend([l.do1() for l in self.l1s])
        return ' '.join(ll)

class L3_1(L3):
    @inject(L2)
    def __init__(self, l2):
        self.l2 = l2

    def do3(self):
        return 'l3_1 ' + self.l2.do2()

class L3_Setter(L3):
    @inject(allof(L1))
    def setL1s(self, l1s):
        self.l1s = l1s

    @inject(L2)
    def setL2(self, l2):
        self.l2 = l2

    def do3(self):
        ll = ['l3_setter']
        ll.extend([l.do1() for l in self.l1s])
        ll.append(self.l2.do2())
        return ' '.join(ll)

class L3_Property(L3):

    @property
    def l1s(self):
        return self._l1s

    @l1s.setter
    @inject(allof(L1))
    def l1s(self, l1s):
        self._l1s = l1s

    @property
    def l2(self):
        return self._l2

    @l2.setter
    @inject(L2)
    def l2(self, l2):
        self._l2 = l2

    def do3(self):
        ll = ['l3_property']
        ll.extend([l.do1() for l in self.l1s])
        ll.append(self.l2.do2())
        return ' '.join(ll)

#===========================================================

class ENoInject(L1):
    def __init__(self, blah):
        """"""

class EL1Cyclic(L1):
    @inject(L3)
    def __init__(self, l3):
        """"""

#===========================================================

class InjectionTest(unittest.TestCase):

    def testBasicGet(self):
        c = Container()
        c.bind(L1, L1_1)
        l = c.get(L1)
        self.assertIsInstance(l, L1_1)

    def testInjectionGet(self):
        c = Container()
        c.bind(L1, L1_1)
        c.bind(L2, L2_1)
        l = c.get(L2)
        self.assertIsInstance(l, L2)
        self.assertEqual('l2_1 l1_1', l.do2())

    def testMultiBind(self):
        c = Container()
        c.bind(L1, L1_1)
        c.bind(L1, L1_2)
        ls = c.getAll(L1)
        self.assertEqual(len(ls), 2)
        self.assertIsInstance(ls[0], L1_1)
        self.assertIsInstance(ls[1], L1_2)

    def testMultiInject(self):
        c = Container()
        c.bind(L1, L1_1)
        c.bind(L1, L1_2)
        c.bind(L2, L2_Multi)
        l = c.get(L2)
        self.assertIsInstance(l, L2_Multi)
        self.assertEqual('l2_multi l1_1 l1_2', l.do2())

    def testSetterInject(self):
        c = Container()
        c.bind(L1, L1_1)
        c.bind(L1, L1_2)
        c.bind(L2, L2_Multi)
        c.bind(L3, L3_Setter)
        l = c.get(L3)
        self.assertEqual('l3_setter l1_1 l1_2 l2_multi l1_1 l1_2', l.do3())

    def testSetterInjectManual(self):
        c = Container()
        c.bind(L1, L1_1)
        c.bind(L1, L1_2)
        c.bind(L2, L2_Multi)
        l = L3_Setter()
        c.inject(l)
        self.assertEqual('l3_setter l1_1 l1_2 l2_multi l1_1 l1_2', l.do3())

    def testPropertyInject(self):
        c = Container()
        c.bind(L1, L1_1)
        c.bind(L1, L1_2)
        c.bind(L2, L2_Multi)
        l = L3_Property()
        c.inject(l)
        self.assertEqual('l3_property l1_1 l1_2 l2_multi l1_1 l1_2', l.do3())

    def testInstanceBinding(self):
        c = Container()
        c.bind(L1, L1_1())
        c.bind(L2, L2_1)
        l = c.get(L2)
        self.assertEqual('l2_1 l1_1', l.do2())

    def testDefaultOnNotBound(self):
        c = Container()
        c.bind(L1, L1_1)
        l = c.get(L2, None)
        self.assertIsNone(l)

    def testRaisesOnNotBound(self):
        c = Container()
        c.bind(L1, L1_1)
        self.assertRaises(InjectionError, lambda: c.get(L2))

    def testRaisesOnUnresolvedDependency(self):
        c = Container()
        c.bind(L2, L2_1)
        self.assertRaises(InjectionError, lambda: c.get(L2))

    def testRaisesOnAmbiguity(self):
        c = Container()
        c.bind(L1, L1_1)
        c.bind(L1, L1_2)
        self.assertRaises(InjectionError, lambda: c.get(L1))

    def testRaisesOnCtorWithoutInjectParams(self):
        c = Container()
        self.assertRaises(InjectionError, lambda: c.bind(L1, ENoInject))

    def testRaisesOnCyclicDependencies(self):
        c = Container()
        c.bind(L1, EL1Cyclic)
        c.bind(L2, L2_1)
        c.bind(L3, L3_1)
        self.assertRaises(InjectionError, lambda: c.get(L3))
