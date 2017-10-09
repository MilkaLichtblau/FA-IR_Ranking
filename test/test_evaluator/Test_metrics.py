'''
Created on Jan 23, 2017

@author: meike.zehlike
'''
import unittest
from evaluator.metrics import selectionUtility, orderingUtility
from dataset_creator.candidate import Candidate


class TestMetrics(unittest.TestCase):
    """
    TODO: Beispiel aus Kommentar im src hier einbauen als test
    """

    def setUp(self):
        self.__fairRanking = self.__createFairRanking()
        self.__unfairRanking = self.__createUnfairRanking()


    def testSelectionUnfairness(self):
        notSelected = self.__unfairRanking[:500]
        ranking = []
        ranking.append(Candidate(1, ["female"]))
        self.assertEqual(-999, selectionUtility(ranking, notSelected))

        ranking[0] = Candidate(1001, ["female"])
        self.assertEqual(0, selectionUtility(ranking, notSelected), "no quality inversion, should\
                                        be therefore zero unfair")


    def testOrderingUnfairness(self):
        ranking1 = [Candidate(10, []),
                   Candidate(9, []),
                   Candidate(8, []),
                   Candidate(6, ["female"]),
                   Candidate(5, ["female"]),
                   Candidate(7, [])]

        self.assertEqual((2, -2), orderingUtility(ranking1))

        ranking2 = [Candidate(10, []),
                   Candidate(9, []),
                   Candidate(8, []),
                   Candidate(7, []),
                   Candidate(6, ["female"]),
                   Candidate(5, ["female"])]
        self.assertEqual((0, 0), orderingUtility(ranking2))

        ranking3 = [Candidate(1000, []),
                   Candidate(996, ["female"]),
                   Candidate(998, []),
                   Candidate(997, []),
                   Candidate(995, []),
                   Candidate(994, []),
                   Candidate(990, ["female"]),
                   Candidate(989, ["female"]),
                   Candidate(993, []),
                   Candidate(993, [])]
        self.assertEqual((2, -4), orderingUtility(ranking3))



    def __createFairRanking(self):
        fairRanking = []
        for i in range(1000, 0, -1):
            if i % 2 == 1:
                fairRanking.append(Candidate(i, ["Female"]))
            else:
                fairRanking.append(Candidate(i, []))
        return fairRanking


    def __createUnfairRanking(self):
        unfairRanking = []
        for i in range(1000, 500, -1):
            unfairRanking.append(Candidate(i, []))
        for i in range(500, 0, -1):
            unfairRanking.append(Candidate(i, ["Female"]))
        return unfairRanking



