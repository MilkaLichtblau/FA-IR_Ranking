'''
Created on Oct 9, 2017

@author: meike.zehlike
'''
import unittest
import numpy as np
from dataset_creator.synthetic import SyntheticDatasetCreator

class TestSyntheticDatasetCreator(unittest.TestCase):
    size = 100000
    creator = SyntheticDatasetCreator(size, {"gender": 2, "ethnicity": 3, "disability": 2}, ["score"])

    def test_constructor(self):
        self.assertTrue("gender" in self.creator.dataset.columns)
        self.assertTrue("ethnicity" in self.creator.dataset.columns)
        self.assertTrue("disability" in self.creator.dataset.columns)
        self.assertTrue("score" in self.creator.dataset.columns)

        self.assertEqual((self.size, 4), self.creator.dataset.shape)
        self.assertEqual(12, len(self.creator.groups))

        expectedGroups = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 2, 0), (0, 2, 1), (1, 0, 0),
                          (1, 0, 1), (1, 1, 0), (1, 1, 1), (1, 2, 0), (1, 2, 1)]
        self.assertCountEqual(expectedGroups, self.creator.groups)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
