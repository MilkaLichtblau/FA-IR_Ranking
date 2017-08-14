'''
Created on Jan 11, 2017

@author: meike.zehlike
'''
from scipy.stats import binom
from utilsAndConstants.utils import countProtected
from post_processing_methods.fair_ranker.alpha_adjustment import AlphaAdjustment

class FairnessInRankingsTester():
    """
    implementation of the statistical significance test that decides if a ranking has a fair representation
    and ordering of protected candidates with respect to non-protected ones.

    The test is based on the cumulative distribution function of a binomial distribution, i.e. on a
    Bernoulli process which we believe is fair.
    A ranking is accepted as fair, if it fairly represents protected candidates over all prefixes of
    the ranking.
    To fairly represent the protected group in a prefix the test compares the actual number of protected
    candidates in the given ranking prefix to the number that would be obtained with a probability of
    p by random Bernoulli trials. If these numbers do not differ too much, the fair representation
    condition accepts this prefix. If this holds for every prefix, the entire ranking is accepted
    as fair.
    """

    @property
    def candidates_needed(self):
        return self.__candidatesNeeded


    @property
    def minimal_proportion(self):
        return self.__minProp


    def __init__(self, minProp, alpha, k, correctedAlpha):
        """

        @param minProp : float
            the minimal proportion of protected candidates that the set should have

        @param alpha : float
            significance level for the binomial cumulative distribution function -> minimum probability at
            which a fair ranking contains the minProp amount of protected candidates

        @param k : int
            the expected length of the ranked output

        @param correctedAlpha : bool
        FIXME: guck nochmal, warum man die Korrektur überhaupt nicht wollen würde
            tells if model adjustment shall be used or not
        """
        self.__minProp = minProp
        self.__alpha = alpha
        if correctedAlpha:
            self.__candidatesNeeded = self.__candidates_needed_with_correction(k)
        else:
            self.__candidatesNeeded = self.__calculate_protected_needed_at_each_position(k)


    def ranked_group_fairness_condition(self, ranking):
        """
        checks that every prefix of a given ranking tau satisfies the fair representation condition
        starts to check from the top of the list (i.e. with the first candidate) and expands downwards
        breaks as soon as it finds a prefix that is unfair

        Parameters:
        ----------
        ranking : [Candidate]
            the set to be checked for fair representation

        Return:
        ------
        True if the ranking has a fair representation of the protected group for each prefix
        False and the index at which the fair representation condition was not satisfied
        """

        prefix = []

        for t in range(len(ranking)):
            prefix.append(ranking[t])
            if not self.fair_representation_condition(prefix):
                return t, False

        return 0, True


    def fair_representation_condition(self, ranking):
        """
        checks if a given ranking with tau_p protected candidates fairly represents the protected group. A
        minimal proportion of protected candidates is defined in advance.

        Parameters:
        ----------
        ranking : [Candidate]
        the set to be checked for fair representation

        Return:
        ------
        True if the ranking fairly represents the protected group, False otherwise
        """

        t = len(ranking)
        numberProtected = countProtected(ranking)

        if self.__candidatesNeeded[t - 1] > numberProtected:
            # not enough protected candidates in my ranking
            return False
        else:
            return True


    def __calculate_protected_needed_at_each_position(self, k):
        result = []

        if self.__minProp == 0:
            # handle special case minProp = 0
            result = [0] * k
        else:
            for n in range(1, k + 1):
                numProtCandidates = binom.ppf(self.__alpha, n, self.__minProp)
                result.append(int(numProtCandidates))

        return result


    def __candidates_needed_with_correction(self, k):
        fc = AlphaAdjustment(k, self.__minProp, self.__alpha)
        mtableAsList = fc.mtable.m.tolist()
        mtableAsList = [int(i) for i in mtableAsList]
        return mtableAsList

