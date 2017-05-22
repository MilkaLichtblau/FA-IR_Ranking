'''
Created on Mar 29, 2017

@author: meike.zehlike
'''
import os
import argparse

from readWriteRankings.readAndWriteRankings import writePickleToDisk
from ranker import createRankings
from utilsAndConstants.constants import ESSENTIALLY_ZERO
from utilsAndConstants.utils import setMemoryLimit
from datasetCreator import compasData, germanCreditData, satData, xingProfilesReader, chileSATData
from evaluator.evaluator import Evaluator
from evaluator.failProbabilityYangStoyanovich import determineFailProbOfGroupFairnessTesterForStoyanovichRanking

EVALUATE_FAILURE_PROBABILITY = 0

def main():
    setMemoryLimit(10000000000)

    # create the top-level parser
    parser = argparse.ArgumentParser(prog='FA*IR', description='a fair Top-k ranking algorithm',
                                     epilog="=== === === end === === ===")
                                     # argument_default="-a")
    parser.add_argument("-c", "--create", nargs='*', help="creates a ranking and dumps it to disk")
    parser.add_argument("-e", "--evaluate", nargs='*', help="evaluates and transposes results")
    parser.add_argument("-r", "--rank", nargs='*', help="ranks")
    # parser.set_defaults(func='run_whole_prog')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "create" command
    parser_create = subparsers.add_parser('dataset_create', help='choose a dataset to generate')
    parser_create.add_argument(dest='dataset_to_evaluate', choices=["sat", "compas", "germancredit", "xing", "csat"])

    # create the parser for the "evaluate" command
    parser_evaluate = subparsers.add_parser('dataset_evaluate', help='choose a dataset to evaluate')
    parser_evaluate.add_argument(dest='dataset_to_create', choices=["sat", "xing"
                                                                  "compas_gender", "compas_race",
                                                                  "germancredit_25", "germancredit_35", "germancredit_gender"])

    # create the parser for the "rank" command
    # parser_evaluate = subparsers.add_parser('dataset_to_rank', help='choose a dataset to rank')
    # parser_evaluate.add_argument("-d", "--dataset", choices=["sat", "compas", "germancredit", "xing"])

    args = parser.parse_args()

    if args.create == []:
        print("creating rankings for all datasets...")
        createRankingsAndWriteToDisk()
    elif args.create == ['sat']:
        createSATData(1500)
    elif args.create == ['compas']:
            createCOMPASData(1000)
    elif args.create == ['germancredit']:
            createGermanCreditData(100)
    elif args.create == ['xing']:
            createXingData(40)
    elif args.create == ['csat']:
            createChileData(1500)
    elif args.evaluate == []:
        evaluator = Evaluator()
        evaluator.printResults()
    elif args.evaluate == ['compas_gender']:
        evaluator = Evaluator('compas_gender')
        evaluator.printResults()
    elif args.evaluate == ['compas_race']:
        evaluator = Evaluator('compas_race')
        evaluator.printResults()
    elif args.evaluate == ['germancredit_25']:
        evaluator = Evaluator('germancredit_25')
        evaluator.printResults()
    elif args.evaluate == ['germancredit_35']:
        evaluator = Evaluator('germancredit_35')
        evaluator.printResults()
    elif args.evaluate == ['germancredit_gender']:
        evaluator = Evaluator('germancredit_gender')
        evaluator.printResults()
    elif args.evaluate == ['xing']:
        evaluator = Evaluator('xing')
        evaluator.printResults()
    elif args.evaluate == ['sat']:
        evaluator = Evaluator('sat')
        evaluator.printResults()

    else:
        print("FA*IR \n running the full program \n Press ctrl+c to abort \n \n")
        createRankingsAndWriteToDisk()
        evaluator = Evaluator()
        evaluator.printResults()
#       in between commits
        if EVALUATE_FAILURE_PROBABILITY:
            determineFailProbOfGroupFairnessTesterForStoyanovichRanking()


