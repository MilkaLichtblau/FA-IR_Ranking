'''
Created on Apr 26, 2017

@author: m.megahed
'''

import pandas as pd
from dataset_creator.candidate import Candidate


class Creator():
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

    @property
    def length(self):
        '''
        number of items in the data
        '''
        return self.__length

    @property
    def query_id(self):
        '''
        int with query id of these candidates
        '''
        return self.__query_id

    def __init__(self, path, protAttr, protAttrName):
        self.__data = pd.read_csv(path, sep=',', names=["query_id", "position", "score", "prot_attr"])
        self.__protectedCandidates = []
        self.__nonprotectedCandidates = []
        self.__length = self.__data.shape[0]
        # make sure there is only one query per file
        if len(self.__data["query_id"].unique()) != 1:
            print(self.__data["query_id"])
            raise ValueError
        self.__query_id = self.__data["query_id"][0]
        self.__separateGroups(protAttr, protAttrName)

    def __separateGroups(self, protAttr, protAttrName):
        '''
        separates data into two lists with protected and non-protected candidate objects

        @param protAttr: int, defines protection status
        @param protAttrName: string, defines protection status in words
        '''
        for _, row in self.__data.iterrows():
            stuffToSave = {
                    "query_id" : row["query_id"],
                    "position" : row["position"],
                }
            if row['prot_attr'] == protAttr:
                self.__protectedCandidates.append(Candidate(row['score'], [protAttrName], stuffToSave=stuffToSave))
            else:
                self.__nonprotectedCandidates.append(Candidate(row['score'], [], stuffToSave=stuffToSave))

        self.__protectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)
        self.__nonprotectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)

