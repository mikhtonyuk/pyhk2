from hk2.types import enum, flags, flags_seq

import unittest

@enum
class DayOfWeek(object):
    Monday, Tuesday, Wednesday, \
    Thursday, Friday, Saturday, Sunday = range(7)

@flags
class Caps(object):
    Read, Write, Create, Delete = flags_seq(4)
    All = 0xff


class TestEnum(unittest.TestCase):
    def testBasicValues(self):
        self.assertEqual(DayOfWeek.Monday, 0)
        self.assertEqual(DayOfWeek.Sunday, 6)
    
    def testToString(self):
        e = DayOfWeek.Thursday
        self.assertEqual('Thursday', DayOfWeek.toString(e))
    
    def testParse(self):
        e = DayOfWeek.parse('sunday')
        self.assertEqual(e, DayOfWeek.Sunday)
    
    def testIterValues(self):
        vals = DayOfWeek.values
        self.assertEqual(len(vals), 7)
        self.assertIn(DayOfWeek.Monday, vals)
        self.assertIn(DayOfWeek.Sunday, vals)
    
    def testFlagsBasic(self):
        self.assertEqual(Caps.Read, 0x1)
        self.assertEqual(Caps.Delete, 0x8)
