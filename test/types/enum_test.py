from hk2.types import enum, flags, flags_seq

import unittest

#===========================================================

@enum
class DayOfWeek(object):
    Monday, Tuesday, Wednesday, \
    Thursday, Friday, Saturday, Sunday = range(7)

#===========================================================

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

#===========================================================

@flags
class Caps(object):
    Empty = 0x0
    Read, Write, Create, Delete = flags_seq(4)
    All = 0xff

#===========================================================

class TestFlagsEnum(unittest.TestCase):
    def testFlagsBasic(self):
        self.assertEqual(Caps.Read, 0x1)
        self.assertEqual(Caps.Delete, 0x8)
    
    def testToStringSingle(self):
        c = Caps.toString(Caps.Write)
        self.assertEqual(c, 'Write')
    
    def testToStringMulti(self):
        c = Caps.toString(Caps.Read | Caps.Write)
        self.assertEqual(c, 'Read | Write')
        
        c = Caps.toString(Caps.Empty)
        self.assertEqual(c, 'Empty')
        
        c = Caps.toString(Caps.All)
        self.assertEqual(c, 'All')
    
    def testParseSingle(self):
        c = Caps.parse('write')
        self.assertEqual(c, Caps.Write)
    
    def testParseMulti(self):
        c = Caps.parse('write|read | delete')
        self.assertEqual(c, Caps.Read | Caps.Write | Caps.Delete)




