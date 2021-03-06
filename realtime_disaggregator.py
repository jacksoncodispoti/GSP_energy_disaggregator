#!/usr/bin/env python
from __future__ import division
import warnings

from pandas.core.frame import DataFrame
from pandas.core.generic import NDFrame
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import gsp_support as gsp
import gsp_visualize as gsp_v
import matplotlib.pyplot as plt
import sys
from config import get_disagg_settings, DisaggSettings
from identifier import Identifier
from matcher import Matcher

disagg_only = True

#If we do a naive clone like list(clusters), it still has 2nd level lists that are referencing
#The same things
def clone_clusters(clusters):
    res = [[]]

    for cluster in clusters:
        for edge in cluster:
            res[-1].append(edge)

        res.append([])

    return res

def aggregate_results(clusters, data_vec, hist_delta_power, settings):
    #We need to clone it so that the underlying 'algorithms' don't change our existing clusters
    agg_clusters = clone_clusters(clusters)
    finalclusters, a_pairs = gsp.pair_clusters_appliance_wise(agg_clusters, data_vec, hist_delta_power, settings.instancelimit)
    appliance_pairs = gsp.feature_matching_module(a_pairs, hist_delta_power, finalclusters, settings.alpha, settings.beta)

    # create appliance wise disaggregated series
    power_series, appliance_signatures = gsp.generate_appliance_powerseries(appliance_pairs, hist_delta_power)

    # Attach timestamps to generated series
    power_timeseries = gsp.create_appliance_timeseries(power_series, main_ind)

    # create pandas dataframe of all series
    gsp_result = pd.concat(power_timeseries, axis=1)

    if disagg_only:
        labels = ['appliance_{}'.format(i) for i in range(len(gsp_result.columns))]
    else:
        # label the disaggregated appliance clusters by comparing with signature DB
        labeled_appliances = gsp.label_appliances(appliance_signatures, signature_database, threshold)
        labels = [(labeled_appliances[i] if i in labeled_appliances else 'Unknown') for i in range(len(gsp_result.columns))]

    #labels = [i[1] for i in list(labeled_appliances.items())]
    gsp_result.columns = labels
    #We don't want it for all days when we only processed half
    gsp_result = gsp_result.iloc[0:len(hist_delta_power)]

    return gsp_result

if len(sys.argv) < 2:
    print('Usage: python realtime_disaggregator.py [house_num]')
    print('This program is for disaggregating the aggregate power readings for specified house')
    sys.exit()

print("Loading settings")
house_num = sys.argv[1]
settings = get_disagg_settings(house_num)

print("\t1 of 6> reading data")
csvfileaggr = 'dataset/house_{}/output_aggr.csv'.format(house_num)
csvfiledisaggr = 'dataset/house_{}/output_disaggr.csv'.format(house_num)
csvfileresponse = 'dataset/house_{}/output_response.csv'.format(house_num)

demo_file = pd.read_csv(csvfileaggr, index_col="Time")
demo_file.index = pd.to_datetime(demo_file.index)
demo_file_truth = pd.read_csv(csvfiledisaggr, index_col="Time")
demo_file_truth.index = pd.to_datetime(demo_file_truth.index)

# select date range
mask = (demo_file.index > settings.start_time) & (demo_file.index < settings.end_time)
demo_file = demo_file.loc[mask]
mask = (demo_file_truth.index > settings.start_time) & (demo_file_truth.index < settings.end_time)
demo_file_truth: DataFrame = demo_file_truth.loc[mask]

main_val = demo_file.values # get only readings
main_ind = demo_file.index  # get only timestamp
data_vec = main_val
signature_database = "signature_database_labelled.csv"
threshold = 2000 # threshold of DTW algorithm used for appliance power signature matching

#Create the initial clusters from the 1st bit of data
extra_amount = 0

identifier = Identifier(settings.T_Positive, csvfileresponse)
matcher = Matcher(5, [c for c in demo_file_truth.columns], ['refrigerator'], 2)

#Try to create a set of initial clusters, re-try until SVD divergence stops
while True:
    current_time = 0
    initial_data = data_vec[current_time : current_time + settings.init_size - extra_amount]
    initial_delta_power = [np.round(initial_data[i + 1] - initial_data[i], 2) for i in range(len(initial_data) - 1)]
    initial_events = [i for i in range(len(initial_delta_power)) if (initial_delta_power[i] > settings.T_Positive or initial_delta_power[i] < settings.T_Negative) ]

    try:
        trial_clusters = gsp.refined_clustering_block(initial_events, initial_delta_power, settings.sigma, settings.ri)
        print('There were {} initial events, {} power'.format(len(initial_events), len(initial_delta_power)))
        print('Trial clusters are {}'.format(trial_clusters))
        break
    except np.linalg.LinAlgError:
        extra_amount += 1
        print("SVD didn't converge, retrying with {} less data".format(extra_amount))
        continue

