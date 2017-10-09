'''
Created on Jan 9, 2017

@author: meike.zehlike
'''
import unittest
from dataset_creator.satData import Creator
from dataset_creator.candidate import Candidate

class TestSATDataSetSimulation(unittest.TestCase):
    filename = "../rawData/SAT/sat_data.pdf"
    creator = Creator(filename)

    def test_constructor(self):
        self.assertEqual(181, len(self.creator._scores), "_scores should have 181 entries as has the \
            SAT testfile")
        self.assertEqual(2400, self.creator._scores[0], "first element of _scores should contain the \
            highest SAT score")
        self.assertEqual(2390, self.creator._scores[1], "second element of _scores should contain the \
            second highest SAT score")
        self.assertEqual(600, self.creator._scores[180], "last element of _scores should contain the \
            lowest SAT score")

        self.assertEqual(181, len(self.creator._number_nonprotected), "_numberMales should have 181 entries \
            as has the SAT testfile")
        self.assertEqual(327, self.creator._number_nonprotected[0], "first element of _numberMales should \
            contain the first table entry of the SAT file")
        self.assertEqual(181, len(self.creator._number_protected), "_numberFemales should have 181 entries \
            as has the SAT testfile")
        self.assertEqual(256, self.creator._number_protected[0], "first element of _numberFemales should \
            contain the first table entry of the SAT file")

    def test_createSetOfCandidates(self):
        protected, nonProtected = self.creator.create()

        self.assertEqual(888825, len(protected), "should have created same number of female candidates \
            as in the SAT file")
        self.assertEqual(783570, len(nonProtected), "should have created same number of male candidates \
            as in the SAT file")

        self.assertIsInstance(protected[0], Candidate, "only Candidates should be created")
        self.assertIsInstance(nonProtected[0], Candidate, "only Candidates should be created")

        for i in range(255):
            self.assertEqual(1.0, protected[i].originalQualification, "the first 256 female candidates \
                should have the highest SAT score, failed at position {0}".format(i))

        self.assertEqual(0.9958333333333333, protected[256].originalQualification, "the 257th female candidate \
                should have the second highest SAT score")


        for i in range(326):
            self.assertEqual(1.0, nonProtected[i].originalQualification, "the first 327 male candidates \
                should have the highest SAT score, failed at position {0}".format(i))

        self.assertEqual(0.9958333333333333, nonProtected[327].originalQualification, "the 328th male candidate \
                should have the second highest SAT score")







