import csv
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_dataset_settings, DatasetSettings

if len(sys.argv) < 2:
    print('Usage: python create.py [house_num]')
    exit(1)

house_num = sys.argv[1]
settings = get_dataset_settings(house_num)
house = 'house_' + str(house_num)
house_dir = '../../dataset/low_freq/{}/'.format(house)

try:
    os.mkdir(house)
except OSError as error:
    pass

aggr_name = '{}/output_aggr.csv'.format(house)
disaggr_name = '{}/output_disaggr.csv'.format(house)
response_name = '{}/output_response.csv'.format(house)

#channel_mask = []

channels = []
channel_names = {}
print('Reading config')
print('\t{}'.format(settings.__dict__))
print('\t{}'.format(settings.channel_mask))
print('Reading labels')
with open(house_dir + 'labels.dat') as label_file:
    csv_reader = csv.reader(label_file, delimiter=' ')

    for row in csv_reader:
        num, name = row

        if len(settings.channel_mask) > 0 and not (name in settings.channel_mask):
            print('\t{} is not in channel_mask, skipping'.format(name))
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


channels.sort(key=lambda x:settings.sort_order.index(x[1]) if x[1] in settings.sort_order else 0)
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

print('Processing channels')
for c_path, c_name in channels:
    if settings.sort_order and not (c_name in settings.sort_order):
        continue
    print('\tProcessing channel {}'.format(c_name))
    channel_frame = pd.read_csv(c_path, index_col=0, delimiter=' ', names=['Time', c_name])
    channel_frame.index = pd.to_datetime(channel_frame.index, unit='s')
#    print(channel_frame)
    #Add to disaggregated as column
    disagg = disagg.add(channel_frame, fill_value=0)

#disagg = disagg.resample('1T').min().round()
disagg = disagg.resample('1T').max().round()

print('Writing CSVs')
if settings.sort_order:
    columns = settings.sort_order
else:
    columns = [c_name for c_path, c_name in channels]

print('\tWriting disaggr')
if settings.start_time:
    disagg[settings.start_time : settings.end_time].to_csv(disaggr_name, columns=columns)
else:
    disagg.to_csv(disaggr_name, columns=columns)


response = disagg.resample('1H').max().ge(settings.threshold)

print('\tWriting response')
if settings.start_time:
    response[settings.start_time : settings.end_time].to_csv(response_name, columns=columns)
else:
    response.to_csv(response_name, columns=columns)

main_agg = disagg.transpose()
main_agg = main_agg.sum()

print('\tWriting aggr')
if settings.start_time:
    main_agg[settings.start_time : settings.end_time].to_csv(aggr_name, index_label='Time', header=['aggregate'])
else:
    main_agg.to_csv(aggr_name, index_label='Time', header=['aggregate'])
