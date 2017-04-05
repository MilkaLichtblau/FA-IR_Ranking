'''
Created on Jan 23, 2017

@author: meike.zehlike
'''
import numpy as np
from utilsAndConstants.utils import countProtected


def selectionUnfairness(ranking, notSelected):
    """
    calculates the difference in qualification of the last candidate in the ranking and the first
    one that was not selected for the ranking.

    @param ranking: the ranking to be measured
    @param notSelected: a list of all candidates that were not selected for the ranking, ordered by
                        qualification

    Return
    ------
    0 if the last one selected actually has a higher qualification than the first one not selected,
    because then no unfairness against somebody who was better occurred

    otherwise a negative number that tells, how much lower the qualification of the first not selected
    candidate was compared to the qualification of the last selected.
    Hence only lower than 0, if a protected candidate was to be preferred over a non-protected due
    to the ranked group fairness constraint.

    """
    if not notSelected:
        # in case their are no more not-selected candidates
        return 0
    else:
        # find the first selected one with a lower qualification than the non-selected one
        for i in range(1, len(ranking) + 1):
            if ranking[-i].originalQualification < notSelected[0].originalQualification:
                return notSelected[0].originalQualification - ranking[-i].originalQualification
        return 0


def orderingUnfairness(ranking):
    """
    calculates the maximum positional difference between a protected candidate that was rated higher
    than a non-protected candidate due to their protected status. Hence the protected candidate is
    put onto a higher position, even though their qualification is lower.

    Return
    ------
    maxRankDrop : int
        The maximum of which a candidate was ranked down

    highestScoreDiff : float
        The maximal score inversion, i.e. finds the maximum quality difference between someone who was
        ranked higher but actually has a lower score

    Note that the maximum position difference and maximum score difference does not necessarily
    belong to the same two candidates, i.e. they are independent metrics.

    Example (N stands for non-protected, P for protected, number in brackets is qualification):

    given ranking    colorblind
    ---------------------------
    1. N(1000)           1.
    2. P(996)            3.
    3. N(998)            4.
    4. N(997)            2.
    5. N(995)            5.
    6. N(994)            6.
    7. P(990)            9.
    8. P(989)            10.
    9. N(993)            7.
    10.N(993)            8.

    The highest score difference of ordering unfairness is 4 (between 8. and 9).
    The highest position difference is 2 (between 9. and 7., 10. and 8.).


    """
    colorblind = sorted(ranking, key=lambda candidate: candidate.originalQualification, reverse=True)
    maxRankDrop = 0
    highestScoreDiff = 0
    for i, candidate in enumerate(ranking):
        if not candidate is colorblind[i]:
            # some order inversion found
            colorblindOrigQual = colorblind[i].originalQualification
            if candidate.originalQualification < colorblindOrigQual:
                # the candidate from the ranking has a higher position even though their qualification
                # is worse than the one that should appear here --> find the actual position of the
                # one that should appear here if rated by qualification
                actualIdxOfColorblind = __findIndexOfCandidateByID(ranking, colorblind[i].uuid)
                # the protected candidate right above the non-protected, that was rated down should have the lowest
                # score above the non-protected, otherwise in-group monotonicity would be violated
                indexOfWorstAboveMe = __findFirstWorseCandidateAboveMe(ranking,
                                                                       colorblindOrigQual,
                                                                       actualIdxOfColorblind)
                currentScoreDiff = colorblindOrigQual - ranking[indexOfWorstAboveMe].originalQualification
                highestScoreDiff = max(highestScoreDiff, currentScoreDiff)
                maxRankDrop = max(maxRankDrop, actualIdxOfColorblind - i)

    return maxRankDrop, highestScoreDiff


def feldmanOrderingUnfairness(ranking):
    """
    a feldman ranking is a special case because it changes the scores into both directions, i.e.
    it's not only increasing but also decreasing the scores, if necessary to adjust the qualification
    distribution of the protected and non-protected group
    That means that protected candidates can be rated up in the first half and rated down in the second
    half of the created ranking
    """
    colorblind = sorted(ranking, key=lambda candidate: candidate.originalQualification, reverse=True)
    highestPosDiff = 0
    highestScoreDiff = 0
    for i, candidate in enumerate(ranking):
        if candidate.qualification != candidate.originalQualification:
            # the candidates qualification was changed to put them into a different position
            colorblindOrigQual = colorblind[i].originalQualification
            if candidate.originalQualification < colorblindOrigQual:
                # the candidate from the ranking has a higher position even though their qualification
                # is worse than the one that should appear here --> find the actual position of the
                # one that should appear here if rated by qualification
                actualIdxOfColorblind = __findIndexOfCandidateByID(ranking, colorblind[i].uuid)
                # the protected candidate right above the non-protected, that was rated down should have the lowest
                # score above the non-protected, otherwise in-group monotonicity would be violated
                indexOfWorstAboveMe = __findFirstWorseCandidateAboveMe(ranking,
                                                                       colorblindOrigQual,
                                                                       actualIdxOfColorblind)
                highestScoreDiff = max(highestScoreDiff, abs(ranking[indexOfWorstAboveMe].originalQualification - colorblindOrigQual))
                highestPosDiff = max(highestPosDiff, abs(actualIdxOfColorblind - i))

    return highestPosDiff, highestScoreDiff


def __findIndexOfCandidateByID(ranking, ident):
    for candidate in ranking:
        if candidate.uuid == ident:
            return ranking.index(candidate)
    return -1


def __findIndexOfLowestColorblind(ranking, qualification):
    """
    finds the last candidate in a ranking with a given qualification

    Example:
    1. 50
    2. 45
    3. 45
    4. 40
    5. 39

    given we are looking for qualification=45, this function would return 3

    returns -1 if the given qualification was not found
    """
    for i in range(len(ranking) - 1, -1, -1):
        if ranking[i].qualification == qualification:
            return i
    return -1


def __findFirstWorseCandidateAboveMe(ranking, myQualification, startIndex):
    i = startIndex
    while i > -1:
        if myQualification > ranking[i].qualification:
            return i
        i -= 1
    return i

# @profile
def utility(ranking, lambd):
    """
    calculates the average utility per position of a ranking by averaging the qualification of the candidates.
    In order to take the positions into account multiplies the qualification by an inverse exponential
    function, such that the ranking of better candidates to lower positions is actually penalized

    @param ranking: the ranking to be measured, containing protected and non-protected candidates
    @param lambd: a number that determines how fast the value of the positions itself decreases
                  e.g. if 0.5 the value of a position drops to almost zero within the first 100 positions
    """

    # ensure k is not zero
    k = max(1, len(ranking))

    # lambda should be dependent on k
    lambd = (lambd + k / 100) / k
    x = np.arange(0, k, 1)
    positionUtility = lambd * np.exp(-lambd * x) * 1000

#     plt.plot(x, positionUtility)
#     plt.show()
    rankingUtility = 0
    for i, candidate in enumerate(ranking):
        rankingUtility += candidate.originalQualification * positionUtility[i]

    return rankingUtility / k


def percentageOfProtected(ranking):
    return countProtected(ranking) / len(ranking)