def createRankingsAndWriteToDisk():
    createSATData(1500)
    # createChileData(1500)  # uncomment, if Chile Data Set is available.
    createCOMPASData(1000)
    createGermanCreditData(100)
    createXingData(40)


def createXingData(k):
    pairsOfPAndAlpha = [(0.1, 0.1),  # no real results, skip in evaluation
                        (0.2, 0.1),  # no real results, skip in evaluation
                        (0.3, 0.1),  # no real results, skip in evaluation
                        (0.4, 0.1),  # no real results, skip in evaluation
                        (0.5, 0.0168),
                        (0.6, 0.0321),
                        (0.7, 0.0293),
                        (0.8, 0.0328),
                        (0.9, 0.0375)]

    xingReader = xingProfilesReader.Reader('../rawData/Xing/*.json')  # glob gets abs/rel paths matching the regex
    for queryString, candidates in xingReader.entireDataSet.iterrows():
        dumpRankingsToDisk(candidates['protected'], candidates['nonProtected'], k, queryString,
                           "../results/rankingDumps/Xing" + '/' + queryString + '/', pairsOfPAndAlpha)
        writePickleToDisk(candidates['originalOrdering'], os.getcwd() + '/../results/rankingDumps/Xing/'
                          + '/' + queryString + '/' + 'OriginalOrdering.pickle')


def createGermanCreditData(k):

    pairsOfPAndAlpha = [(0.1, 0.1),  # no real results, skip in evaluation
                        (0.2, 0.1),  # no real results, skip in evaluation
                        (0.3, 0.0220),
                        (0.4, 0.0222),
                        (0.5, 0.0207),
                        (0.6, 0.0209),
                        (0.7, 0.0216),
                        (0.8, 0.0216),
                        (0.9, 0.0256)]

    protectedGermanCreditGender, nonProtectedGermanCreditGender = germanCreditData.create(
        "../rawData/GermanCredit/GermanCredit_sex.csv", "DurationMonth", "CreditAmount",
        "score", "sex", protectedAttribute=["female"])
    dumpRankingsToDisk(protectedGermanCreditGender, nonProtectedGermanCreditGender, k,
                       "GermanCreditGender", "../results/rankingDumps/German Credit/Gender",
                       pairsOfPAndAlpha)

    protectedGermanCreditAge25, nonProtectedGermanCreditAge25 = germanCreditData.create(
        "../rawData/GermanCredit/GermanCredit_age25.csv", "DurationMonth", "CreditAmount",
        "score", "age25", protectedAttribute=["younger25"])
    dumpRankingsToDisk(protectedGermanCreditAge25, nonProtectedGermanCreditAge25, k,
                       "GermanCreditAge25", "../results/rankingDumps/German Credit/Age25",
                       pairsOfPAndAlpha)

    protectedGermanCreditAge35, nonProtectedGermanCreditAge35 = germanCreditData.create(
        "../rawData/GermanCredit/GermanCredit_age35.csv", "DurationMonth", "CreditAmount",
        "score", "age35", protectedAttribute=["younger35"])
    dumpRankingsToDisk(protectedGermanCreditAge35, nonProtectedGermanCreditAge35, k,
                       "GermanCreditAge35", "../results/rankingDumps/German Credit/Age35",
                       pairsOfPAndAlpha)


