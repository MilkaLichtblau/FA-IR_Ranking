"""
Created on 1.2.2016

@author: mohamed.megahed
"""

import json
import glob
import datetime
import math
import pandas as pd
import pickle

from dataset_creator.candidate import Candidate
from utilsAndConstants.utils import normalizeQualifications


class Reader(object):
    """
    reads profiles collected from Xing on certain job description queries
    profiles are available in JSON format
    they are read into a data frame indexed by the search queries we used to obtain candidate profiles

    the columns consists of arrays of Candidates, the protected ones, the non-protected ones and
    one that contains all candidates in the same order as was collected from Xing website.

                             |          PROTECTED            |            NON-PROTECTED            |       ORIGINAL ORDERING
    Administrative Assistant | [protected1, protected2, ...] | [nonProtected1, nonProtected2, ...] | [nonProtected1, protected1, ...]
    Auditor                  | [protected3, protected4, ...] | [nonProtected3, nonProtected3, ...] | [protected4, nonProtected3, ...]
            ...              |            ...                |               ...                   |             ...


    the protected attribute of a candidate is their sex
    a candidate's sex was manually determined from the profile name
    depending on the dominating sex of a search query result, the other one was set as the protected
    attribute (e.g. for administrative assistant the protected attribute is male, for auditor it's female)
    """

    EDUCATION_OR_JOB_WITH_NO_DATES = 3  # months count if you had a job that has no associated dates
    EDUCATION_OR_JOB_WITH_SAME_YEAR = 6  # months count if you had a job that started and finished in the same year
    EDUCATION_OR_JOB_WITH_UNDEFINED_DATES = 1  # month given that the person entered the job

    @property
    def entireDataSet(self):
        return self.__entireDataSet


    def __init__(self, path):
        """
        @param path: path to JSON files with Xing data
        """
        self.__entireDataSet = pd.DataFrame(columns=['protected', 'nonProtected', 'originalOrdering'])

        files = glob.glob(path)

        for filename in files:
            key, protected, nonProtected, origOrder = self.__readFileOfQuery(filename)
            self.__entireDataSet.loc[key] = [protected, nonProtected, origOrder]


    def dumpDataSet(self, pathToFile):
        with open(pathToFile, 'wb') as handle:
            pickle.dump(self.__entireDataSet, handle, protocol=pickle.HIGHEST_PROTOCOL)


    def __readFileOfQuery(self, filename):
        """
        takes one .json file and reads all information, creates candidate objects from these
        information and sorts them into 3 arrays. One contains all protected candidates, one contains
        all non-protected candidates, one contains all candidates in the same order as they appear
        in the json-file

        @param filename: the json's filename

        @return:
            key: the search query string
            protected: array that contains all protected candidates
            nonProtected: array that contains all nonProtected candidates

        """
        protected = []
        nonProtected = []
        originalOrdering = []

        currentfile = open(filename)
        data = json.load(currentfile)

        xingSearchQuery = data['category']
        # if the Xing search query results in a gender neutral list,
        # we take female as the protected attribute
        protectedAttribute = 'm' if data['dominantSexXing'] == 'f' else 'f'

        for r in data['profiles']:
            # determine Member since / Hits
            if 'memberSince_Hits' in r['profile'][0]:
                hits_string = r['profile'][0]['memberSince_Hits']
                hits = hits_string.split(' / ')[1]
            else:
                hits = 1

            work_experience = self.__determineWorkMonths(r)
            edu_experience = self.__determineEduMonths(r)
            score = (work_experience + edu_experience) * int(hits)

            if self.__determineIfProtected(r, protectedAttribute):
                protected.append(Candidate(score, [protectedAttribute]))
                originalOrdering.append(Candidate(score, [protectedAttribute]))
            else:
                nonProtected.append(Candidate(score, []))
                originalOrdering.append(Candidate(score, []))

        protected.sort(key=lambda candidate: candidate.qualification, reverse=True)
        nonProtected.sort(key=lambda candidate: candidate.qualification, reverse=True)

        normalizeQualifications(protected + nonProtected)
        normalizeQualifications(originalOrdering)

        currentfile.close()
        return xingSearchQuery, protected, nonProtected, originalOrdering


    def __determineIfProtected(self, r, protAttr):
        """
        takes a JSON profile and finds if the person belongs to the protected group

        Parameter:
        ---------
        r : JSON node
        a person description in JSON, everything below node "profile"

        """

        if 'sex' in r['profile'][0]:
            if r['profile'][0]['sex'] == protAttr:
                return True
            else:
                return False
        else:
            print('>>> undetermined\n')
            return False


    def __determineWorkMonths(self, r):
        """
        takes a person's profile as JSON node and computes the total amount of work months this
        person has

        Parameters:
        ----------
        r : JSON node
        """

        total_working_months = 0  # ..of that profile
        job_duration = 0

        if len(r['profile'][0]) > 4:  # a job is on the profile
            list_of_Jobs = r['profile'][0]['jobs']
            # print('profile summary' + str(r['profile'][0]['jobs']))
            for count in range(0, len(list_of_Jobs)):
                if len(list_of_Jobs[count]) > 3:  # an exact duration is given at 5 nodes!

                    job_duration_string = list_of_Jobs[count]['jobDates']
                    if job_duration_string == 'bis heute':
                        # print('job with no dates found - will be count for ' + str(job_with_no_dates) + ' months.')
                        job_duration = self.EDUCATION_OR_JOB_WITH_NO_DATES

                    else:
                        job_start_string, job_end_string = job_duration_string.split(' - ')

                        if len(job_start_string) == 4:
                            job_start = datetime.datetime.strptime(job_start_string, "%Y")
                        elif len(job_start_string) == 7:
                            job_start = datetime.datetime.strptime(job_start_string, "%m/%Y")
                        else:
                            print("error reading start date")

                        if len(job_end_string) == 4:
                            job_end = datetime.datetime.strptime(job_end_string, "%Y")
                        elif len(job_end_string) == 7:
                            job_end = datetime.datetime.strptime(job_end_string, "%m/%Y")
                        else:
                            print("error reading end date")

                        if job_end - job_start == 0:
                            delta = self.EDUCATION_OR_JOB_WITH_SAME_YEAR
                        else:
                            delta = job_end - job_start

                        job_duration = math.ceil(delta.total_seconds() / 2629743.83)

                total_working_months += job_duration
        else:
            print('-no jobs on profile-')

        return total_working_months


    def __determineEduMonths(self, r):
        """
        takes a person's profile as JSON node and computes the total amount of work months this
        person has

        Parameters:
        ----------
        r : JSON node
        """

        total_education_months = 0  # ..of that profile
        edu_duration = 0

        if 'education' in r:  # education info is on the profile
            list_of_edu = r['education']  # edu child nodes {institution, url, degree, eduDuration}
            # print('education summary' + str(r['education']))
            for count in range(0, len(list_of_edu)):
                if 'eduDuration' in list_of_edu[count]:  # there are education dates

                    edu_duration_string = list_of_edu[count]['eduDuration']
                    if edu_duration_string == ('bis heute' or None or ''):
                        edu_duration = self.EDUCATION_OR_JOB_WITH_NO_DATES
                    else:
                        edu_start_string, edu_end_string = edu_duration_string.split(' - ')

                        if len(edu_start_string) == 4:
                            edu_start = datetime.datetime.strptime(edu_start_string, "%Y")
                        elif len(edu_start_string) == 7:
                            edu_start = datetime.datetime.strptime(edu_start_string, "%m/%Y")
                        else:
                            print("error reading start date")

                        if len(edu_end_string) == 4:
                            edu_end = datetime.datetime.strptime(edu_end_string, "%Y")
                        elif len(edu_end_string) == 7:
                            edu_end = datetime.datetime.strptime(edu_end_string, "%m/%Y")
                        else:
                            print("error reading end date")

                        if edu_end - edu_start == 0:
                            delta = self.EDUCATION_OR_JOB_WITH_SAME_YEAR
                        else:
                            delta = edu_end - edu_start

                        edu_duration = math.ceil(delta.total_seconds() / 2629743.83)

                        # print(job_duration_string)
                        # print('this job: ' + str(job_duration))

                else: edu_duration = self.EDUCATION_OR_JOB_WITH_NO_DATES

                total_education_months += edu_duration
                # print('total jobs: ' + str(total_working_months))

            # print("studying: " + str(total_education_months))
        else:
            print('-no education on profile-')

        return total_education_months

