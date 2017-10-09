'''
Created on Apr 3, 2017

@author: mzehlike
'''

#!/usr/bin/env python3 -tt
# -*- coding: utf-8 -*-

"""
Created on Jan 5, 2017

@author: meike.zehlike

"""
import PyPDF2 as pypdf
from utilsAndConstants.utils import Switch, normalizeQualifications
from dataset_creator.candidate import Candidate


class Creator(object):
    """
    loads a given PDF that contains a table of SAT _scores achieved by male and female students
    respectively. From that information a data set is created that contains as many protected and
    unprotected candidates for each score, as given in the table.

    For example: the table says that 327 male and 256 female students achieved a SAT score of 2400.
    Hence this test_simulation creates 327 non-protected candidates and 256 protected ones with a
    qualification criterion of 2400
    """

    _scores = []
    _number_nonprotected = []
    _number_protected = []

    def __init__(self, filename):

        tableContent = self.__loadSATPDF(filename)
        self.__writeContentIntoClassMembers(tableContent)


    def create(self):
        print("creating SAT candidate set")
        """
        creates the actual candidate objects such that the data set has the same distribution as
        given in the SAT table
        """
        protectedCandidates = []
        nonProtectedCandidates = []

        for index in range(len(self._scores)):
            print('.', end='', flush=True)
            score = self._scores[index]

            # create protected candidates of given score
            for i in range(self._number_protected[index]):
                protectedCandidates.append(Candidate(score, ["protected"]))

            # create non-protected candidates of given score
            for i in range(self._number_nonprotected[index]):
                nonProtectedCandidates.append(Candidate(score, []))

        normalizeQualifications(protectedCandidates + nonProtectedCandidates)

        protectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)
        nonProtectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)

        print(" [Done]")
        return protectedCandidates, nonProtectedCandidates


    def __loadSATPDF(self, filename):
        print("loading SAT score pdf")
        """
        loads the SAT PDF file, deletes all nonsense and creates an array containing only the numbers
        from the table

        Return
        ------
        All numbers from the SAT table in a string array
        """
        pdf = pypdf.PdfFileReader(open(filename, "rb"))
        tableContents = []

        for page in pdf.pages:
            content = page.extractText()
            tableHeader = "Total \nMale Female \nScore \nNumber Percentile Number Percentile Number Percentile "
            tableFooter = "De˜nitions of statistical terms are provided online at research."
            tableContents += self.__getTableContent(content, tableHeader, tableFooter)
            if "Number" and  "Mean" and "S.D." in tableContents:
                tableContents = tableContents[:tableContents.index("S.D.") - 2]

        return tableContents

    def __getTableContent(self, content, header, footer):
        """
        deletes all extra chars that are not numbers in the SAT table

        Return
        ------
        the pure table content of one single page from the SAT document, i.e. only the numbers
        """
        # deletes all 1˜ from the table content and writes a 0 for compatibility reasons
        # we don't need that number later on, not to worry
        content = content.replace('1˜', '0 ')
        tableStart = content.find(header) + len(header)
        tableEnd = content.find(footer)
        return content[tableStart:tableEnd].split()


    def __writeContentIntoClassMembers(self, tableContent):
        """
        takes the array of numbers from the SAT table and splits them into three arrays with respect to
        what the meaning of these numbers actually is
        """
        for index, number in enumerate(tableContent):
            numID = index % 7  # seven entries per line in the SAT file

            # remove useless chars
            if ',' in number or '+' in number or 'Š' in number:
                number = number.replace(',', '')
                number = number.replace('+', '.5')
                number = number.replace('Š', '0')

            # put numbers in their dedicated arrays
            for case in Switch(numID):
                if case(0):
                    # first column
                    self._scores.append(int(number))
                    break
                if case(1):
                    # second column
                    break
                if case(2):
                    # third column
                    break
                if case(3):
                    # fourth column
                    self._number_nonprotected.append(int(number))
                    break
                if case(4):
                    # fifth column
                    break
                if case(5):
                    # sixth column
                    self._number_protected.append(int(number))
                    break
                if case(6):
                    # seventh column
                    break
                if case():
                    raise ValueError("There should be only 7 data classes in the SAT table, \
                    corresponding to the above created arrays")

        # ensure that all lists are of the same length now
        if not ((len(self._scores) == len(self._number_protected)) and (len(self._number_protected) == len(self._number_nonprotected))):
            raise IndexError("All lists created from the SAT table should be of the same size")