def createCOMPASData(k):

    pairsOfPAndAlpha = [(0.1, 0.0140),
                        (0.2, 0.0115),
                        (0.3, 0.0103),
                        (0.4, 0.0099),
                        (0.5, 0.0096),
                        (0.6, 0.0093),
                        (0.7, 0.0094),
                        (0.8, 0.0095),
                        (0.9, 0.0100)]

    protectedCompasRace, nonProtectedCompasRace = compasData.createRace(
       "../rawData/COMPAS/ProPublica_race.csv", "race", "Violence_rawscore", "Recidivism_rawscore",
       "priors_count")
    dumpRankingsToDisk(protectedCompasRace, nonProtectedCompasRace, k, "CompasRace",
                       "../results/rankingDumps/Compas/Race", pairsOfPAndAlpha)

    protectedCompasGender, nonProtectedCompasGender = compasData.createGender(
       "../rawData/COMPAS/ProPublica_sex.csv", "sex", "Violence_rawscore", "Recidivism_rawscore",
       "priors_count")
    dumpRankingsToDisk(protectedCompasGender, nonProtectedCompasGender, k, "CompasGender",
                      "../results/rankingDumps/Compas/Gender", pairsOfPAndAlpha)


def createSATData(k):

    SATFile = '../rawData/SAT/sat_data.pdf'

    pairsOfPAndAlpha = [(0.1, 0.0122),
                        (0.2, 0.0101),
                        (0.3, 0.0092),
                        (0.4, 0.0088),
                        (0.5, 0.0084),
                        (0.6, 0.0085),
                        (0.7, 0.0084),
                        (0.8, 0.0084),
                        (0.9, 0.0096)]

    satSetCreator = satData.Creator(SATFile)
    protectedSAT, nonProtectedSAT = satSetCreator.create()
    dumpRankingsToDisk(protectedSAT, nonProtectedSAT, k, "SAT", "../results/rankingDumps/SAT", pairsOfPAndAlpha)


def createChileData(k):

    # loop through all files
    chileDir = '../rawData/ChileSAT/Dataset'
    pairsOfPAndAlpha = [(0.1, 0.0122),
                        (0.2, 0.0101),
                        (0.3, 0.0092),
                        (0.4, 0.0088),
                        (0.5, 0.0084),
                        (0.6, 0.0085),
                        (0.7, 0.0084),
                        (0.8, 0.0084),
                        (0.9, 0.0096)]
    for root, dirs, filenames in os.walk(chileDir):
        for chileFile in filenames:
            if not chileFile.startswith('.') and os.path.isfile(os.path.join(root, chileFile)):

                chileFile = '../rawData/ChileSAT/Dataset/' + chileFile
                print("reading: " + chileFile)

                protectedChileSATSchool, nonProtectedChileSATSchool = chileSATData.createSchool(chileFile, 6)
                dumpRankingsToDisk(protectedChileSATSchool, nonProtectedChileSATSchool, k, "ChileSATSchool",
                                   "../results/rankingDumps/ChileSAT", pairsOfPAndAlpha)
                # protectedChileSATNat, nonProtectedChileSATNat = chileSATData.createNationality(chileFile, 6)
                # dumpRankingsToDisk(protectedChileSATNat, nonProtectedChileSATNat, k, "ChileSATNationality",
                #                    "../results/rankingDumps/ChileSAT", pairsOfPAndAlpha)


