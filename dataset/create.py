import csv
import pandas as pd
import sys
import os

if len(sys.argv) < 2:
    print('Usage: python create.py [house_num]')
    exit(1)

start_time = '2011-04-23'
end_time = '2011-04-30'
channel_mask = ['refrigerator', 'kitchen_outlets', 'microwave', 'lighting']
sort_order = ['refrigerator',  'kitchen_outlets', 'kitchen_outlets2', 'microwave', 'lighting']

house = 'house_' + str(sys.argv[1])
house_dir = '../../dataset/low_freq/{}/'.format(house)

try:
    os.mkdir(house)
except OSError as error:
    pass

aggr_name = '{}/output_aggr.csv' .format(house)
disaggr_name = '{}/output_disaggr.csv' .format(house)

#channel_mask = []

channels = []
channel_names = {}
with open(house_dir + 'labels.dat') as label_file:
    csv_reader = csv.reader(label_file, delimiter=' ')

    for row in csv_reader:
        num, name = row

        if len(channel_mask) > 0 and not (name in channel_mask):
            print('{} is not in channel_mask'.format(name))
            continue

        #Auto-increment names
        if name in channel_names:
            channel_names[name] += 1
        else:
            channel_names[name] = 1

        if name == 'mains':
            pass
        else:
            canonical_name = name + ('' if channel_names[name] == 1 else str(channel_names[name]))
            channels.append([house_dir + 'channel_' + num + '.dat', canonical_name])


channels.sort(key=lambda x:sort_order.index(x[1]) if x[1] in sort_order else 0)
main1_path = house_dir + 'channel_1.dat'
main2_path = house_dir + 'channel_2.dat'

#Use main channel to get the timestamp indicies
#Don't sample from main channel because we're only selecting from the mask
main1 = pd.read_csv(main1_path, index_col=0, delimiter=' ', names=['Time', 'aggregate'])
main1.index = pd.to_datetime(main1.index, unit='s')

disagg = pd.DataFrame(None, main1.index)

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#pd.set_option('display.width', None)
#pd.set_option('display.max_colwidth', -1)

for c_path, c_name in channels:
    if not (c_name in sort_order):
        continue
    print('Processing channel {}'.format(c_name))
    channel_frame = pd.read_csv(c_path, index_col=0, delimiter=' ', names=['Time', c_name])
    channel_frame.index = pd.to_datetime(channel_frame.index, unit='s')
#    print(channel_frame)
    #Add to disaggregated as column
    disagg = disagg.add(channel_frame, fill_value=0)

#disagg = disagg.resample('1T').min().round()
disagg = disagg.resample('1T').max().round()
disagg[start_time : end_time].to_csv(disaggr_name, columns=sort_order)
main_agg = disagg.transpose()
main_agg = main_agg.sum()
main_agg[start_time : end_time].to_csv(aggr_name, index_label='Time', header=['aggregate'])
