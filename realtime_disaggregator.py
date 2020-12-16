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
import sys
from config import get_disagg_settings, DisaggSettings

disagg_only = True
#%%
if len(sys.argv) < 2:
    print('Usage: python realtime_disaggregator.py [house_num]')
    exit()

print("Loading settings")
house_num = sys.argv[1]
settings = get_disagg_settings(house_num)

print("1 of 6> reading data")
csvfileaggr = 'dataset/house_{}/output_aggr.csv'.format(house_num)
csvfiledisaggr = 'dataset/house_{}/output_disaggr.csv'.format(house_num)

#csvfileaggr = "./house_2_output_aggr.csv"
#csvfiledisaggr = "./house_2_output_disaggr.csv"

demo_file = pd.read_csv(csvfileaggr, index_col="Time") # read demo file with aggregated active power
demo_file.index = pd.to_datetime(demo_file.index)
demo_file_truth = pd.read_csv(csvfiledisaggr, index_col="Time") # read file with ground truth disaggregated appliances
demo_file_truth.index = pd.to_datetime(demo_file_truth.index)

#np.set_printoptions(threshold=sys.maxsize)
#print(demo_file.values)
#exit()
# select date range
mask = (demo_file.index > settings.start_time) & (demo_file.index < settings.end_time)
demo_file = demo_file.loc[mask]
mask = (demo_file_truth.index > settings.start_time) & (demo_file_truth.index < settings.end_time)
demo_file_truth = demo_file_truth.loc[mask]


#%%
main_val = demo_file.values # get only readings
main_ind = demo_file.index  # get only timestamp
data_vec = main_val
signature_database = "signature_database_labelled.csv" #the signatures were extracted of power analysis from April 28th to 30th
threshold = 2000 # threshold of DTW algorithm used for appliance power signature matching


#Create the initial clusters from the 1st bit of data
current_time = 0
initial_data = data_vec[current_time : current_time + settings.init_size]
initial_delta_power = [round(initial_data[i + 1] - initial_data[i], 2) for i in range(0, len(initial_data) - 1)]
initial_events = [i for i in range(0, len(initial_delta_power)) if (initial_delta_power[i] > settings.T_Positive or initial_delta_power[i] < settings.T_Negative) ]
clusters = gsp.refined_clustering_block(initial_events, initial_delta_power, settings.sigma, settings.ri)
print('Expected {} got {}'.format(len(initial_events), sum([len(c) for c in clusters])))
current_time += settings.init_size

hist_delta_power= initial_delta_power
#Testing to make sure it works
clusters, pairs =  gsp.pair_clusters_appliance_wise(clusters, data_vec, hist_delta_power, settings.instancelimit)
print('Found {} pairs'.format(pairs))
appliance_pairs = gsp.feature_matching_module(pairs, hist_delta_power, clusters, settings.alpha, settings.beta)

# create appliance wise disaggregated series
power_series, appliance_signatures = gsp.generate_appliance_powerseries(appliance_pairs, hist_delta_power)

# label the disaggregated appliance clusters by comparing with signature DB
if not disagg_only:
    labeled_appliances = gsp.label_appliances(appliance_signatures, signature_database, threshold)

# Attach timestamps to generated series
power_timeseries = gsp.create_appliance_timeseries(power_series, main_ind)

# create pandas dataframe of all series
gsp_result = pd.concat(power_timeseries, axis=1)

if disagg_only:
    labels = ['None' for i in range(len(gsp_result.columns))]
else:
    labels = [(labeled_appliances[i] if i in labeled_appliances else 'Unknown') for i in range(len(gsp_result.columns))]

gsp_result.columns = labels
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
exit()
#Traverse through the data each frame at a time
current_frame = 0
event_offset = len(initial_events)
hist_delta_power= initial_delta_power
total_frames = int((len(data_vec) - settings.init_size) / frame_size)
while current_time < len(data_vec):
    #fig, axs = plt.subplots(3, 1, sharex=True)
    #axs[0].plot(demo_file)
    #axs[0].set_title("Aggregated power of house 2 from April 23th to 30th 2011, downsampled to 1 minute", size=8)
    #axs[1].stackplot(demo_file_truth.index, demo_file_truth.values.T, labels=list(demo_file_truth.columns.values))
    #axs[1].set_title("Disaggregated appliance power [Ground Truth]", size=8)
    #axs[1].legend(loc='upper left', fontsize=6)

    print('Processing frame {} of {} from times {} to {}'.format(current_frame, total_frames, current_time, current_time + frame_size))
    #The -1 is so that we have the difference from the end of the last frame
    #Otherwise, we will drop events accidentally
    frame_data = data_vec[current_time - 1 : current_time + frame_size] #This works at end case
    frame_delta_power = [round(frame_data[i + 1] - frame_data[i], 2) for i in range(0, len(frame_data) - 1)]

    #Members of frame_events are indicies
    frame_events = [i + event_offset for i in range(0, len(frame_delta_power)) if (frame_delta_power[i] > settings.T_Positive or frame_delta_power[i] < settings.T_Negative) ]
    #Prepare frames and events
    print('\tAdding {} events. Have {} existing clusters'.format(len(frame_events), len(clusters)))
    preevents = sum([len(c) for c in clusters])
    expected_edges = preevents + len(frame_events)
    hist_delta_power += frame_delta_power

    #Create/extend clusters
    clusters = gsp.extend_refined_clustering_block(clusters, frame_events, hist_delta_power, settings.sigma, settings.ri)

    #Shrink clusters so equal positive/negative
    #clusters = gsp.shrink_positive_negative(clusters, data_vec, hist_delta_power, settings.instancelimit)
    clusters, pairs =  gsp.pair_clusters_appliance_wise(clusters, data_vec, hist_delta_power, settings.instancelimit)
    appliance_pairs = gsp.feature_matching_module(pairs, hist_delta_power, clusters, settings.alpha, settings.beta)

