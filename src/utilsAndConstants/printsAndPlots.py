'''
Created on Apr 12, 2017

@author: meike.zehlike
'''

import matplotlib as mpl
from matplotlib import pyplot as plt

def plotTwoListsInOnePlot(xdata, ydata1, ydata2, ydata3, ydata4, xlabel, ylabel, filename):
    mpl.rcParams.update({'font.size': 20, 'lines.linewidth': 3})
    plt.plot(xdata, ydata1, c='r')
    plt.scatter(xdata, ydata2, marker='x', c='r')
    plt.plot(xdata, ydata3, c='b')
    plt.scatter(xdata, ydata4, marker='x', c='b')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    if filename:
        plt.savefig(filename)
    else:
        plt.show()