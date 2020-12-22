from __future__ import division
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import gsp_support as gsp
import matplotlib.pyplot as plt
import sys

def graph(demo_file, demo_file_truth, gsp_result):
    fig, axs = plt.subplots(3, 1, sharex=True)
    axs[0].plot(demo_file)
    axs[0].set_title("Aggregated power of house 2 from April 23th to 30th 2011, downsampled to 1 minute", size=8)

    for i in range(demo_file_truth.values.shape[1]):
        axs[1].plot(demo_file_truth.index, demo_file_truth.values.T[i], label=demo_file_truth.columns.values[i])
#axs[1].stackplot(demo_file_truth.index, demo_file_truth.values.T, labels=list(demo_file_truth.columns.values))
    axs[1].set_title("Disaggregated appliance power [Ground Truth]", size=8)
    axs[1].legend(loc='upper left', fontsize=6)

    for i in range(gsp_result.values.shape[1]):
        axs[2].plot(gsp_result.index, gsp_result.values.T[i], label=gsp_result.columns.values[i])
#axs[2].stackplot(gsp_result.index, gsp_result.values.T, labels=labels)
    axs[2].set_title("Disaggregated appliance [Results]", size=8)
    axs[2].legend(loc='upper left', fontsize=6)
    plt.show()
