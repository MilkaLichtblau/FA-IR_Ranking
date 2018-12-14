import pandas as pd
import numpy as np
import scipy.stats as stats


class AlphaAdjustment:

    def __init__(self, n: int, p: float, alpha: float):
        if n < 1:
            raise ValueError("Parameter n must be at least 1")
        if p <= 0.0 or p >= 1.0:
            raise ValueError("Parameter p must be in ]0.0, 1.0[")
        if alpha <= 0.0 or alpha > 1.0:
            raise ValueError("Parameter alpha must be in ]0.0, 1.0[")

        self.n = n
        self.p = p
        self.alpha = alpha

        self.mtable = self.compute_mtable()
        self.aux_mtable = self.compute_aux_mtable()

    def m(self, k:int):
        if k < 1:
            raise ValueError("Parameter k must be at least 1")
        elif k > self.n:
            raise ValueError("Parameter k must be at most n")

        return stats.binom.ppf(self.alpha, k, self.p)

    def compute_mtable(self):
        """ Computes a table containing the minimum number of protected elements
            required at each position

        """
        mtable = pd.DataFrame(columns=[ "m"])
#         mtable.loc[0] = 0  # test should not fail at the first position so we require no protected candidate at position 1
        for i in range(1, self.n + 1):
            if i % 2000 == 0:
                print("Computing m: {:.0f} of {:.0f}".format(i, self.n))
            mtable.loc[i] = [ self.m(i) ]
        return mtable

    def compute_aux_mtable(self):
        """ Computes an auxiliary table containing the inverse table m[i] and the block sizes

        """
        if not(isinstance(self.mtable, pd.DataFrame)):
            raise TypeError("Internal mtable must be a DataFrame")

        aux_mtable = pd.DataFrame(columns=["inv", "block"])
        last_m_seen = 0
        last_position = 0
        for position in range(1, len(self.mtable)):
            if position % 2000 == 0:
                print("Computing m inverse: {:.0f} of {:.0f}".format(position, len(self.mtable)))
            if self.mtable.at[position, "m"] == last_m_seen + 1:
                last_m_seen += 1
                aux_mtable.loc[last_m_seen] = [ position, position - last_position ]
                last_position = position
            elif self.mtable.at[position, "m"] != last_m_seen:
                raise RuntimeError("Inconsistent mtable")

        return aux_mtable

    def compute_success_probability(self):
        max_protected = self.aux_mtable["inv"].count()
        min_protected = 1

        success_obtained_prob = np.zeros(max_protected)
        success_obtained_prob[0] = 1.0

        self.success_prob_report = pd.DataFrame(columns=["prob"])
#         old_fail_probability = 0.0

        pmf_cache = pd.DataFrame(columns=["table"])
        while min_protected < max_protected:
            if min_protected % 2000 == 0:
                print("Computing success probability: block {:.0f} of {:.0f}".format(min_protected, max_protected))

            # print("*** Must have at least {:.0f} at position {:.0f} ***".format(min_protected, position))

            block_length = int(self.aux_mtable["block"][min_protected])
            # print("Block length  : {:.0f}".format(block_length))

            if block_length in pmf_cache.index:
                current_trial = pmf_cache.loc[block_length]["table"]
            else:
                current_trial = np.empty(int(block_length) + 1)
                for i in range(0, int(block_length) + 1):
                    current_trial[i] = stats.binom.pmf(i, block_length, self.p)
                pmf_cache.loc[block_length] = [ current_trial ]

            # print("** Success table so far:")
            # print(success_obtained_prob)

            # print("** Current trial probabilities:")
            # print(current_trial)

            new_success_obtained_prob = np.zeros(max_protected)
            for i in range(0, int(block_length) + 1):
                increase = np.roll(success_obtained_prob, i) * current_trial[i]
                new_success_obtained_prob += increase
            new_success_obtained_prob[min_protected - 1] = 0

            # print("** New success table:")
            # print(new_success_obtained_prob)

            success_obtained_prob = new_success_obtained_prob

            success_probability = success_obtained_prob.sum()
#             fail_probability = 1 - success_probability
            # print("Fail probability          = {:.6f}".format(fail_probability))
            # print("Fail probability delta    = {:.6f}".format(fail_probability - old_fail_probability))
            self.success_prob_report.loc[self.aux_mtable["inv"][min_protected]] = success_probability

            success_obtained_prob = new_success_obtained_prob
#             old_fail_probability = 1 - success_probability

            min_protected += 1

        return success_probability

# Example

# n = 5000
# p = 0.9
# alpha = 0.0072
#
# fc = AlphaAdjustment(n=n, p=p, alpha=alpha)
# print("Success probability for n={:.0f}, p={:.2f}, alpha={:.6f}: {:.10f}".format(n, p, alpha, fc.compute_success_probability()))

