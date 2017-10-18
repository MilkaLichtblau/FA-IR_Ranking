'''
Created on Mar 29, 2017

provides basic utilities for candidate rankings

@author: meike.zehlike
'''

import resource
import numpy as np


def countProtected(ranking):
    result = 0
    for candidate in ranking:
        if candidate.isProtected:
            result += 1
    return result


def normalizeQualifications(ranking):
    """normalizes candidate qualifications to be within [0, 1]"""
    # find highest qualification of candidate
    qualifications = [ranking[i].qualification for i in range(len(ranking))]
    highest = max(qualifications)
    for candidate in ranking:
        candidate.originalQualification = candidate.originalQualification / highest
        candidate.qualification = candidate.qualification / highest


def setMemoryLimit(maxMem):
    if maxMem is None:
        maxMem = -1
    try:
        resource.setrlimit(resource.RLIMIT_MEMLOCK, (1, maxMem))
        return True
    except ValueError:
        return False


def cartesian_product(*arrays):
    ndim = len(arrays)
    return np.stack(np.meshgrid(*arrays), axis=-1).reshape(-1, ndim)


class Switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
