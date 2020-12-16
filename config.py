import ConfigParser
from collections import namedtuple

conf_path = 'config.config'

conf_disagg = 'disaggregator'
conf_dataset = 'dataset'

def get_disagg_settings(house_num):
    master_parser = ConfigParser.RawConfigParser()
    master_parser.read(conf_path)

    indiv_parser = ConfigParser.RawConfigParser()
    indiv_parser.read('dataset/house_{}/{}'.format(house_num, conf_path))

    master_settings = { key : master_parser.get(conf_disagg, key) for key in master_parser.options(conf_disagg) }

    if conf_disagg in indiv_parser.sections():
        indiv_settings = { key : indiv_parser.get(conf_disagg, key) for key in indiv_parser.options(conf_disagg) }
    else:
        indiv_settings = {}

    #Overwrite master dict with indiv settings
    master_settings.update(indiv_settings)

    return DisaggSettings(**master_settings)

def get_dataset_settings(house_num):
    master_parser = ConfigParser.RawConfigParser()
    master_parser.read(conf_path)

    indiv_parser = ConfigParser.RawConfigParser()
    indiv_parser.read('house_{}/{}'.format(house_num, conf_path))

    master_settings = { key : master_parser.get(conf_dataset, key) for key in master_parser.options(conf_dataset) }

    if conf_dataset in indiv_parser.sections():
        indiv_settings = { key : indiv_parser.get(conf_dataset, key) for key in indiv_parser.options(conf_dataset) }
    else:
        indiv_settings = {}

    #Overwrite master dict with indiv settings
    master_settings.update(indiv_settings)

    return DatasetSettings(**master_settings)

class DisaggSettings:
    def __init__(self, start_time, end_time, sigma, ri, t_positive, t_negative, alpha, beta, instancelimit, init_size, frame_size):
        self.start_time = start_time
        self.end_time = end_time
        self.sigma = float(sigma)
        self.ri = float(ri)
        self.T_Positive = float(t_positive)
        self.T_Negative = float(t_negative)
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.instancelimit = int(instancelimit)
        self.init_size = int(init_size)
        self.frame_size = int(frame_size)

class DatasetSettings:
    def __init__(self, start_time, end_time, threshold, channel_mask, sort_order):
        self.start_time = start_time
        self.end_time = end_time

        self.threshold = int(threshold)

        if isinstance(channel_mask, list):
            self.channel_mask = channel_mask
        else:
            if not channel_mask:
                self.channel_mask = []
            else:
                self.channel_mask = [s.strip() for s in channel_mask.split(',')]

        if isinstance(sort_order, list):
            self.sort_order = sort_order
        else:
            if not sort_order:
                self.sort_order = []
            else:
                self.sort_order = [s.strip() for s in sort_order.split(',')]

