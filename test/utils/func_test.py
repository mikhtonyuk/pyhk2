import hk2.utils.func as func

import unittest

#===========================================================

class FuncTest(unittest.TestCase):
    def testForeach(self):
        seq = (i for i in range(5))
        nseq = []
        func.foreach(nseq.append, seq)
        self.assertListEqual(nseq, [0, 1, 2, 3, 4])

    def testCount(self):
        seq = (i for i in range(5))
        c = func.count(seq)
        self.assertEqual(c, 5)

    def testCountIf(self):
        seq = (i for i in range(5))
        c = func.count(seq, lambda x: x % 2 == 0)
        self.assertEqual(c, 3)

    def testGroupBy(self):
        seq = (i for i in range(5))
        group = func.group_by(lambda x: x % 2, seq)
        expected = {0: [0, 2, 4], 1: [1, 3]}
        self.assertDictEqual(group, expected)
