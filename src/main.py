'''
Created on Mar 29, 2017

@author: meike.zehlike
'''
import os
import argparse

from readWriteRankings.readAndWriteRankings import writePickleToDisk, convertFAIRPicklesToCSVForL2R
from post_processing_methods.fair_ranker.create import buildFairRanking
from utilsAndConstants.constants import ESSENTIALLY_ZERO
from utilsAndConstants.utils import setMemoryLimit
from dataset_creator import *
from evaluator.evaluator import Evaluator
from evaluator.failProbabilityYangStoyanovich import determineFailProbOfGroupFairnessTesterForStoyanovichRanking
from post_processing_methods import fair_ranker

EVALUATE_FAILURE_PROBABILITY = 0


def main():
    setMemoryLimit(10000000000)

    # create the top-level parser
    parser = argparse.ArgumentParser(prog='FA*IR', description='a fair Top-k ranking algorithm',
                                     epilog="=== === === end === === ===")
    parser.add_argument("-c", "--create", nargs='*', help="creates a ranking from the raw data and dumps it to disk")
    parser.add_argument("-e", "--evaluate", nargs='*', help="evaluates rankings and writes results to disk")
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "create" command
    parser_create = subparsers.add_parser('dataset_create', help='choose a dataset to generate')
    parser_create.add_argument(dest='dataset_to_create', choices=["sat", "compas", "germancredit", "xing", "chilesat", "lsat"])

    # create the parser for the "evaluate" command
    parser_evaluate = subparsers.add_parser('dataset_evaluate', help='choose a dataset to evaluate')
    parser_evaluate.add_argument(dest='dataset_to_evaluate', choices=["sat", "xing",
                                                                  "compas_gender", "compas_race",
                                                                  "germancredit_25", "germancredit_35", "germancredit_gender"])

    args = parser.parse_args()

    if args.create == []:
        print("creating rankings for all datasets...")
        createDataAndRankings()
    elif args.create == ['sat']:
        createAndRankSATData()
    elif args.create == ['compas']:
        createAndRankCOMPASData()
    elif args.create == ['germancredit']:
        createAndRankGermanCreditData()
    elif args.create == ['xing']:
        createAndRankXingData()
    elif args.create == ['chilesat']:
        createAndRankChileData()
        # gender
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/gender/fold_1/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/gender/",
                               fold="fold_1/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/gender/fold_2/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/gender/",
                               fold="fold_2/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/gender/fold_3/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/gender/",
                               fold="fold_3/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/gender/fold_4/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/gender/",
                               fold="fold_4/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/gender/fold_5/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/gender/",
                               fold="fold_5/")
        # highschool
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/highschool/fold_1/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/highschool/",
                               fold="fold_1/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/highschool/fold_2/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/highschool/",
                               fold="fold_2/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/highschool/fold_3/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/highschool/",
                               fold="fold_3/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/highschool/fold_4/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/highschool/",
                               fold="fold_4/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/ChileSAT/highschool/fold_5/",
                               "../../Meike-FairnessInL2R-Code/octave-src/sample/ChileUni/NoSemi/highschool/",
                               fold="fold_5/")
    elif args.create == ['lsat']:
        createAndRankLSATData()
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/LSAT/gender/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/LawStudents/gender/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/LSAT/race_black/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/LawStudents/race_black/")
    elif args.create == ['trec']:
        createAndRankTRECData()
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/TREC/fold_1/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/TREC/",
                                fold="fold_1/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/TREC/fold_2/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/TREC/",
                                fold="fold_2/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/TREC/fold_3/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/TREC/",
                                fold="fold_3/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/TREC/fold_4/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/TREC/",
                                fold="fold_4/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/TREC/fold_5/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/TREC/",
                                fold="fold_5/")
        convertFAIRPicklesToCSVForL2R("../results/rankingDumps/TREC/fold_6/",
                                "../../Meike-FairnessInL2R-Code/octave-src/sample/TREC/",
                                fold="fold_6/")
    elif args.create == ['syntheticsat']:
        createSyntheticSAT()
    #=======================================================
    elif args.evaluate == []:
        evaluator = Evaluator()
        evaluator.printResults()
    elif args.evaluate == ['compas_gender']:
        evaluator = Evaluator('compas_gender')
        evaluator.printResults()
        evaluator.plotOrderingUtilityVsPercentageOfProtected()
    elif args.evaluate == ['compas_race']:
        evaluator = Evaluator('compas_race')
        evaluator.printResults()
    elif args.evaluate == ['germancredit_25']:
        evaluator = Evaluator('germancredit_25')
        evaluator.printResults()
        evaluator.plotOrderingUtilityVsPercentageOfProtected()
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
        createDataAndRankings()
        evaluator = Evaluator()
        evaluator.printResults()

        if EVALUATE_FAILURE_PROBABILITY:
            determineFailProbOfGroupFairnessTesterForStoyanovichRanking()


