import pandas as pd

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

        #print(gsp_appliances)
        #print(usr_appliances)

        #This is a partial implementation, we still gotta think of the weirder cases like
        #If there are more appliance_X than actual labels
        print('\tIdentifying appliances')
        for i in range(min(len(gsp_appliances), len(usr_appliances))):
            print('\t\t{} is {}'.format(usr_appliances[i][0], gsp_appliances[i][0]))
