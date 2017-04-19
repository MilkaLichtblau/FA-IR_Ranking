'''
Created on 23.12.2016

@author: meike.zehlike
'''
import uuid

class Candidate(object):
    """
    represents a candidate in a set that is passed to a search algorithm
    a candidate composes of a qualification and a list of protected attributes (strings)
    if the list of protected attributes is empty/null this is a candidate from a non-protected group
    natural ordering established by the qualification
    """


    def __init__(self, qualification, protectedAttributes):
        """
        @param qualification : describes how qualified the candidate is to match the search query
        @param protectedAttributes: list of strings that represent the protected attributes this
                                    candidate has (e.g. gender, race, etc)
                                    if the list is empty/null this is a candidate from a non-protected group
        """
        self.__qualification = qualification
        self.__protectedAttributes = protectedAttributes
        # keeps the candidate's initial qualification for evaluation purposes
        self.__originalQualification = qualification
        self.uuid = uuid.uuid4()


    @property
    def qualification(self):
        return self.__qualification


    @qualification.setter
    def qualification(self, value):
        self.__qualification = value


    @property
    def originalQualification(self):
        return self.__originalQualification


    @originalQualification.setter
    def originalQualification(self, value):
        self.__originalQualification = value


    @property
    def isProtected(self):
        '''
        true if the list of ProtectedAttribute elements actually contains anything
        false otherwise
        '''
        return not self.__protectedAttributes == []



























