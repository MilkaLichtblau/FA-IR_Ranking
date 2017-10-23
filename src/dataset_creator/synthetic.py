'''
Created on Oct 3, 2017

@author: meike.zehlike

'''
import numpy as np
import pandas as pd
import random, uuid
import itertools


class SyntheticDatasetCreator(object):

    """
    a dataframe that contains protected and non-protected features in columns. Each row represents
    a candidate with their feature values
    """
    @property
    def dataset(self):
        return self.__dataset


    """
    refers to possible combinations of protected attributes. Each group is an element of the Cartesian
    product of the element set per protected attribute.
    example:   attribute gender has two possible elements {0, 1}, attribute ethnicity has three
               possible elements {0, 1, 2} --> there are six groups
               a group is determined by one of the tuples (0, 0), (0,1), (1, 0), ..., (2, 1)
    the non-protected group is always represented by the tuple with only zeros
    """
    @property
    def groups(self):
        return self.__groups


    def __init__(self, size, attributeNamesAndCategories, nonProtectedAttributes):
        """
        TODO: Parameter description
        mu and sigma as parameters
        """
        self.__dataset = pd.DataFrame()

        # determine groups of candidates
        self.__determineGroups(attributeNamesAndCategories)

        # generate distribution of protected attributes
        self.__createCategoricalProtectedAttributes(attributeNamesAndCategories, size)

        # generate scores per group
        self.__createScoresNormalDistribution(nonProtectedAttributes)

        # generate ID column
        # self.__dataset['uuid'] = uuid.uuid4()



    def writeToJSON(self, path):
        self.__dataset.to_json(path, orient='records', lines=True)


    def __determineGroups(self, attributeNamesAndCategories):
        elementSets = []
        for attr, cardinality in attributeNamesAndCategories.items():
            elementSets.append(list(range(0, cardinality)))

        self.__groups = list(itertools.product(*elementSets))


    def __createScoresNormalDistribution(self, nonProtectedAttributes):
        """
        @param nonProtectedAttributes:     a string array that contains the names of the non-protected
                                           features
        @param mu:                         float array that contains means of the expected scores. Its
                                           length should match the length of 'nonProtectedAttributes'
        @param sigma:                      float array that contains standard deviations of the
                                           expected scores. Its length should match the length of
                                           'nonProtectedAttributes'
        """
        # if len(mu_diff) != len(nonProtectedAttributes) or len(sigma_diff) != len(nonProtectedAttributes):
        #    raise ValueError("lengths of arrays nonProtectedAttributes, mu_diff and sigma_diff have to match")

        def score(x, colName):
            mu = np.random.uniform()
            sigma = np.random.uniform()
            x[colName] = np.random.normal(mu, sigma, size=len(x))
            return x

        for attr in nonProtectedAttributes:
            self.__dataset = self.__dataset.groupby(self.__dataset.columns.tolist(), as_index=False,
                                                    sort=False).apply(score, (attr))


    def __createCategoricalProtectedAttributes(self, attributeNamesAndCategories, numItems):
        """
        @param attributeNamesAndCategories:         a dictionary that contains the names of the
                                                    protected attributes as keys and the number of
                                                    categories as values
                                                    (e.g. {('ethnicity'; 5), ('gender'; 2)})
        @param numItems:                            number of items in entire created dataset (all
                                                    protection status)

        @return category zero is assumed to be the non-protected
        """
        newData = pd.DataFrame(columns=attributeNamesAndCategories.keys())

        for attributeName in attributeNamesAndCategories.keys():
            col = []
            categories = range(0, attributeNamesAndCategories[attributeName])
            for count in range(0, numItems):
                col.append(random.choice(categories))
            newData[attributeName] = col

        # add protected columns to dataset
        self.__dataset = self.__dataset.append(newData)

