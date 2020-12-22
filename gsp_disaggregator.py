#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This implements GSP energy disaggregation method proposed in the paper "On a training-less solution for non-intrusive appliance load monitoring using graph signal processing"

Created on Thu Feb  1 15:42:41 2018

@author: haroonr
"""
from __future__ import division
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import gsp_support as gsp
import matplotlib.pyplot as plt
from config import get_disagg_settings, DisaggSettings

#%%
print("Loading settings")
house_num = 2
settings = get_disagg_settings(house_num)

print("1 of 6> reading data")
#csvfileaggr = "./output_aggr.csv"
#csvfiledisaggr = "./output_disaggr.csv"
csvfileaggr = "./dataset/house_2/output_aggr.csv"
csvfiledisaggr = "./dataset/house_2/output_disaggr.csv"
df = pd.read_csv(csvfileaggr, index_col = "Time") # read demo file with aggregated active power
df.index = pd.to_datetime(df.index)
dfd = pd.read_csv(csvfiledisaggr, index_col = "Time") # read file with ground truth disaggregated appliances
dfd.index = pd.to_datetime(dfd.index)

#settings.end_time = '2011-05-02' # to 2011-05-01
mask = (df.index > settings.start_time) & (df.index < settings.end_time)
df = df.loc[mask]
mask = (dfd.index > settings.start_time) & (dfd.index < settings.end_time)
dfd = dfd.loc[mask]

fig, axs = plt.subplots(3, 1, sharex=True)
axs[0].plot(df)
axs[0].set_title("Aggregated power of house 2 from April 23th to 30th 2011, downsampled to 1 minute", size=8)
axs[1].stackplot(dfd.index, dfd.values.T, labels = list(dfd.columns.values))
axs[1].set_title("Disaggregated appliance power [Ground Truth]", size=8)
axs[1].legend(loc='upper left', fontsize=6)

#%%
main_val = df.values # get only readings
main_ind = df.index  # get only timestamp
data_vec =  main_val
signature_database = "signature_database_labelled.csv" #the signatures were extracted of power analysis from April 28th to 30th
threshold = 2000 # threshold of DTW algorithm used for appliance power signature matching

delta_p = [round(data_vec[i+1] - data_vec[i], 2) for i in range(0, len(data_vec) - 1)]
event =  [i for i in range(0, len(delta_p)) if (delta_p[i] > settings.T_Positive or delta_p[i] < settings.T_Negative) ]
np.savetxt('d_events.txt', np.array(event, dtype=np.dtype(np.int32)).astype(int), fmt='%i')
print('Events is {}'.format(len(event)))
# initial and refined clustering block of Figure 1 in the paper
print('Clusters with {} {} {} {}'.format(len(event), len(delta_p), settings.sigma, settings.ri))
clusters = gsp.refined_clustering_block(event, delta_p, settings.sigma, settings.ri)
print('Expected {} got {}'.format(len(event), sum([len(c) for c in clusters])))
print('Got {} clusters'.format(len(clusters)))

# Feature matching block of Figure 1 in the paper
finalclusters, pairs = gsp.pair_clusters_appliance_wise(clusters, data_vec, delta_p, settings.instancelimit)
print('Found {} pairs'.format(pairs))
print('Got {} clusters and {} final clusters'.format(len(clusters), len(finalclusters)))
appliance_pairs = gsp.feature_matching_module(pairs, delta_p, finalclusters, settings.alpha, settings.beta)

# create appliance wise disaggregated series
power_series, appliance_signatures = gsp.generate_appliance_powerseries(appliance_pairs, delta_p)

# label the disaggregated appliance clusters by comparing with signature DB
#labeled_appliances = gsp.label_appliances(appliance_signatures, signature_database, threshold)

# Attach timestamps to generated series
power_timeseries = gsp.create_appliance_timeseries(power_series, main_ind)

# create pandas dataframe of all series
gsp_result = pd.concat(power_timeseries, axis = 1)

labels = ['None' for i in range(len(gsp_result.columns))]
#labels = [(labeled_appliances[i] if i in labeled_appliances else 'Unknown') for i in range(len(gsp_result.columns))]
#labels= [i[1] for i in list(labeled_appliances.items())]

#gsp_result.columns = labels

axs[2].stackplot(gsp_result.index, gsp_result.values.T, labels=labels)
axs[2].set_title("Disaggregated appliance [Results]", size=8)
axs[2].legend(loc='upper left', fontsize=6)

#gsp_result.plot(kind='area', stacked=True, title='stacked appliances power', label=labeled_appliances)
#gsp_result.plot(subplots=True, layout=(2,1))
print("6 of 6> plotting the input and results :)")
print('Delta p is {}'.format(len(delta_p)))
print('Events is {}'.format(len(event)))
print(event[0:10])

plt.show()

gsp.calculate_energy_pct(dfd, gsp_result)
