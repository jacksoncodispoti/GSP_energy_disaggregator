import pandas as pd
import numpy.ma as ma
import numpy as np

class Identifier:
    def __init__(self, threshold, response_file):
        self.threshold = threshold
        self.responses = pd.read_csv(response_file, index_col="Time") * 1.0
        self.responses.index = pd.to_datetime(self.responses.index)

    def process_frame(self, frame_num, frame_size, gsp_result):
        gsp_response = gsp_result.resample('60T').max().ge(self.threshold)
        gsp_response = (gsp_response.resample('{}T'.format(frame_size)).sum() / 4)

        usr_response = self.responses.iloc[0 : len(gsp_response)]
        #print(gsp_response)
        #print(usr_response)
        #print('==========')
        #print(gsp_response.sum())
        #print(usr_response.sum())

        gsp_appliances = gsp_response.sum()
        usr_appliances = usr_response.sum()
        gsp_appliances = list(zip(gsp_appliances.keys(), gsp_appliances.values))
        usr_appliances = list(zip(usr_appliances.keys(), usr_appliances.values))

        gsp_appliances.sort(key=lambda x:-x[1])
        usr_appliances.sort(key=lambda x:-x[1])

        diff_matrix = ma.zeros((len(usr_appliances), len(gsp_appliances)))
        diff_matrix.mask = np.zeros(diff_matrix.shape)

        for i, (usr_key, usr_val) in enumerate(usr_appliances):
            for j, (gsp_key, gsp_val) in enumerate(gsp_appliances):
                diff_matrix[i][j] = abs((gsp_val - usr_val) / gsp_val)

        print(gsp_appliances)
        print(usr_appliances)
#        print(diff_matrix)
        pairs = []
        for i, (usr_key, usr_val) in enumerate(usr_appliances):
            match = diff_matrix[i].argmin()
            print('Looking to match {}[{}]'.format(usr_key, usr_val))
            print([l[0] for l in gsp_appliances])
            print(diff_matrix[i])
            print('got match {} with {}'.format(match, i))
            pairs.append([match, i])
            new_mask = diff_matrix.mask.transpose()
            new_mask[match] = np.ones(len(usr_appliances))
            diff_matrix.mask = new_mask.transpose()

        #This is a partial implementation, we still gotta think of the weirder cases like
        #If there are more appliance_X than actual labels
        labels = []
        print('\tIdentifying appliances')
        print(len(usr_appliances))
        print(len(gsp_appliances))
        for i, j in pairs:
            print('({} {}'.format(i, j))
            labels.append((usr_appliances[j][0], gsp_appliances[i][0]))
            print('\t\t[{} ~ {}]{} is {}'.format(usr_appliances[j][1], gsp_appliances[i][1], usr_appliances[j][0], gsp_appliances[i][0]))

        labels.sort(key=lambda x:x[1])
        labels = [label[0] for label in labels][:len(gsp_result.columns)]
        for i in range(len(labels), len(gsp_result.columns)):
            labels.append(None)
        gsp_result.columns = labels
