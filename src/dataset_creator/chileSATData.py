'''
Created on Apr 26, 2017

@author: m.megahed
'''

#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

import pandas as pd
from utilsAndConstants.utils import Switch, normalizeQualifications
from dataset_creator.candidate import Candidate




def createSchool(filename, *columnsToRead):
    """
    currently working with _________ as qualification attribute in candidates. Change index
    to try with other columns
    """
    nonProtected = []
    protected = []
    with open(filename) as csvfile:
        data = pd.read_csv(csvfile, usecols=columnsToRead)
        for row in data.itertuples():
            # change to different index in row[.] to access other columns from csv file
            if row[45] == (1 or 2):
                nonProtected.append(Candidate(1 - row[44], []))
            elif row[45] == 3:
                protected.append(Candidate(1 - row[44], ["private_school"]))
            else:
                continue

    # sort candidates by recidivism scores in COMPAS
    protected.sort(key=lambda candidate: candidate.qualification, reverse=True)
    nonProtected.sort(key=lambda candidate: candidate.qualification, reverse=True)

    return protected, nonProtected


def createNationality(filename, *columnsToRead):
    """
    currently working with recidivism score as qualification attribute in candidates. Change index
    to try with other columns
    """
    nonProtected = []
    protected = []
    with open(filename) as csvfile:
        data = pd.read_csv(csvfile, usecols=columnsToRead)
        for row in data.itertuples():
            # change to different index in row[.] to access other columns from csv file
            if row[2] == 1:
                nonProtected.append(Candidate(1 - row[1], []))
            else:
                protected.append(Candidate(1 - row[1], ["foreigner"]))

    # sort candidates by ____ scores in chileSAT
    protected.sort(key=lambda candidate: candidate.qualification, reverse=True)
    nonProtected.sort(key=lambda candidate: candidate.qualification, reverse=True)

    return protected, nonProtected

