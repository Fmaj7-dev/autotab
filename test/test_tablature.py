import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import unittest

import tablature

class TestTablature(unittest.TestCase):

  def test_add(self):
    t = tablature.Tablature()
    t.addNote(8)
    t.addNote(8)
    t.addNote(10)
    t.addNote(10)
    t.print()

    self.assertEqual( 1, 1 )

#if __name__ == '__main__':
suite = unittest.TestLoader().loadTestsFromTestCase(TestTablature)
unittest.TextTestRunner(verbosity=2).run(suite)