def dumpRankingsToDisk(protected, nonProtected, k, dataSetName, directory, pairsOfPAndAlpha):
    """
    creates all rankings we need for one experimental data set and writes them to disk to be used later

    @param protected:        list of protected candidates, assumed to satisfy in-group monotonicty
    @param nonProtected:     list of non-protected candidates, assumed to satisfy in-group monotonicty
    @param k:                length of the rankings we want to create
    @param dataSetName:      determines which data set is used in this experiment
    @param directory:        directory in which to store the rankings
    @param pairsOfPAndAlpha: contains the mapping of a certain alpha correction to be used for a certain p

    The experimental setting is as follows: for a given data set of protected and non-
    protected candidates we create the following rankings:
    * a colorblind ranking,
    * a ranking as in Feldman et al
    * ten rankings using our FairRankingCreator, with p varying from 0.1, 0.2 to 0.9, whereas alpha
      stays 0.1

    """
    print("====================================================================")
    print("create rankings of {0}".format(dataSetName))

    if not os.path.exists(os.getcwd() + '/' + directory + '/'):
        os.makedirs(os.getcwd() + '/' + directory + '/')

    print("colorblind ranking", end='', flush=True)
    colorblindRanking, colorblindNotSelected = createRankings.createFairRanking(k, protected, nonProtected, ESSENTIALLY_ZERO, 0.1)
    print(" [Done]")

    print("fair rankings", end='', flush=True)
    pair01 = [item for item in pairsOfPAndAlpha if item[0] == 0.1][0]
    fairRanking01, fair01NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair01[0], pair01[1])
    pair02 = [item for item in pairsOfPAndAlpha if item[0] == 0.2][0]
    fairRanking02, fair02NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair02[0], pair02[1])
    pair03 = [item for item in pairsOfPAndAlpha if item[0] == 0.3][0]
    fairRanking03, fair03NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair03[0], pair03[1])
    pair04 = [item for item in pairsOfPAndAlpha if item[0] == 0.4][0]
    fairRanking04, fair04NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair04[0], pair04[1])
    pair05 = [item for item in pairsOfPAndAlpha if item[0] == 0.5][0]
    fairRanking05, fair05NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair05[0], pair05[1])
    pair06 = [item for item in pairsOfPAndAlpha if item[0] == 0.6][0]
    fairRanking06, fair06NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair06[0], pair06[1])
    pair07 = [item for item in pairsOfPAndAlpha if item[0] == 0.7][0]
    fairRanking07, fair07NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair07[0], pair07[1])
    pair08 = [item for item in pairsOfPAndAlpha if item[0] == 0.8][0]
    fairRanking08, fair08NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair08[0], pair08[1])
    pair09 = [item for item in pairsOfPAndAlpha if item[0] == 0.9][0]
    fairRanking09, fair09NotSelected = createRankings.createFairRanking(k, protected, nonProtected, pair09[0], pair09[1])
    print(" [Done]")

    print("feldman ranking", end='', flush=True)
    feldmanRanking, feldmanNotSelected = createRankings.createFeldmanRanking(protected, nonProtected, k)
    print(" [Done]")

    print("Write rankings to disk", end='', flush=True)
    writePickleToDisk(colorblindRanking, os.getcwd() + '/' + directory + '/' + dataSetName + 'ColorblindRanking.pickle')
    writePickleToDisk(colorblindNotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'ColorblindRankingNotSelected.pickle')
    writePickleToDisk(feldmanRanking, os.getcwd() + '/' + directory + '/' + dataSetName + 'FeldmanRanking.pickle')
    writePickleToDisk(feldmanNotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FeldmanRankingNotSelected.pickle')
    writePickleToDisk(fairRanking01, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking01PercentProtected.pickle')
    writePickleToDisk(fair01NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking01NotSelected.pickle')
    writePickleToDisk(fairRanking02, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking02PercentProtected.pickle')
    writePickleToDisk(fair02NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking02NotSelected.pickle')
    writePickleToDisk(fairRanking03, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking03PercentProtected.pickle')
    writePickleToDisk(fair03NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking03NotSelected.pickle')
    writePickleToDisk(fairRanking04, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking04PercentProtected.pickle')
    writePickleToDisk(fair04NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking04NotSelected.pickle')
    writePickleToDisk(fairRanking05, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking05PercentProtected.pickle')
    writePickleToDisk(fair05NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking05NotSelected.pickle')
    writePickleToDisk(fairRanking06, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking06PercentProtected.pickle')
    writePickleToDisk(fair06NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking06NotSelected.pickle')
    writePickleToDisk(fairRanking07, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking07PercentProtected.pickle')
    writePickleToDisk(fair07NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking07NotSelected.pickle')
    writePickleToDisk(fairRanking08, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking08PercentProtected.pickle')
    writePickleToDisk(fair08NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking08NotSelected.pickle')
    writePickleToDisk(fairRanking09, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking09PercentProtected.pickle')
    writePickleToDisk(fair09NotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking09NotSelected.pickle')
    print(" [Done]")



if __name__ == '__main__':
    main()
