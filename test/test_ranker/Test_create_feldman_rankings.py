'''
Created on Feb 2, 2017

@author: meike.zehlike
'''
import unittest
from dataset_creator.candidate import Candidate
from post_processing_methods.fair_ranker.create import feldmanRanking


class Test_create_feldman_rankings(unittest.TestCase):


    def testCreateFeldmanRanking(self):
        """
        creates 500 protected candidates and 1000 non-protected candidates into two arrays, ordered
        by descending qualifications
        """
        protectedCandidates = []
        nonProtectedCandidates = []
        k = 500
        lastIndex = 0
        for i in range(1, k + 1):
            protectedCandidates.append(Candidate(i, ["female"]))
            lastIndex += 1

        for i in range(1, k + 1501):
            nonProtectedCandidates.append(Candidate(2 * i, []))
            lastIndex += 1

        protectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)
        nonProtectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)

        protectedForExpectedResult = protectedCandidates[:]
        nonProtectedForExpectedResult = nonProtectedCandidates[:]

        # build a result that looks like the one produced in this case
        expectedResult = []
        fiveNonProtectedInbetween = 4
        for i in range(k):
            if fiveNonProtectedInbetween == 4:
                expectedResult.append(protectedForExpectedResult.pop(0))
                fiveNonProtectedInbetween = 0
            else:
                expectedResult.append(nonProtectedForExpectedResult.pop(0))
                fiveNonProtectedInbetween += 1

        result = feldmanRanking(protectedCandidates, nonProtectedCandidates, k)[0]
        for candidate in result:
            candidate.qualification = int(candidate.qualification)

        expectedQualifications = [expectedResult[i].isProtected for i in range(len(expectedResult))]
        actualQualifications = [result[i].isProtected for i in range(len(result))]

        self.assertEqual(expectedQualifications, actualQualifications)


