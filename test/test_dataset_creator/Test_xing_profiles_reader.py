'''
Created on Mar 15, 2017
'''

import unittest
from dataset_creator.xingProfilesReader import Reader


class Test(unittest.TestCase):

    def testReadFemaleDominant(self):
        data = Reader('test_dataset_creator/femaleDominant.json')
        df = data.entireDataSet

        # check shape is 1 row, 3 columns
        self.assertEqual((1, 3), df.shape, "female dominant data frame has wrong shape")

        # check that row is called like search query
        self.assertTrue("Administrative Assistant" in df.index)

        # check that columns protected, nonProtected and originalOrdering
        self.assertTrue("protected" in df.columns)
        self.assertTrue("nonProtected" in df.columns)
        self.assertTrue("originalOrdering" in df.columns)

        # check that protected column contains protected candidates
        protected = df.iloc[0]['protected']
        self.assertEqual(7, len(protected), "should have 7 candidates")
        self.assertEqual(7, self.__countProtected(protected), "all candidates should be protected")

        # check that non-protected column contains non-protected candidates
        nonProtected = df.iloc[0]['nonProtected']
        self.assertEqual(33, len(nonProtected), "should have 33 candidates")
        self.assertEqual(0, self.__countProtected(nonProtected), "all candidates should be non-protected")

        # check that original ordering column contains all candidates
        origOrder = df.iloc[0]['originalOrdering']
        self.assertEqual(40, len(origOrder), "should have 40 candidates")
        self.assertEqual(7, self.__countProtected(origOrder), "33 candidates should be protected")


    def testReadMaleDominant(self):
        data = Reader('test_dataset_creator/maleDominant.json')
        df = data.entireDataSet

        # check shape is 1 row, 3 columns
        self.assertEqual((1, 3), df.shape, "male dominant data frame has wrong shape")

        # check that row is called like search query
        self.assertTrue("bank teller" in df.index)

        # check that columns protected, nonProtected and originalOrdering
        self.assertTrue("protected" in df.columns)
        self.assertTrue("nonProtected" in df.columns)
        self.assertTrue("originalOrdering" in df.columns)

        # check that protected column contains protected candidates
        protected = df.iloc[0]['protected']
        self.assertEqual(16, len(protected), "should have 16 candidates")
        self.assertEqual(16, self.__countProtected(protected), "all candidates should be protected")

        # check that non-protected column contains non-protected candidates
        nonProtected = df.iloc[0]['nonProtected']
        self.assertEqual(24, len(nonProtected), "should have 24 candidates")
        self.assertEqual(0, self.__countProtected(nonProtected), "all candidates should be non-protected")

        # check that original ordering column contains all candidates
        origOrder = df.iloc[0]['originalOrdering']
        self.assertEqual(40, len(origOrder), "should have 40 candidates")
        self.assertEqual(16, self.__countProtected(origOrder), "16 candidates should be protected")


    def testReadGenderNeutral(self):
        data = Reader('test_dataset_creator/genderNeutral.json')
        df = data.entireDataSet

        # check shape is 1 row, 3 columns
        self.assertEqual((1, 3), df.shape, "male dominant data frame has wrong shape")

        # check that row is called like search query
        self.assertTrue("statistician" in df.index)

        # check that columns protected, nonProtected and originalOrdering
        self.assertTrue("protected" in df.columns)
        self.assertTrue("nonProtected" in df.columns)
        self.assertTrue("originalOrdering" in df.columns)

        # check that protected column contains protected candidates
        protected = df.iloc[0]['protected']
        self.assertEqual(18, len(protected), "should have 18 candidates")
        self.assertEqual(18, self.__countProtected(protected), "all candidates should be protected")

        # check that non-protected column contains non-protected candidates
        nonProtected = df.iloc[0]['nonProtected']
        self.assertEqual(22, len(nonProtected), "should have 22 candidates")
        self.assertEqual(0, self.__countProtected(nonProtected), "all candidates should be non-protected")

        # check that original ordering column contains all candidates
        origOrder = df.iloc[0]['originalOrdering']
        self.assertEqual(40, len(origOrder), "should have 40 candidates")
        self.assertEqual(18, self.__countProtected(origOrder), "18 candidates should be protected")


    def testReadAll(self):
        data = Reader('test_dataset_creator/*.json')
        df = data.entireDataSet

        # check shape is 3 row, 3 columns
        self.assertEqual((3, 3), df.shape, "reading all data results in data frame having wrong shape")

        # check that row is called like search query
        self.assertTrue("statistician" in df.index)
        self.assertTrue("bank teller" in df.index)
        self.assertTrue("Administrative Assistant" in df.index)

        # check that columns protected, nonProtected and originalOrdering
        self.assertTrue("protected" in df.columns)
        self.assertTrue("nonProtected" in df.columns)
        self.assertTrue("originalOrdering" in df.columns)


    def __countProtected(self, ranking):
        result = 0
        for candidate in ranking:
            if candidate.isProtected:
                result += 1
        return result


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
