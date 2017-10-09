"""
Created on Jan 2, 2017

@author: meike.zehlike
"""
from dataset_creator.candidate import Candidate
import random

def create(fairnessProbability, k, numProtected, numNonProtected):
    """
    creates a set of protected candidates and a set of unprotected candidates
    merges those together into one ranked output that contains protected and unprotected candidates.

    This method was described in "Ke Yang and Julia Stoyanovich. "Measuring Fairness in Ranked Outputs."
    arXiv preprint arXiv:1610.08559 (2016)."


    @param fairnessProbability : float
        the probability that a protected candidate is chosen as the next element in rankedOutput

    @param k : int
        the size of the ranked output list

    Returns
    -------
    rankedOutput : [Candidate]
        an array of :class:`candidates <datastructure.Candidate.Candidate>` containing a fraction of
        protected ones as specified in fairnessProbability
    """

    # generate a set of protected and unprotected candidates
    protectedCandidates = generateCandidateList(True, numProtected)
    unprotectedCandidates = generateCandidateList(False, numNonProtected)

    rankedOutput = []

    # until one of the sets is empty or the output is filled with k candidates, do:
    i = 0
    while protectedCandidates and unprotectedCandidates and (i < k):
        p = random.uniform(0, 1)
        if p < fairnessProbability:
            # pop returns the last element of a list which is here the candidate with the highest
            # qualification criterion (because they are created in decreasing order)
            rankedOutput.append(protectedCandidates.pop())
        else:
            rankedOutput.append(unprotectedCandidates.pop())

        i += 1

    # if the ranked output is too short yet, fill up with remaining candidates
    while len(rankedOutput) < k and protectedCandidates:
        rankedOutput.append(protectedCandidates.pop())
    while len(rankedOutput) < k and unprotectedCandidates:
        rankedOutput.append(unprotectedCandidates.pop())

    return rankedOutput

def generateCandidateList(isProtected, numCandidates):

    candidates = []

    if isProtected:
        # i serves also as the qualification criterion of an individual candidate, even though
        # we don't need that right away
        for i in range(numCandidates):
            candidates.append(Candidate(i, ["female"]))
    else:
        for i in range(numCandidates):
            candidates.append(Candidate(i, []))

    return candidates

