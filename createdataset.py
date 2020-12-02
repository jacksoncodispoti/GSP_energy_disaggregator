import csv
import pandas as pd

house = 'house_2'
house_dir = '../dataset/low_freq/{}/'.format(house)
aggr_name = '{}_output_aggr.csv' .format(house)
disaggr_name = '{}_output_disaggr.csv' .format(house)

channel_mask = ['refrigerator1', 'kitchen_outlets1', 'kitchen_outlets2', 'microwave1', 'lighting1']

channels = []
channel_names = {}
with open(house_dir + 'labels.dat') as label_file:
    csv_reader = csv.reader(label_file, delimiter=' ')

    for row in csv_reader:
        num, name = row

        #Auto-increment names
        if name in channel_names:
            channel_names[name] += 1
        else:
            channel_names[name] = 1

        if name == 'mains':
            pass
        else:
            canonical_name = name + str(channel_names[name])
            channels.append([house_dir + 'channel_' + num + '.dat', canonical_name])

main1_path = house_dir + 'channel_1.dat'
main2_path = house_dir + 'channel_2.dat'

main1 = pd.read_csv(main1_path, index_col=0, delimiter=' ', names=['Time', 'aggregate'])
main1.index = pd.to_datetime(main1.index, unit='s')

main2 = pd.read_csv(main2_path, index_col=0, delimiter=' ', names=['Time', 'aggregate'])
main2.index = pd.to_datetime(main2.index, unit='s')

main_agg = main1 + main2
main_agg = main_agg.resample('1T').mean().round()
main_agg.to_csv(aggr_name)

disagg = pd.DataFrame(None, main1.index)

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#pd.set_option('display.width', None)
#pd.set_option('display.max_colwidth', -1)

for c_path, c_name in channels:
    if len(channel_mask) > 0 and not(c_name in channel_mask):
        print('Skipping channel {} (not in mask)'.format(c_name))
        continue

    print('Processing channel {}'.format(c_name))
    channel_frame = pd.read_csv(c_path, index_col=0, delimiter=' ', names=['Time', c_name])
    channel_frame.index = pd.to_datetime(channel_frame.index, unit='s')
#    print(channel_frame)
    disagg = disagg.add(channel_frame, fill_value=0)

disagg = disagg.resample('1T').mean().round()
disagg.to_csv(disaggr_name)
