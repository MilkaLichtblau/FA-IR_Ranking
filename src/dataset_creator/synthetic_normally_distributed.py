'''
Created on Oct 3, 2017

@author: meike.zehlike

'''
import numpy as np
from utilsAndConstants import printsAndPlots


def create_multinomial(num_groups, mean_diff=50, std_dev_diff=0):
    """
    creates synthetic training data for learning to rank. The score data is normally distributed and
    the means for each groups vary by mean_diff points. Scores are integers.

    @param num_groups:    the number of groups (assumes one non-protected, rest protected) in the data
    @param mean_diff:     desired difference of means for each group
    @param std_dev_diff:      difference in variances per group

    @return: dictionary with group_number as key and arrays of size 10000 with normally distributed data
             points (integers) as value
    """
    data = {}
    sigma = 100
    mu = 0
    for group in range(0, num_groups):
        score_data = np.random.normal(mu, sigma, 10000)
        data[group] = score_data.round().astype(int)

        sigma += std_dev_diff
        mu += mean_diff

#    printsAndPlots.plot_two_histograms(data[0], data[1])

    return data
