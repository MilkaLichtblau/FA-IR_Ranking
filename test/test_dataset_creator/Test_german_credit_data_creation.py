'''
Created on Apr 3, 2017

@author: meike.zehlike
'''
import unittest
from dataset_creator import germanCreditData
from utilsAndConstants.utils import countProtected


class Test(unittest.TestCase):

    def testGermanCreditDataCreation(self):
        protected, nonProtected = germanCreditData.create("test_dataset_creator/GermanCredit_sex.csv", "DurationMonth", "CreditAmount",
                                                          "score", "sex", protectedAttribute=["female"])
        self.assertEqual(310, len(nonProtected), "should have 310 males")
        self.assertEqual(0, countProtected(nonProtected), "the nonProtected array should not contain protected candidates")
        self.assertAlmostEqual(0.744449197, nonProtected[0].originalQualification, places=9,
                               msg="best non-protected candidate has wrong score")
        self.assertEqual(690, len(protected), "should have 690 females")
        self.assertEqual(690, countProtected(protected), "the protected ranking should contain only protected candidates")
        self.assertAlmostEqual(0.790280217, protected[0].originalQualification, places=9,
                               msg="best protected candidate has wrong score")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
