'''
Created on Apr 3, 2017

@author: meike.zehlike
'''
import unittest
from dataset_creator import compasData
from utilsAndConstants.utils import countProtected


class Test(unittest.TestCase):


    def testDatasetCreationRace(self):
        # the csv file contains 310 male persons and 690 female
        protected, nonProtected = compasData.createRace("test_dataset_creator/ProPublica_race.csv", "race", "Violence_rawscore", "Recidivism_rawscore",
       "priors_count")
        self.assertEqual(3361, len(nonProtected), "should have 3361 non-blacks")
        self.assertEqual(0, countProtected(nonProtected), "the nonProtected array should not contain protected candidates")
        # for COMPAS we take the negativ recidivism score
        self.assertEqual(1 - 0, nonProtected[0].originalQualification, "best non-protected candidate has wrong score")
        self.assertEqual(3528, len(protected), "should have 3528 blacks")
        self.assertEqual(3528, countProtected(protected), "the protected ranking should contain only protected candidates")
        # for COMPAS we take the negativ recidivism score
        self.assertEqual(1 - 0.012793177, protected[0].originalQualification, "best protected candidate has wrong score")


    def testDatasetCreationGender(self):
        # the csv file contains 5561 male persons and 1328 female
        protected, nonProtected = compasData.createGender("test_dataset_creator/ProPublica_sex.csv", "sex", "Violence_rawscore", "Recidivism_rawscore",
       "priors_count")
        self.assertEqual(1328, len(protected), "should have 1328 females")
        self.assertEqual(1328, countProtected(protected), "the nonProtected array should not contain protected candidates")
        # for COMPAS we take the negativ recidivism score
        self.assertEqual(1 - 0.038379531, protected[0].originalQualification, "best non-protected candidate has wrong score")
        self.assertEqual(5561, len(nonProtected), "should have 5561 males")
        self.assertEqual(0, countProtected(nonProtected), "the protected ranking should contain only protected candidates")
        # for COMPAS we take the negativ recidivism score
        self.assertEqual(1 - 0, nonProtected[0].originalQualification, "best protected candidate has wrong score")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
