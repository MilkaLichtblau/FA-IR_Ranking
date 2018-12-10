'''
Created on Apr 26, 2017

@author: m.megahed
'''

import pandas as pd
from dataset_creator.candidate import Candidate


class ChileSatCreator():
    '''
    TODO: write doc
    '''

    @property
    def protectedCandidates(self):
        '''
        list with protected candidate objects
        '''
        return self.__protectedCandidates

    @property
    def nonprotectedCandidates(self):
        '''
        list with non-protected candidate objects
        '''
        return self.__nonprotectedCandidates

    def __init__(self, path, protAttr, protAttrName):
        self.__data = pd.read_csv(path, sep=',', names=["query_id", "ranking_position", "score", "prot_attr"])
        self.__protectedCandidates = []
        self.__nonprotectedCandidates = []
        self.__separateGroups(protAttr, protAttrName)

    def __separateGroups(self, protAttr, protAttrName):
        '''
        separates data into two lists with protected and non-protected candidate objects

        @param protAttr: int, defines protection status
        '''
        for _, row in self.__data.iterrows():
            if row['prot_attr'] == protAttr:
                self.__protectedCandidates.append(Candidate(row['score'], [protAttrName]))
            else:
                self.__nonprotectedCandidates.append(Candidate(row['score'], []))

        self.__protectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)
        self.__nonprotectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)

