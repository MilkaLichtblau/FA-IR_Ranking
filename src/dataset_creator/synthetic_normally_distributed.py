'''
Created on Oct 3, 2017

@author: meike.zehlike

'''
import numpy as np
from utilsAndConstants import printsAndPlots


def create_multinomial(num_groups, mean_diff=50, var_diff=0):
    """
    creates synthetic training data for learning to rank. The score data is normally distributed and
    the means for each groups vary by mean_diff points. Scores are integers.

    @param num_groups:    the number of groups (assumes one non-protected, rest protected) in the data
    @param mean_diff:     desired difference of means for each group
    @param var_diff:      difference in variances per group
    """
    data = {}
    sigma = 100
    for mu in range(0, mean_diff * num_groups, mean_diff):
        score_data = np.random.normal(mu, sigma, 10000)
        score_data = score_data.round().astype(int)
        data[mu] = score_data
        sigma += var_diff

    printsAndPlots.plot_two_histograms(data[0], data[50])
