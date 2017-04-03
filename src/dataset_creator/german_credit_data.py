'''
Created on Apr 3, 2017

@author: meike.zehlike
'''

import pandas as pd
from dataset_creator.candidate import Candidate


def createGermanCreditDataSet(filename, *columnsToRead, protectedAttribute):
    """
    currently working with pure score as qualification attribute in candidates. Change index
    to try with other columns

    dataset already normalized, therefore no normalization done
    """
    protected = []
    nonProtected = []
    with open(filename) as csvfile:
        data = pd.read_csv(csvfile, usecols=columnsToRead)
        identifier = 0
        for row in data.itertuples():
            # change to different index in row[.] to access other columns from csv file
            if row[4] == 0:
                nonProtected.append(Candidate(row['score'], [], identifier))
            else:
                protected.append(Candidate(row['score'], protectedAttribute, identifier))
            identifier += 1

    # sort candidates by credit scores in German Credit
    protected.sort(key=lambda candidate: candidate.qualification, reverse=True)
    nonProtected.sort(key=lambda candidate: candidate.qualification, reverse=True)

    return protected, nonProtected