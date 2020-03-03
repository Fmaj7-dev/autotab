import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import dataset
import unittest

class TestDataset(unittest.TestCase):

  def test_readwrite(self):
    d = dataset.DataSet()
    d.createFromAudioFiles( "../../guitar_dataset/dataset/" )
    d.save("database.db")

    d2 = dataset.DataSet()
    d2.load("database.db")

    self.assertEqual( d.getNumSamples(), d2.getNumSamples() )

  def test_x(self):
    self.assertEqual(3, 3)

#if __name__ == '__main__':
suite = unittest.TestLoader().loadTestsFromTestCase(TestDataset)
unittest.TextTestRunner(verbosity=2).run(suite)

os.remove("database.db")