def createDataAndRankings():
    createAndRankSATData()
#     createAndRankChileData()  # uncomment, if Chile Data Set is available.
    createAndRankLSATData()
    createAndRankTRECData()
    createAndRankCOMPASData()
    createAndRankGermanCreditData()
    createAndRankXingData()


def createSyntheticSAT(k):
#     creator = synthetic.SyntheticDatasetCreator(50000, {"gender": 2, "ethnicity": 3, "disability": 2}, ["score"])
    size = 50
    creator = synthetic.SyntheticDatasetCreator(1, size, {"gender": 2}, ["score"])
    creator.dataset.sort_values(by=['score'], inplace=True, ascending=False)
    creator.dataset['rank'] = range(size, 0, -1)
    creator.dataset['rank'] = creator.dataset['rank'] / size
    creator.writeToTXT('../rawData/Synthetic/sample_train_data_scoreAndGender_separated.txt')

    creator = synthetic.SyntheticDatasetCreator(1, size, {"gender": 2}, ["score"])
    creator.dataset.sort_values(by=['score'], inplace=True, ascending=False)
    creator.dataset['rank'] = range(size, 0, -1)
    creator.dataset['rank'] = creator.dataset['rank'] / size
    creator.writeToTXT('../rawData/Synthetic/sample_test_data_scoreAndGender_separated.txt')


def createAndRankXingData():
    k = 40
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
        rankAndDump(candidates['protected'], candidates['nonProtected'], k, queryString,
                           "../results/rankingDumps/Xing" + '/' + queryString + '/', pairsOfPAndAlpha)
        writePickleToDisk(candidates['originalOrdering'], os.getcwd() + '/../results/rankingDumps/Xing/'
                          +'/' + queryString + '/' + 'OriginalOrdering.pickle')


def createAndRankGermanCreditData():
    k = 100
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
    rankAndDump(protectedGermanCreditGender, nonProtectedGermanCreditGender, k,
                       "GermanCreditGender", "../results/rankingDumps/German Credit/Gender",
                       pairsOfPAndAlpha)

    protectedGermanCreditAge25, nonProtectedGermanCreditAge25 = germanCreditData.create(
        "../rawData/GermanCredit/GermanCredit_age25.csv", "DurationMonth", "CreditAmount",
        "score", "age25", protectedAttribute=["younger25"])
    rankAndDump(protectedGermanCreditAge25, nonProtectedGermanCreditAge25, k,
                       "GermanCreditAge25", "../results/rankingDumps/German Credit/Age25",
                       pairsOfPAndAlpha)

    protectedGermanCreditAge35, nonProtectedGermanCreditAge35 = germanCreditData.create(
        "../rawData/GermanCredit/GermanCredit_age35.csv", "DurationMonth", "CreditAmount",
        "score", "age35", protectedAttribute=["younger35"])
    rankAndDump(protectedGermanCreditAge35, nonProtectedGermanCreditAge35, k,
                       "GermanCreditAge35", "../results/rankingDumps/German Credit/Age35",
                       pairsOfPAndAlpha)


def createAndRankCOMPASData():
    k = 1000
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
    rankAndDump(protectedCompasRace, nonProtectedCompasRace, k, "CompasRace",
                       "../results/rankingDumps/Compas/Race", pairsOfPAndAlpha)

    protectedCompasGender, nonProtectedCompasGender = compasData.createGender(
       "../rawData/COMPAS/ProPublica_sex.csv", "sex", "Violence_rawscore", "Recidivism_rawscore",
       "priors_count")
    rankAndDump(protectedCompasGender, nonProtectedCompasGender, k, "CompasGender",
                      "../results/rankingDumps/Compas/Gender", pairsOfPAndAlpha)


def createAndRankSATData():
    k = 1500
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

    rankAndDump(protectedSAT, nonProtectedSAT, k, "SAT", "../results/rankingDumps/SAT", pairsOfPAndAlpha)


