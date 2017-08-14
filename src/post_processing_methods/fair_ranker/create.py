'''
Created on Jan 17, 2017

@author: meike.zehlike
'''

from post_processing_methods.fair_ranker.test import FairnessInRankingsTester
from scipy.stats.stats import percentileofscore
from scipy.stats.stats import scoreatpercentile
from utilsAndConstants.constants import ESSENTIALLY_ZERO


def feldmanRanking(protectedCandidates, nonProtectedCandidates, k):
    """
    creates a ranking that promotes the protected candidates by adjusting the distribution of the
    qualifications of the protected and non-protected group

    IMPORTANT: THIS METHOD MODIFIES THE ORIGINAL LIST OF PROTECTED CANDIDATES!
    I.e. it modifies the qualification of the
    protected candidates. If the original list has to be preserved, it has to be deep-copied into a
    new data structure, before handed over into this method.

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

    # create a colorblind ranking
    return fairRanking(k, protectedCandidates, nonProtectedCandidates, ESSENTIALLY_ZERO, 0.1)


def fairRanking(k, protectedCandidates, nonProtectedCandidates, minProp, alpha):
    """
    creates a ranked output that satisfies the fairness definition in :class:'FairnessInRankingsTester'
    if k is larger than one of the candidate lists we have available, the ranking is filled up with
    candidates from the other group, i.e. if all protected candidates already appear in the ranking
    the left over positions are filled with non-protected

    Parameters:
    ----------
    k : int
        the expected length of the ranking

    protectedCandidates : [Candidates]
        array of protected class:`candidates <datasetCreator.candidate.Candidate>`, assumed to be
        sorted by candidate qualification in descending order

    nonProtectedCandidates : [Candidates]
        array of non-protected class:`candidates <datasetCreator.candidate.Candidate>`, assumed to be
        sorted by candidate qualification in descending order

    minProp : float
        minimal proportion of protected candidates to appear in the fair ranking result

    alpha : float
        significance level for the binomial cumulative distribution function -> minimum probability at
        which a fair ranking contains the minProp amount of protected candidates

    Return:
    ------
    an array of class:`candidates <datasetCreator.candidate.Candidate>` that maximizes ordering and
    selection fairness

    the left-over candidates that were not selected into the ranking, sorted color-blindly
    """


    result = []
    gft = FairnessInRankingsTester(minProp, alpha, k, correctedAlpha=True)
    countProtected = 0

    idxProtected = 0
    idxNonProtected = 0

    for i in range(k):
        if idxProtected >= len(protectedCandidates) and idxNonProtected >= len(nonProtectedCandidates):
            # no more candidates available, return list shorter than k
            return result, []
        if idxProtected >= len(protectedCandidates):
            # no more protected candidates available, take non-protected instead
            result.append(nonProtectedCandidates[idxNonProtected])
            idxNonProtected += 1

        elif idxNonProtected >= len(nonProtectedCandidates):
            # no more non-protected candidates available, take protected instead
            result.append(protectedCandidates[idxProtected])
            idxProtected += 1
            countProtected += 1

        elif countProtected < gft.candidates_needed[i]:
            # add a protected candidate
            result.append(protectedCandidates[idxProtected])
            idxProtected += 1
            countProtected += 1

        else:
            # find the best candidate available
            if protectedCandidates[idxProtected].qualification >= nonProtectedCandidates[idxNonProtected].qualification:
                # the best is a protected one
                result.append(protectedCandidates[idxProtected])
                idxProtected += 1
                countProtected += 1
            else:
                # the best is a non-protected one
                result.append(nonProtectedCandidates[idxNonProtected])
                idxNonProtected += 1

    return result, __mergeTwoRankings(protectedCandidates[idxProtected:], nonProtectedCandidates[idxNonProtected:])


def __mergeTwoRankings(ranking1, ranking2):
    result = ranking1 + ranking2
    result.sort(key=lambda candidate: candidate.originalQualification, reverse=True)
    return result



