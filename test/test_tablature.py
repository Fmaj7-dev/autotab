import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import unittest

import tablature

class TestTablature(unittest.TestCase):

  def test_add_incorrect(self):
    t = tablature.Tablature()
    t.addNote(8)
    t.addNote(8)
    t.addNote(10)
    t.addNote(10)
    t.addBar()
    t.addTime("1.2")

    t.addNote(17)
    t.addNote(25)
    t.addNote(17)
    t.addNote(24)
    t.addNote(20)
    t.addBar()
    t.addTime("2.4")

    t.addNote(25)
    
    self.assertEqual( t.getSize(), 0 )

  def test_add_correct(self):
    t = tablature.Tablature()
    
    for i in range(28, 68):
      t.addNote(i)

    t.print()

    self.assertEqual( t.getSize(), len(range(28, 68)) )

#if __name__ == '__main__':
suite = unittest.TestLoader().loadTestsFromTestCase(TestTablature)
unittest.TextTestRunner(verbosity=2).run(suite)
