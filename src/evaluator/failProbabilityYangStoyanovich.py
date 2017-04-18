'''
Created on Apr 12, 2017

@author: meike.zehlike
'''
from utilsAndConstants import printsAndPlots
from datasetCreator import yangStoyanovichMethod
from ranker.testFairnessInRankings import FairnessInRankingsTester

def determineFailProbOfGroupFairnessTesterForStoyanovichRanking():
    """
    determines the probability that the ranked group fairness test fails given an artificial dataset
    created by means of Yang and Stoyanovich ("Ke Yang and Julia Stoyanovich. "Measuring Fairness in
    Ranked Outputs." arXiv preprint arXiv:1610.08559 (2016).") which we believe to be fair.

    """
    numTrials = 10000  # Set to 100 or 10,000
    alpha = 0.01
    k = 1000  # Set to 1000

#     resultFile = open('resultFailuresYangStoyanovichK={0}.csv'.format(k), 'w')
#     wr = csv.writer(resultFile, delimiter=',')
    modelAlpha1 = [0.075378, 0.090049, 0.098331, 0.100432, 0.103713, 0.103976, 0.105475, 0.103502, 0.099602]
    modelAlpha2 = [0.295883, 0.330252, 0.349234, 0.361767, 0.360710, 0.362456, 0.360749, 0.356852, 0.328008]


    failProbs1 = []
    failProbs2 = []
    ps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    print("numTrials={0}".format(numTrials))

    # percentage describes the generated amount of protected candidates
    for p in ps:
        print("currently running: k={0}, p={1}, alpha={2}".format(k, p, alpha))
        result, expectedCandidates = rankedGroupFairnessInYangStoyanovich(
            alpha, p, k, k, k, numTrials)
        sumOfFailures = sum(result)
        failProb = sumOfFailures / numTrials
        failProbs1.append(failProb)

    for p in ps:
        print("currently running: k={0}, p={1}, alpha={2}".format(k + 500, p, alpha + 0.04))
        result, expectedCandidates = rankedGroupFairnessInYangStoyanovich(
            alpha + 0.04, p, k + 500, k + 500, k + 500, numTrials)
        sumOfFailures = sum(result)
        failProb = sumOfFailures / numTrials
        failProbs2.append(failProb)

    printsAndPlots.plotTwoListsInOnePlot(ps, modelAlpha1, failProbs1, modelAlpha2, failProbs2, 'p', 'prob. rejection', filename='failProbs.pdf')


def rankedGroupFairnessInYangStoyanovich(alpha, p, k, numberProtected, numberNonProtected, trials):
    result = [0] * k
    gft = FairnessInRankingsTester(p, alpha, k, correctedAlpha=True)

    for idx in range(trials):
        rankedOutput = yangStoyanovichMethod.create(p, k, numberProtected, numberNonProtected)
        posAtFail, isFair = gft.rankedGroupFairnessCondition(rankedOutput)
        if not isFair:
            result[posAtFail] += 1

    return result, gft.candidatesNeeded
