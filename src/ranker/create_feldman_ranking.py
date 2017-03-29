'''
Created on Feb 1, 2017

@author: meike.zehlike
'''
from scipy.stats.stats import percentileofscore
from scipy.stats.stats import scoreatpercentile
from ranker.create_FAIR_ranking import createFairRanking
from utils_and_constants.constants import ESSENTIALLY_ZERO


def createFeldmanRanking(protectedCandidates, nonProtectedCandidates, k):
    """
    creates a ranking that promotes the protected candidates by adjusting the distribution of the
    qualifications of the protected and non-protected group

    steps:
        1. take a protected candidate x
        2. determine the percentile of that candidate within their group percentile(x)
        3. find a non-protected candidate y that has the same percentile(y) == percentile(x)
        4. assign the score of y to x
        5. goto 1

    Parameters:
    ----------
    :param protectedCandidates: array of protected candidates
    :param nonProtectedCandidates: array of non-protected candidates
    :param k: length of the ranking to return

    Return:
    ------
    a ranking of protected and non-protected candidates, which tries to have a better share of
    protected and non-protected candidates
    """

    # ensure candidates are sorted by descending qualificiations
    protectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)
    nonProtectedCandidates.sort(key=lambda candidate: candidate.qualification, reverse=True)


    protectedQualifications = [protectedCandidates[i].qualification for i in range(len(protectedCandidates))]
    nonProtectedQualifications = [nonProtectedCandidates[i].qualification for i in range(len(nonProtectedCandidates))]


    # create same distribution for protected and non-protected candidates
    for i, candidate in enumerate(protectedCandidates):
        if i >= k:
            # only need to adapt the scores for protected candidates up to required length
            # the rest will not be considered anyway
            break
        # find percentile of protected candidate
        p = percentileofscore(protectedQualifications, candidate.qualification)
        # find score of a non-protected in the same percentile
        score = scoreatpercentile(nonProtectedQualifications, p)
        candidate.qualification = score

    return createFairRanking(k, protectedCandidates, nonProtectedCandidates, ESSENTIALLY_ZERO, 0.1)


