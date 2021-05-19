import sys
import pandas as pd
from identifier import Identifier
from config import get_disagg_settings, DisaggSettings
import gsp_visualize as gsp_v

if len(sys.argv) < 2:
    print('Usage: python visualizer.py [house_num]')
    print('This program is for visualizing full datasets to create refined ones')
    sys.exit()

house_num = int(sys.argv[1])

csvfileaggr = 'dataset/house_{}/output_aggr.csv'.format(house_num)
csvfiledisaggr = 'dataset/house_{}/output_disaggr.csv'.format(house_num)
csvfileresponse = 'dataset/house_{}/output_response.csv'.format(house_num)

identifier = Identifier(20, csvfileresponse)

demo_file = pd.read_csv(csvfileaggr, index_col="Time")
demo_file.index = pd.to_datetime(demo_file.index)
demo_file_truth = pd.read_csv(csvfiledisaggr, index_col="Time")
demo_file_truth.index = pd.to_datetime(demo_file_truth.index)

settings = get_disagg_settings(house_num)

mask = (demo_file.index > settings.start_time) & (demo_file.index < settings.end_time)
masked_demo_file = demo_file.loc[mask]

mask = (demo_file_truth.index > settings.start_time) & (demo_file_truth.index < settings.end_time)
masked_demo_file_truth = demo_file_truth.loc[mask]

gsp_v.graph_ranged(demo_file, demo_file_truth, masked_demo_file, masked_demo_file_truth, house_num)