def createAndRankLSATData():

        # run with gender as protected attribute
    lsatGenderDir = '../rawData/LSAT/gender/'
    pairsOfPAndAlpha = [(0.337177280550775 - 0.1, 0.0066),
                        (0.437177280550775, 0.0063),
                        (0.537177280550775 + 0.1, 0.0063)]
    for root, _, filenames in os.walk(lsatGenderDir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if filename.endswith('SORTED.pred') and os.path.isfile(path):
                print("reading: " + filename + "\nfrom: " + root)

                lsatData = L2R_PredictionsData.Creator(path, 1, 'female')

                resultDir = "../results/rankingDumps/LSAT/gender/" + root.replace(lsatGenderDir, "")

                rankAndDump(lsatData.protectedCandidates,
                            lsatData.nonprotectedCandidates,
                            lsatData.length,
                            "LSAT_gender_",
                            resultDir,
                            pairsOfPAndAlpha)

    lsatRaceDir = '../rawData/LSAT/race_black/'
    p = 0.0638977635782748
    pairsOfPAndAlpha = [(p, 0.0095),
                        (p + 0.1, 0.0076)]
    for root, _, filenames in os.walk(lsatRaceDir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if filename.endswith('SORTED.pred') and os.path.isfile(path):
                print("reading: " + filename + "\nfrom: " + root)

                lsatData = L2R_PredictionsData.Creator(path, 1, 'black')

                resultDir = "../results/rankingDumps/LSAT/race_black/" + root.replace(lsatRaceDir, "")

                rankAndDump(lsatData.protectedCandidates,
                            lsatData.nonprotectedCandidates,
                            lsatData.length,
                            "LSAT_black_",
                            resultDir,
                            pairsOfPAndAlpha)


def createAndRankTRECData():
    p = 0.105
    pairsOfPAndAlpha = [(p - 0.1, 0.020263671875),
                        (p, 0.02783203125),
                        (p + 0.1, 0.05)]

    # run with gender as protected attribute
    trecDir = '../rawData/TREC/'
    for root, _, filenames in os.walk(trecDir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if filename.endswith('SORTED.pred') and os.path.isfile(path):
                print("reading: " + filename + "\nfrom: " + root)
                # TODO: apply algorithm per Query only
                trecData = L2R_PredictionsData.Creator(path, 1, 'female')

                resultDir = "../results/rankingDumps/TREC/" \
                            +root.replace(trecDir, "") \
                            +"/query_id=" + str(trecData.query_id) + "/"

                rankAndDump(trecData.protectedCandidates,
                            trecData.nonprotectedCandidates,
                            trecData.length,
                            "TREC_",
                            resultDir,
                            pairsOfPAndAlpha)


def createAndRankChileData():
    psAndAlphasPerQuery = {'1' : [(0.039293139293139, 0.02813720703125),
                                  (0.139293139293139, 0.016162109375),
                                  (0.239293139293139, 0.013385009765625)],
                           '2' : [(0.076352705410822, 0.0203857421875),
                                  (0.176352705410822, 0.0148498535156249),
                                  (0.276352705410822, 0.0131439208984375)],
                           '3' : [(0.127272727272727, 0.01683349609375),
                                  (0.227272727272727, 0.0137786865234375),
                                  (0.327272727272727, 0.0127555847167968)],
                           '4' : [(0.095011337868481, 0.01875),
                                  (0.195011337868481, 0.014581298828125),
                                  (0.295011337868481, 0.0129928588867187)],
                           '5' : [(0.173076923076923, 0.0151155471801757),
                                  (0.273076923076923, 0.0132232666015625),
                                  (0.373076923076923, 0.0124481201171875)]}
    # run with gender as protected attribute
    chileGenderDir = '../rawData/ChileUniversitySAT/NoSemiprivateSchools/gender/'
    for root, _, filenames in os.walk(chileGenderDir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if filename.endswith('SORTED.pred') and os.path.isfile(path):
                print("reading: " + filename + "\nfrom: " + root)

                chileData = L2R_PredictionsData.Creator(path, 1, 'female')
                pairsOfPAndAlpha = psAndAlphasPerQuery.get(str(chileData.query_id))
                resultDir = "../results/rankingDumps/ChileSAT/gender/" + root.replace(chileGenderDir, "")

                rankAndDump(chileData.protectedCandidates,
                            chileData.nonprotectedCandidates,
                            chileData.length,
                            "ChileSATGender_",
                            resultDir,
                            pairsOfPAndAlpha)

    # run with highschool type as protected attribute
    chileHighschoolDir = '../rawData/ChileUniversitySAT/NoSemiprivateSchools/highschool/'
    psAndAlphasPerQuery = {'1' : [(0.216008316008316, 0.0140625),
                                  (0.316008316008316, 0.0128196716308593),
                                  (0.416008316008316, 0.012176513671875)],
                           '2' : [(0.250701402805611, 0.01329345703125),
                                  (0.350701402805611, 0.0126083374023437),
                                  (0.450701402805611, 0.0118988037109375)],
                           '3' : [(0.250649350649351, 0.0132843017578125),
                                  (0.350649350649351, 0.01260986328125),
                                  (0.450649350649351, 0.0118865966796875)],
                           '4' : [(0.253741496598639, 0.0134849548339843),
                                  (0.353741496598639, 0.01246337890625),
                                  (0.453741496598639, 0.01165771484375)],
                           '5' : [(0.271153846153846, 0.013055419921875),
                                  (0.371153846153846, 0.0122451782226562),
                                  (0.471153846153846, 0.011566162109375)]}
    for root, _, filenames in os.walk(chileHighschoolDir):
        for filename in filenames:
            path = os.path.join(root, filename)
            if filename.endswith('SORTED.pred') and os.path.isfile(path):
                print("reading: " + filename + "\nfrom: " + root)

                chileData = L2R_PredictionsData.Creator(path, 1, 'publicSchool')
                pairsOfPAndAlpha = psAndAlphasPerQuery.get(str(chileData.query_id))

                resultDir = "../results/rankingDumps/ChileSAT/highschool/" + root.replace(chileHighschoolDir, "")

                rankAndDump(chileData.protectedCandidates,
                            chileData.nonprotectedCandidates,
                            chileData.length,
                            "ChileSATHighschool_",
                            resultDir,
                            pairsOfPAndAlpha)


def rankAndDump(protected, nonProtected, k, dataSetName, directory, pairsOfPAndAlpha):
    """
    creates all rankings we need for one experimental data set and writes them to disk to be used later

    @param protected:        list of protected candidates, assumed to satisfy in-group monotonicty
    @param nonProtected:     list of non-protected candidates, assumed to satisfy in-group monotonicty
    @param k:                length of the rankings we want to create
    @param dataSetName:      determines which data set is used in this experiment
    @param directory:        directory in which to store the rankings
    @param pairsOfPAndAlpha: contains the mapping from a given p to the corrected alpha. The alpha
                             correction depends on p and k

    The experimental setting is as follows: for a given data set of protected and non-
    protected candidates we create the following rankings:
    * a colorblind ranking,
    * a ranking as in Feldman et al
    * rankings using our FairRankingCreator, one for each pair of p and alpha in @param pairsOfPAndAlpha

    """
    print("====================================================================")
    print("create rankings of {0}".format(dataSetName))

    if not os.path.exists(os.getcwd() + '/' + directory + '/'):
        os.makedirs(os.getcwd() + '/' + directory + '/')

    print("colorblind ranking")
    colorblindRanking, colorblindNotSelected = buildFairRanking(k, protected, nonProtected, ESSENTIALLY_ZERO, 0.1)
    writePickleToDisk(colorblindRanking, os.getcwd() + '/' + directory + '/' + dataSetName + 'ColorblindRanking.pickle')
    writePickleToDisk(colorblindNotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'ColorblindRankingNotSelected.pickle')
    print(" [Done]")

    print("fair rankings")
    for p, alpha in pairsOfPAndAlpha:
        print('p=' + str(p) + '; alpha=' + str(alpha))
        fairRanking, fairNotSelected = buildFairRanking(k, protected, nonProtected, p, alpha)
        writePickleToDisk(fairRanking, os.getcwd() + '/' + directory + '/' + dataSetName + 'FairRanking_p=' + str(p) + '.pickle')
        writePickleToDisk(fairNotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'NotSelected_p=' + str(p) + '.pickle')
    print(" [Done]")

    print("feldman ranking")
    feldmanRanking, feldmanNotSelected = fair_ranker.create.feldmanRanking(protected, nonProtected, k)
    writePickleToDisk(feldmanRanking, os.getcwd() + '/' + directory + '/' + dataSetName + 'FeldmanRanking.pickle')
    writePickleToDisk(feldmanNotSelected, os.getcwd() + '/' + directory + '/' + dataSetName + 'FeldmanRankingNotSelected.pickle')
    print(" [Done]")


if __name__ == '__main__':
    main()
