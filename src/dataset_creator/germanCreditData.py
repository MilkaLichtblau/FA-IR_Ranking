'''
Created on Apr 3, 2017

@author: meike.zehlike
'''

import pandas as pd
from dataset_creator.candidate import Candidate


def create(filename, *columnsToRead, protectedAttribute):
    """
    currently working with credit worthiness score as qualification attribute in candidates. Change column index in data frame
    to try with other columns

    dataset already normalized, therefore no normalization done
    """
    protected = []
    nonProtected = []
    with open(filename) as csvfile:
        data = pd.read_csv(csvfile, usecols=columnsToRead)
        for row in data.itertuples():
            # change to different index in row[.] to access other columns from csv file
            if row[4] == 0:
                nonProtected.append(Candidate(row[3], []))
            else:
                protected.append(Candidate(row[3], protectedAttribute))

    # sort candidates by credit scores in German Credit
    protected.sort(key=lambda candidate: candidate.qualification, reverse=True)
    nonProtected.sort(key=lambda candidate: candidate.qualification, reverse=True)

    return protected, nonProtected