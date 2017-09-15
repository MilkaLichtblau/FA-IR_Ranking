'''
Created on Feb 9, 2017

@author: meike.zehlike
'''
import os
import pandas as pd

from readWriteRankings.readAndWriteRankings import loadPicklesFromDirectory, loadPicklesFromSubDirs, \
    writePickleToDisk
from evaluator import metrics
from utilsAndConstants.utils import Switch
from utilsAndConstants.printsAndPlots import plotTwoListsInOnePlot



class Evaluator(object):

    """
    reads all previously created rankings from the results directory and applies all metrics to these
    rankings. Stores the results of these measurements in a separate data structure for each data set

    ranking types:
        * color-blind
        * Feldman et al.
        * FairRankingCreator using p = {0.1, 0.2, ..., 0.9}, alpha = 0.1
        * for Xing, we compare all created rankings to the original ranking we obtained when crawling
          their web site

    current data sets and experimental settings we use:
        * COMPAS data set, evaluated with respect to gender and race
        * German Credit data set, evaluated with respect to gender and age
        * SAT score data set, evaluated with respect to gender
        * Xing data set, evaluated with respect to gender

    current metrics we apply:
        * general metrics:
            ** percentage of protected people in the result ranking
            ** ndcp of the result ranking
        * own metrics:
            ** selected unfairness
            ** ordering unfairness
    """

    # CURRENT_WORKING_DIR = os.getcwd()

    # ranking types
    COLORBLIND = 'colorblind'
    FAIR_RANKING_01 = 'fairranking01'
    FAIR_RANKING_02 = 'fairranking02'
    FAIR_RANKING_03 = 'fairranking03'
    FAIR_RANKING_04 = 'fairranking04'
    FAIR_RANKING_05 = 'fairranking05'
    FAIR_RANKING_06 = 'fairranking06'
    FAIR_RANKING_07 = 'fairranking07'
    FAIR_RANKING_08 = 'fairranking08'
    FAIR_RANKING_09 = 'fairranking09'
    FELDMAN = 'feldman'
    ORIGINAL = 'original'

    LAMBDA = 0.00001


    @property
    def compasGenderResults(self):
        """
        a dictionary that maps from the ranking type to the result metrics for data set COMPAS
        evaluated towards gender
        """
        return self.__compasGenderResults


    @property
    def compasRaceResults(self):
        """
        a dictionary that maps from the ranking type to the result metrics for data set COMPAS
        evaluated towards race
        """
        return self.__compasRaceResults


    @property
    def germanCreditAge25Results(self):
        """
        a dictionary that maps from the ranking type to the result metrics for data set German Credit
        evaluated towards age to be younger than 25
        """
        return self.__germanCreditAge25Results


    @property
    def germanCreditAge35Results(self):
        """
        a dictionary that maps from the ranking type to the result metrics for data set German Credit
        evaluated towards age to be younger than 35
        """
        return self.__germanCreditAge35Results


    @property
    def germanCreditGenderResults(self):
        """
        a dictionary that maps from the ranking type to the result metrics for data set German Credit
        evaluated towards gender
        """
        return self.__germanCreditGenderResults


    @property
    def SATResults(self):
        """
        a dictionary that maps from the ranking type to the result metrics for data set SAT
        evaluated towards gender
        """
        return self.__SATResults


    @property
    def xingResults(self):
        """
        a two layered dictionary that maps from the Xing query that was issued to collect a candidate set to
        all ranking types. These ranking types themselves then map to the result metrics for the
        measured data set.
        evaluated towards gender

        looks like that:

        xing query (job description 1) : | ranking type (COLORBLIND) : result metrics
                                         | ranking type (FELDMAN) : result metrics
                                         | ranking type (FAIR) : result metrics
        xing query (job description 2) : | ranking type (COLORBLIND) : result metrics
                                         | ranking type (FELDMAN) : result metrics
                                         | ranking type (FAIR) : result metrics
        """
        return self.__xingResults

    @property
    def whichDataset(self):
        return self.__whichDataset


    # init generisch für den ganzen pfad
    def __init__(self, dataset=None):
        print(os.getcwd())
        if dataset is None:
            self.__compasGenderResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/Compas/Gender/')
            self.__compasRaceResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/Compas/Race/')
            self.__germanCreditAge25Results = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/German Credit/Age25/')
            self.__germanCreditAge35Results = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/German Credit/Age35/')
            self.__germanCreditGenderResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/German Credit/Gender/')
            self.__SATResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/SAT/')
            self.__xingResults = self.evaluateXing(os.getcwd() + '/' + '../results/rankingDumps/Xing/')

            self.__normalizeUtility(self.compasGenderResults)
            self.__normalizeUtility(self.compasRaceResults)
            self.__normalizeUtility(self.germanCreditAge25Results)
            self.__normalizeUtility(self.germanCreditAge35Results)
            self.__normalizeUtility(self.germanCreditGenderResults)
            self.__normalizeUtility(self.SATResults)
            for jobDescription, metricsResults in self.xingResults.items():
                self.__normalizeUtility(self.xingResults[jobDescription])

            self.__compasGenderResults = self.compasGenderResults.T
            self.__compasRaceResults = self.compasRaceResults.T
            self.__germanCreditAge25Results = self.germanCreditAge25Results.T
            self.__germanCreditAge35Results = self.germanCreditAge35Results.T
            self.__germanCreditGenderResults = self.germanCreditGenderResults.T
            self.__SATResults = self.SATResults.T
            for jobDescription, metricsResults in self.xingResults.items():
                self.__xingResults[jobDescription] = self.xingResults[jobDescription].T
        else:
            self.__whichDataset = dataset
            for case in Switch(self.whichDataset):
                if case('compas_gender'):
                    self.__compasGenderResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/Compas/Gender/')
                    self.__normalizeUtility(self.compasGenderResults)
                    self.__compasGenderResults = self.compasGenderResults.T
                    break
                if case('compas_race'):
                    self.__compasRaceResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/Compas/Race/')
                    self.__normalizeUtility(self.compasRaceResults)
                    self.__compasRaceResults = self.compasRaceResults.T
                    break
                if case('germancredit_25'):
                    self.__germanCreditAge25Results = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/German Credit/Age25/')
                    self.__normalizeUtility(self.germanCreditAge25Results)
                    self.__germanCreditAge25Results = self.germanCreditAge25Results.T
                    break
                if case('germancredit_35'):
                    self.__germanCreditAge35Results = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/German Credit/Age35/')
                    self.__normalizeUtility(self.germanCreditAge35Results)
                    self.__germanCreditAge35Results = self.germanCreditAge35Results.T
                    break
                if case('germancredit_gender'):
                    self.__germanCreditGenderResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/German Credit/Gender/')
                    self.__normalizeUtility(self.germanCreditGenderResults)
                    self.__germanCreditGenderResults = self.germanCreditGenderResults.T
                    break
                if case('sat'):
                    self.__SATResults = self.evaluate(os.getcwd() + '/' + '../results/rankingDumps/SAT/')
                    self.__normalizeUtility(self.SATResults)
                    self.__SATResults = self.SATResults.T
                    break
                if case('xing'):
                    self.__xingResults = self.evaluateXing(os.getcwd() + '/' + '../results/rankingDumps/Xing/')
                    for jobDescription, metricsResults in self.xingResults.items():
                        self.__normalizeUtility(self.xingResults[jobDescription])
                        self.__xingResults[jobDescription] = self.xingResults[jobDescription].T
                    break


    def evaluate(self, path):
        """
        loads all rankings (which are of all possible ranking types) from a directory and applies
        metrics to it, stores that in a dict with key=ranking type and value=measurements

        Return:
        ------
        a dictionary that maps from ranking type to metrics result
        """
        print("evaluate rankings from {0}".format(path))
        rankings = loadPicklesFromDirectory(path)
        result = dict()
        result[self.COLORBLIND] = self.__evaluatePairwiseRanking(rankings, self.COLORBLIND)
        result[self.FELDMAN] = self.__evaluatePairwiseRanking(rankings, self.FELDMAN)
        result[self.FAIR_RANKING_01] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_01)
        result[self.FAIR_RANKING_02] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_02)
        result[self.FAIR_RANKING_03] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_03)
        result[self.FAIR_RANKING_04] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_04)
        result[self.FAIR_RANKING_05] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_05)
        result[self.FAIR_RANKING_06] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_06)
        result[self.FAIR_RANKING_07] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_07)
        result[self.FAIR_RANKING_08] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_08)
        result[self.FAIR_RANKING_09] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_09)

        print("[Done] with {0}".format(path))
        print("====================================================================================")
        return pd.DataFrame(result)


    def evaluateXing(self, path):
        """
        handles special Xing case because rankings are organized in sub-directories. Apart from that
        works as self.evaluate

        Return:
        ------
        a two layered dictionary mapping from job description query to ranking type to result metrics
        """
        allRankings = loadPicklesFromSubDirs(path)
        resultsForAllSubdirs = dict()
        for dirname, rankings in allRankings.items():
            print("evaluate rankings from {0}".format(path + dirname))
            resultForOneSubdir = dict()
            resultForOneSubdir[self.COLORBLIND] = self.__evaluatePairwiseRanking(rankings, self.COLORBLIND)
            resultForOneSubdir[self.FELDMAN] = self.__evaluatePairwiseRanking(rankings, self.FELDMAN)
            resultForOneSubdir[self.FAIR_RANKING_01] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_01)
            resultForOneSubdir[self.FAIR_RANKING_02] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_02)
            resultForOneSubdir[self.FAIR_RANKING_03] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_03)
            resultForOneSubdir[self.FAIR_RANKING_04] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_04)
            resultForOneSubdir[self.FAIR_RANKING_05] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_05)
            resultForOneSubdir[self.FAIR_RANKING_06] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_06)
            resultForOneSubdir[self.FAIR_RANKING_07] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_07)
            resultForOneSubdir[self.FAIR_RANKING_08] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_08)
            resultForOneSubdir[self.FAIR_RANKING_09] = self.__evaluatePairwiseRanking(rankings, self.FAIR_RANKING_09)
            resultForOneSubdir[self.ORIGINAL] = self.__evaluateXingOriginalRanking(rankings)

            resultsForAllSubdirs[dirname.lower()] = pd.DataFrame(resultForOneSubdir)

            print("[Done] with {0}".format(path + dirname))
            print("===================")

        return resultsForAllSubdirs


    def __evaluateXingOriginalRanking(self, rankings):
        """
        evaluates the original Xing ranking that was obtained from the xing query. Needs special
        treatment because there is no pair ranking that contains the non-selected, hence selection
        unfairness measure doesn't make sense
        """
        for filename, rank in rankings.items():
            if self.ORIGINAL in filename.lower():
                util = metrics.ndcp(rank)
                orderUnfair = metrics.orderingUtility(rank)
                percentProt = metrics.percentageOfProtected(rank)
                return pd.Series({'util':util, 'selectUnfair':0, 'orderUnfair':orderUnfair,
                                  'percentProt':percentProt, 'percentProt_dataset':percentProt})


    def __evaluatePairwiseRanking(self, rankings, rankingType):
        """
        performs the actual measurements for a pair of rankings of a given type, e.g. for the
        color-blind ranking and the color-blind not selected candidates
        """

        print("current ranking name: {0}".format(rankingType), end='', flush=True)

        # not-selected candidates are needed for determining selection unfairness
        ranking, notSelected, percProtDataset = self.__findFilePair(rankingType, rankings)

        util = metrics.ndcp(ranking)
        selectUnfair = metrics.selectionUtility(ranking, notSelected)
        orderUnfair = metrics.orderingUtility(ranking)
        percentProt = metrics.percentageOfProtected(ranking)
        print(" [Done]")

        return pd.Series({'util':util, 'selectUnfair':selectUnfair, 'orderUnfair':orderUnfair,
                          'percentProt':percentProt, 'percentProt_dataset':percProtDataset})


    def __findFilePair(self, rankingType, rankings):
        """
        finds the file pair of one ranking type in a particular experiment (e.g. for the SAT rankings
        it finds the colorblind ranking and the respective list of candidates not selected for a
        colorblind ranking

        @param rankingType: the type of the ranking, e.g. FAIR_RANKING_01
        @param rankings: all rankings of one particular directory
        """

        ranking, notSelected = [], []
        for filename, rank in rankings.items():
            if rankingType in filename.lower():
                if "notselected" in filename.lower():
                    notSelected = rank
                else:
                    ranking = rank
        dataset = ranking + notSelected
        percProt = metrics.percentageOfProtected(dataset)
        return ranking, notSelected, percProt


    def __getCandidateRankingByIDs(self, ranking):
        """
        creates a list that contains only the candidates' identifiers, preserving the original order
        of the given ranking. Needed to apply the yangStoyanovich metrics
        """
        IDRanking = []
        IDsOfProtected = []
        for candidate in ranking:
            IDRanking.append(candidate.uuid)
            if candidate.isProtected:
                IDsOfProtected.append(candidate.uuid)
        return IDRanking, IDsOfProtected


    def __normalizeUtility(self, result):
        maxUtil = result.loc['util'].max()
        for idx, util in result.loc['util'].iteritems():
            result.loc['util'][idx] = util / maxUtil


    def dumpResults(self, directory):
        directory = os.getcwd() + directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        writePickleToDisk(self.compasGenderResults, directory + 'CompasGenderResults.pickle')
        writePickleToDisk(self.compasRaceResults, directory + 'CompasRaceResults.pickle')
        writePickleToDisk(self.germanCreditAge25Results, directory + 'GermanCreditAge25Results.pickle')
        writePickleToDisk(self.germanCreditAge35Results, directory + 'GermanCreditAge35Results.pickle')
        writePickleToDisk(self.germanCreditGenderResults, directory + 'GermanCreditGenderResults.pickle')
        writePickleToDisk(self.SATResults, directory + 'SATResults.pickle')
        writePickleToDisk(self.xingResults, directory + 'XingResults.pickle')


    def printResults(self):
        if self.whichDataset is not None:
            if self.whichDataset == 'compas_gender':
                print("========================================================================================")
                print("COMPAS Gender Results")
                print(self.compasGenderResults)
                print("========================================================================================")
            elif self.whichDataset == 'compas_race':
                print("========================================================================================")
                print("COMPAS race results")
                print(self.compasRaceResults)
                print("========================================================================================")
            elif self.whichDataset == 'germancredit_gender':
                print("========================================================================================")
                print("GERMAN CREDIT gender results")
                print(self.germanCreditGenderResults)
                print("========================================================================================")
            elif self.whichDataset == 'germancredit_25':
                print("GERMAN CREDIT age 25 results")
                print(self.germanCreditAge25Results)
                print("========================================================================================")
            elif self.whichDataset == 'germancredit_35':
                print("========================================================================================")
                print("GERMAN CREDIT age 35 results")
                print(self.germanCreditAge35Results)
                print("========================================================================================")
            elif self.whichDataset == 'sat':
                print("========================================================================================")
                print("SAT results")
                print(self.SATResults)
                print("========================================================================================")
            elif self.whichDataset == 'xing':
                print("========================================================================================")
                print("Xing results")
                for rankingType, allMetrics in self.xingResults.items():
                    for metricsType, result in allMetrics.items():
                        print("{0}        {1}\n{2}".format(rankingType, metricsType, result))
                    print("--------------------------------------------------------")
                print("========================================================================================")
        else:
            print("========================================================================================")
            print("COMPAS Gender Results")
            print(self.compasGenderResults)
            print("========================================================================================")
            print("========================================================================================")
            print("COMPAS race results")
            print(self.compasRaceResults)
            print("========================================================================================")
            print("========================================================================================")
            print("GERMAN CREDIT gender results")
            print(self.germanCreditGenderResults)
            print("========================================================================================")
            print("GERMAN CREDIT age 25 results")
            print(self.germanCreditAge25Results)
            print("========================================================================================")
            print("========================================================================================")
            print("GERMAN CREDIT age 35 results")
            print(self.germanCreditAge35Results)
            print("========================================================================================")
            print("========================================================================================")
            print("SAT results")
            print(self.SATResults)
            print("========================================================================================")
            print("========================================================================================")
            print("Xing results")
            for rankingType, allMetrics in self.xingResults.items():
                for metricsType, result in allMetrics.items():
                    print("{0}        {1}\n{2}".format(rankingType, metricsType, result))
                print("--------------------------------------------------------")
            print("========================================================================================")


    def plotOrderingUtilityVsPercentageOfProtected(self):
        ps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        if self.whichDataset is not None:
            if self.whichDataset == 'germancredit_25':
                orderUtil = self.germanCreditAge25Results.T.loc['orderUnfair']
                orderUtil = orderUtil.drop(orderUtil.index[0])
                orderUtil = orderUtil.drop(orderUtil.index[-1])
                orderUtilValues = [1 - abs(values[1]) for values in orderUtil]

                percentProt = self.germanCreditAge25Results.T.loc['percentProt']
                percentProt = percentProt.drop(percentProt.index[0])
                percentProt = percentProt.drop(percentProt.index[-1])

                plotTwoListsInOnePlot(ps, percentProt.values, orderUtilValues, 'Protected', 'Ordering Utility',
                                       "p", r"Percentage Protected in Ranking", r"Ordering Utility",
                                       '../results/plots/d4-protected-vs-ordering.pdf')

                utilList = self.germanCreditAge25Results.T.loc['util']
                utilList = utilList.drop('colorblind')
                utilList = utilList.drop('feldman')

                plotTwoListsInOnePlot(ps, percentProt.values, utilList.values, 'Protected', 'NDCG',
                                      "p",
                                      r"Percentage Protected in Ranking",
                                      r"NDCG",
                                      '../results/plots/d4-protected-vs-ndcg.pdf')
        else:
            print('not yet implemented')