print('Expected {} got {}'.format(len(initial_events), sum([len(c) for c in trial_clusters])))
current_time += settings.init_size - extra_amount

hist_delta_power= initial_delta_power
trial_clusters, pairs =  gsp.pair_clusters_appliance_wise(trial_clusters, data_vec, hist_delta_power, settings.instancelimit)
print('Found {} pairs'.format(pairs))

#Traverse through the data each frame at a time
current_frame = 0
event_offset = len(initial_events)
hist_events = initial_events
hist_delta_power= initial_delta_power
total_frames = int((len(data_vec) - settings.init_size) / settings.frame_size)

while current_time < len(data_vec):
    print('Processing frame {} of {} from times {} to {}'.format(current_frame, total_frames, current_time, current_time + settings.frame_size))
    #The -1 is so that we have the difference from the end of the last frame
    #Otherwise, we will drop events accidentally
    frame_data = data_vec[current_time - 1 : current_time + settings.frame_size] #This works at end case
    frame_delta_power = [np.round(frame_data[i + 1] - frame_data[i], 2) for i in range(0, len(frame_data) - 1)]

    print('\tDisaggregating appliances')
    #Members of frame_events are indicies
    frame_events = [i + current_time - 1 for i in range(0, len(frame_delta_power)) if (frame_delta_power[i] > settings.T_Positive or frame_delta_power[i] < settings.T_Negative) ]
    #Prepare frames and events
    print('\t\tAdding {} events. Have {} existing clusters'.format(len(frame_events), len(trial_clusters)))
    preevents = sum([len(c) for c in trial_clusters])
    expected_edges = preevents + len(frame_events)
    hist_delta_power += frame_delta_power
    hist_events += frame_events

    #Create/extend clusters
    #clusters = gsp.refined_clustering_block(hist_events, hist_delta_power, settings.sigma, settings.ri)
    print("hist deltap {}".format(len(hist_delta_power)))
    print("frame events {}".format(frame_events))
    trial_clusters = gsp.extend_refined_clustering_block(trial_clusters, frame_events, hist_delta_power, settings.sigma, settings.ri)

    #The line below modifies the results somehow which screws everything up
    gsp_results: NDFrame = aggregate_results(trial_clusters, data_vec, hist_delta_power, settings)
    gsp_truth: NDFrame = demo_file_truth[0:len(gsp_results)]
    #identifier.process_frame(current_frame, settings.frame_size, gsp_results)
    #matcher.process_frame(current_frame, settings.frame_size, gsp_results, gsp_truth)
    matcher.process_frame(current_time, settings.frame_size, gsp_truth, gsp_truth)

    #gsp_v.graph(demo_file, demo_file_truth, gsp_results)

    #Shrink clusters so equal positive/negative
#    clusters = gsp.shrink_positive_negative(clusters, data_vec, hist_delta_power, settings.instancelimit)

    #gsp_results = aggregate_results(clusters, data_vec, hist_delta_power, settings)
    #gsp_v.graph_all(demo_file, demo_file_truth, gsp_results)
    #exit()

    #Handle frame stuff
    result_edges = sum([len(c) for c in trial_clusters])
    p_clusters = sum([1 for c in trial_clusters if hist_delta_power[c[0]] > 0])
    n_clusters = sum([1 for c in trial_clusters if hist_delta_power[c[0]] < 0])

    print('\t\tExpected {} to {} events, got {}'.format(preevents, expected_edges, result_edges))
    print('\t\tEnding with {} = {}[+] + {}[-]'.format(len(trial_clusters), p_clusters, n_clusters))

    event_offset += len(frame_events)
    current_frame += 1
    current_time += settings.frame_size

#np.savetxt('r_events.txt', np.array(hist_events).astype(int), fmt='%i')
#print('Clusters with {} {} {} {}'.format(len(hist_events), len(hist_delta_power), settings.sigma, settings.ri))
#clusters = gsp.refined_clustering_block(hist_events, hist_delta_power, settings.sigma, settings.ri)
print('\tEnding at {}'.format(current_time))
#gsp_results = aggregate_results(trial_clusters, data_vec, hist_delta_power, settings)
gsp_results = matcher.final_matching(gsp_truth)
matcher.print_question_pool()
#gsp_results = matcher.final_matching()

#identifier.process_frame(current_frame, settings.frame_size, gsp_results)
gsp_v.graph_all(demo_file, demo_file_truth, gsp_results)
