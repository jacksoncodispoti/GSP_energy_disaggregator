import sys
import pandas as pd
from identifier import Identifier
import gsp_visualize as gsp_v

if len(sys.argv) < 2:
    print('Usage: python visualizer.py [house_num]')
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

gsp_v.graph(demo_file, demo_file_truth)
