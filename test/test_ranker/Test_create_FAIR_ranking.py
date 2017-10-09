'''
Created on Jan 18, 2017

@author: meike.zehlike
'''
import unittest
from dataset_creator.candidate import Candidate
from post_processing_methods.fair_ranker.create import fairRanking
from post_processing_methods.fair_ranker.test import FairnessInRankingsTester
from utilsAndConstants import constants


class Test_create_FAIR_rankings(unittest.TestCase):

    @classmethod
    def setUp(self):
        """
        creates k protected and k non-protected candidates into two arrays. Ordered by descending
        qualifications
        """
        self.__protectedCandidates = []
        self.__nonProtectedCandidates = []
        self.__k = 200

        for count in range(self.__k):
            protected = Candidate(count, ["female"])
            nonProtected = Candidate(count + self.__k, [])

            self.__nonProtectedCandidates.append(nonProtected)
            self.__protectedCandidates.append(protected)

        self.__nonProtectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)
        self.__protectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)


    @classmethod
    def tearDownClass(cls):
        super(Test_create_FAIR_rankings, cls).tearDownClass()


    def test_CreateFairRankingColorBlind(self):

        minProp = constants.ESSENTIALLY_ZERO
        sigma = 0.1
        ranking = fairRanking(self.__k, self.__protectedCandidates,
                                        self.__nonProtectedCandidates, minProp, sigma)[0]

        predecessor = ranking[0]
        self.assertFalse(predecessor.isProtected, "first one should be non-protected")
        for idx in range(1, len(ranking)):
            current = ranking[idx]
            self.assertFalse(current.isProtected, "all candidates should be non-protected")
            self.assertGreater(predecessor.originalQualification, current.originalQualification, "candidates should be ordered by qualification\
                failed at position {0}".format(idx))
            predecessor = current


    def test_CreateFairRankingOnlyProtected(self):
        minProp = constants.ESSENTIALLY_ONE
        sigma = 0.1
        ranking = fairRanking(self.__k, self.__protectedCandidates,
                                        self.__nonProtectedCandidates, minProp, sigma)[0]

        predecessor = ranking[0]
        self.assertTrue(predecessor.isProtected, "ranking should contain only protected")
        for idx in range(1, len(ranking)):
            current = ranking[idx]
            self.assertTrue(current.isProtected, "ranking should contain only protected")
            self.assertGreater(predecessor.originalQualification, current.originalQualification, "candidates should be ordered by qualification\
                failed at position {0}".format(idx))
            predecessor = current


    def test_CreateFairRankingHalfHalf(self):
        minProp = 0.5
        sigma = 0.1
        ranking = fairRanking(self.__k, self.__protectedCandidates,
                                        self.__nonProtectedCandidates, minProp, sigma)[0]

        tester = FairnessInRankingsTester(minProp, sigma, self.__k, False)

        predecessor = ranking[0]
        self.assertFalse(predecessor.isProtected, "first one should be non-protected")
        candidatesNeededAtLastIdx = tester.candidates_needed[0]
        for idx in range(1, len(ranking)):
            current = ranking[idx]
            if candidatesNeededAtLastIdx == tester.candidates_needed[idx]:
                # protected candidate should be inserted at each idx, at which the number of
                # needed protected candidates changes, otherwise should be the better one (for this
                # setting, not in general for the algorithm)
                self.assertFalse(current.isProtected)
            else:
                self.assertTrue(current.isProtected, "every candidate on even position should be protected")

            predecessor = current
            candidatesNeededAtLastIdx = tester.candidates_needed[idx]


    def test_CreateFairRankingSameQualification(self):
        # make all protected candidates having the same qualification as non-protected
        for candidate in self.__protectedCandidates:
            candidate.qualification += self.__k

        for idx, candidate in enumerate(self.__protectedCandidates):
            # ensure that both candidate pools have same qualifications
            self.assertEqual(candidate.qualification, self.__nonProtectedCandidates[idx].qualification)

        # no matter what minProp, we should see a ranking that alternates between protected and
        # non-protected
        minProp = 0.5
        sigma = 0.1
        ranking = fairRanking(self.__k, self.__protectedCandidates, self.__nonProtectedCandidates,
                                        minProp, sigma)[0]

        predecessor = ranking[0]
        self.assertTrue(predecessor.isProtected, "first one should be protected")

        for idx in range(1, len(ranking)):
            current = ranking[idx]
            if idx % 2 == 0:
                # protected candidate should appear on each odd position
                self.assertTrue(current.isProtected, "every candidate on odd position should be protected")
                self.assertGreater(predecessor.qualification, current.qualification, "if we see a \
                    protected candidate the above one should be non-protected and have a higher score")
            else:
                self.assertFalse(current.isProtected, "failed at position {0}".format(idx))
                self.assertEqual(predecessor.qualification, current.qualification, "if we see a non-\
                    protected candidate, the above should be protected and have the same qualification")
            predecessor = current









