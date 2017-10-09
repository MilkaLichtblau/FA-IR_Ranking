'''
Created on Jan 7, 2017

@author: meike.zehlike
'''
import unittest
from dataset_creator.yangStoyanovichMethod import generateCandidateList, create


class TestYangStoyanovichSimulation(unittest.TestCase):

    def test_generateCandidateList(self):

        candidates = generateCandidateList(True, 123456)
        self.assertEqual(123456, len(candidates), "candidate list should have 123456 elements")
        self.assertTrue(candidates[0].isProtected, "candidates should be created protected")

        candidates = generateCandidateList(False, 1234)
        self.assertEqual(1234, len(candidates), "candidate list should have 1234 elements")
        self.assertFalse(candidates[0].isProtected, "candidates should be created protected")

    def test_simulate(self):

        # a half protected, half non-protected result list should be produced here
        rankedCandidates = create(0.5, 1500, 1000, 1000)
        self.assertEqual(1500, len(rankedCandidates), "output should have k=1500 elements")
        protected, nonProtected = self.separateProtectedFromUnprotected(rankedCandidates)
        self.assertAlmostEqual(len(protected), len(nonProtected), msg="protected and nonprotected \
            candidates should be more or less equally distributed", delta=50)

        # a protected candidate is always to be preferred, should therefor result in a list with
        # 1000 protected candidates at the top followed by 500 non-protected
        rankedCandidates = create(1, 1500, 1000, 1000)
        self.assertEqual(1500, len(rankedCandidates), "output should have k=1500 elements")
        for idx in range(1000 - 1):
            self.assertTrue(rankedCandidates[idx].isProtected, "the first 1000 candidates should be \
            protected")
        for idx in range(1000, 1499):
            self.assertFalse(rankedCandidates[idx].isProtected, "the last 500 candidates should be \
            non-protected, because after all protected candidates are in the result list, the \
            remaining positions are filled with non-protected")

        # a non-protected candidate is always to be preferred, should therefor result in a list with
        # 1000 non-protected candidates at the top followed by 500 protected
        rankedCandidates = create(0, 1500, 1000, 1000)
        self.assertEqual(1500, len(rankedCandidates), "output should have k=1500 elements")
        for idx in range(1000 - 1):
            self.assertFalse(rankedCandidates[idx].isProtected, "the first 1000 candidates should be \
            non-protected")
        for idx in range(1000, 1499):
            self.assertTrue(rankedCandidates[idx].isProtected, "the last 500 candidates should be \
            protected, because after all non-protected candidates are in the result list, the \
            remaining positions are filled with protected")


    def separateProtectedFromUnprotected(self, rankedCandidates):
        protected = []
        nonProtected = []
        for candidate in rankedCandidates:
            if candidate.isProtected:
                protected.append(candidate)
            else:
                nonProtected.append(candidate)
        return protected, nonProtected

