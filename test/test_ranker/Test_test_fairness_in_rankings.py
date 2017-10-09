'''
Created on Jan 13, 2017

@author: meike.zehlike
'''
import unittest
from dataset_creator.candidate import Candidate
from post_processing_methods.fair_ranker.test import FairnessInRankingsTester

class Test_test_fairness_in_rankings(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        creates 20 protected and 20 non-protected candidates and ranks them into 3 rankings:
        - one that contains only protected candidates
        - one that contains only non-protected
        - one that alternates between a protected and a non-protected, starting with a protected
          candidate at position 0
        """
        cls.__fairRankingHalfHalf = []
        cls.__unfairRankingOnlyNonProtected = []
        cls.__unfairRankingOnlyProtected = []

        for count in range(20):
            protected = Candidate(count, ["female"])
            nonProtected = Candidate(count, [])

            cls.__unfairRankingOnlyNonProtected.append(nonProtected)
            cls.__unfairRankingOnlyProtected.append(protected)

            # put a protected candidate each even round, a nonProtected each odd round
            if count % 2:
                cls.__fairRankingHalfHalf.append(protected)
            else:
                cls.__fairRankingHalfHalf.append(nonProtected)


    @classmethod
    def tearDownClass(cls):
        super(Test_test_fairness_in_rankings, cls).tearDownClass()


    def test_fairRepresentationCondition(self):
        tester = FairnessInRankingsTester(0.5, 0.1, len(self.__fairRankingHalfHalf), False)

        self.assertTrue(tester.fair_representation_condition(self.__fairRankingHalfHalf))
        self.assertTrue(tester.fair_representation_condition(self.__unfairRankingOnlyProtected),
                        "we ensure that there are AT LEAST 50% protected candidates, not approximately 50%")
        self.assertFalse(tester.fair_representation_condition(self.__unfairRankingOnlyNonProtected),
                         "if there are less than 50% protected candidates in the ranking, should return False")

        # we expect a minimal proportion of protected candidates of 100%, however the set only contains
        # 50% of protected candidates
        tester = FairnessInRankingsTester(1, 0.1, len(self.__fairRankingHalfHalf), False)

        self.assertFalse(tester.fair_representation_condition(self.__fairRankingHalfHalf))
        self.assertTrue(tester.fair_representation_condition(self.__unfairRankingOnlyProtected),
                        "contains only protected candidates, so each minimal proportion should be sufficient")
        self.assertFalse(tester.fair_representation_condition(self.__unfairRankingOnlyNonProtected),
                         "if there are less than 50% protected candidates in the ranking, should return False")

        # we don't expect a single protected candidate, so this should accept all sets
        tester = FairnessInRankingsTester(0, 0.1, len(self.__fairRankingHalfHalf), False)

        self.assertTrue(tester.fair_representation_condition(self.__fairRankingHalfHalf))
        self.assertTrue(tester.fair_representation_condition(self.__unfairRankingOnlyProtected),
                        "contains only protected candidates, so each minimal proportion should be sufficient")
        self.assertTrue(tester.fair_representation_condition(self.__unfairRankingOnlyNonProtected),
                        "if there are less than 50% protected candidates in the ranking, should return False")


    def test_rankedGroupFairnessCondition(self):
        tester = FairnessInRankingsTester(0.5, 0.1, len(self.__fairRankingHalfHalf), False)

        pos, isFair = tester.ranked_group_fairness_condition(self.__fairRankingHalfHalf)
        self.assertTrue(isFair, "Test MinProp: {0} => half half ranking became unfair at position \
            {1}".format(tester.minimal_proportion, pos))
        pos, isFair = tester.ranked_group_fairness_condition(self.__unfairRankingOnlyProtected)
        self.assertTrue(isFair, "Test MinProp: {0} => ranking with only protected became unfair at \
            position {1}".format(tester.minimal_proportion, pos))
        pos, isFair = tester.ranked_group_fairness_condition(self.__unfairRankingOnlyNonProtected)
        self.assertFalse(isFair, "Test MinProp: {0} => ranking with only non-protected became unfair \
            at position {1}".format(tester.minimal_proportion, pos))

        # we expect a minimal proportion of protected candidates of 100%, however the set only contains
        # 50% of protected candidates
        tester = FairnessInRankingsTester(1, 0.1, len(self.__fairRankingHalfHalf), False)

        pos, isFair = tester.ranked_group_fairness_condition(self.__fairRankingHalfHalf)
        self.assertFalse(isFair, "Test MinProp: {0} => half half ranking should be unfair at each \
            position for this minimal proportion".format(tester.minimal_proportion))
        pos, isFair = tester.ranked_group_fairness_condition(self.__unfairRankingOnlyProtected)
        self.assertTrue(isFair, "Test MinProp: {0} => ranking with only protected became unfair at \
            position {1}".format(tester.minimal_proportion, pos))
        pos, isFair = tester.ranked_group_fairness_condition(self.__unfairRankingOnlyNonProtected)
        self.assertFalse(isFair, "Test MinProp: {0} => ranking with only non-protected became unfair \
            at position {1}".format(tester.minimal_proportion, pos))

        # we don't expect a single protected candidate, so this should accept all sets
        tester = FairnessInRankingsTester(0, 0.1, len(self.__fairRankingHalfHalf), False)

        pos, isFair = tester.ranked_group_fairness_condition(self.__fairRankingHalfHalf)
        self.assertTrue(isFair, "Test MinProp: {0} => half half ranking became unfair at position \
            {1}".format(tester.minimal_proportion, pos))
        pos, isFair = tester.ranked_group_fairness_condition(self.__unfairRankingOnlyProtected)
        self.assertTrue(isFair, "Test MinProp: {0} => ranking with only protected became unfair at \
            position {1}".format(tester.minimal_proportion, pos))
        pos, isFair = tester.ranked_group_fairness_condition(self.__unfairRankingOnlyNonProtected)
        self.assertTrue(isFair, "Test MinProp: {0} => ranking with only non-protected became unfair \
            at position {1}".format(tester.minimal_proportion, pos))


    def test_CandidatesNeededAtPosition(self):
        expected0 = [0] * 10
        expected20 = [0] * 10
        expected30 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        expected40 = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2]
        expected50 = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3]
        expected100 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        gft = FairnessInRankingsTester(0, 0.1, 10, False)
        self.assertEqual(expected0, gft.candidates_needed)

        gft = FairnessInRankingsTester(0.2, 0.1, 10, False)
        self.assertEqual(expected20, gft.candidates_needed)

        gft = FairnessInRankingsTester(0.3, 0.1, 10, False)
        self.assertEqual(expected30, gft.candidates_needed)

        gft = FairnessInRankingsTester(0.4, 0.1, 10, False)
        self.assertEqual(expected40, gft.candidates_needed)

        gft = FairnessInRankingsTester(0.5, 0.1, 10, False)
        self.assertEqual(expected50, gft.candidates_needed)

        gft = FairnessInRankingsTester(1, 0.1, 10, False)
        self.assertEqual(expected100, gft.candidates_needed)