# create appliance wise disaggregated series
    power_series, appliance_signatures = gsp.generate_appliance_powerseries(appliance_pairs, hist_delta_power)

# label the disaggregated appliance clusters by comparing with signature DB
    #if not disagg_only:
    #    labeled_appliances = gsp.label_appliances(appliance_signatures, signature_database, threshold)

# Attach timestamps to generated series
    power_timeseries = gsp.create_appliance_timeseries(power_series, main_ind)

# create pandas dataframe of all series
    gsp_result = pd.concat(power_timeseries, axis=1)

    if disagg_only:
        labels = ['None' for i in range(len(gsp_result.columns))]
    else:
        labels = [(labeled_appliances[i] if i in labeled_appliances else 'Unknown') for i in range(len(gsp_result.columns))]

    #labels = [i[1] for i in list(labeled_appliances.items())]
    gsp_result.columns = labels

    #Feature matching
    #Labeling


    #Handle frame stuff
    result_edges = sum([len(c) for c in clusters])
    p_clusters = sum([1 for c in clusters if hist_delta_power[c[0]] > 0])
    n_clusters = sum([1 for c in clusters if hist_delta_power[c[0]] < 0])

    print('\tExpected {} to {} events, got {}'.format(preevents, expected_edges, result_edges))
    print('\tEnding with {} = {}[+] + {}[-]'.format(len(clusters), p_clusters, n_clusters))

    event_offset += len(frame_events)
    current_frame += 1
    current_time += frame_size

#fig, axs = plt.subplots(3, 1, sharex=True)
#axs[0].plot(demo_file)
#axs[0].set_title("Aggregated power of house 2 from April 23th to 30th 2011, downsampled to 1 minute", size=8)
#axs[1].stackplot(demo_file_truth.index, demo_file_truth.values.T, labels=list(demo_file_truth.columns.values))
#axs[1].set_title("Disaggregated appliance power [Ground Truth]", size=8)
#axs[1].legend(loc='upper left', fontsize=6)
#axs[2].stackplot(gsp_result.index, gsp_result.values.T, labels=labels)
#axs[2].set_title("Disaggregated appliance [Results]", size=8)
#axs[2].legend(loc='upper left', fontsize=6)
#plt.show()
#finalclusters, pairs = gsp.pair_clusters_appliance_wise(clusters, data_vec, delta_power, settings.instancelimit)
#appliance_pairs = gsp.feature_matching_module(pairs, delta_power, finalclusters, settings.alpha, settings.beta)
#
## create appliance wise disaggregated series
#power_series, appliance_signatures = gsp.generate_appliance_powerseries(appliance_pairs, delta_power)
#
## label the disaggregated appliance clusters by comparing with signature DB
#labeled_appliances = gsp.label_appliances(appliance_signatures, signature_database, threshold)
#
## Attach timestamps to generated series
#power_timeseries = gsp.create_appliance_timeseries(power_series, main_ind)
#
## create pandas dataframe of all series
#gsp_result = pd.concat(power_timeseries, axis=1)
#
#labels = [i[1] for i in list(labeled_appliances.items())]
#gsp_result.columns = labels
#
#axs[2].stackplot(gsp_result.index, gsp_result.values.T, labels=labels)
#axs[2].set_title("Disaggregated appliance [Results]", size=8)
#axs[2].legend(loc='upper left', fontsize=6)
#
##gsp_result.plot(kind='area', stacked=True, title='stacked appliances power', label=labeled_appliances)
##gsp_result.plot(subplots=True, layout=(2,1))
#print("6 of 6> plotting the input and results :)")
#
#plt.show()
#
#gsp.calculate_energy_pct(demo_file_truth, gsp_result)
