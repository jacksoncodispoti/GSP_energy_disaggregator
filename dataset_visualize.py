"""
This is for visualizing the datasets so we can ensure our's for house 2 is like theirs
"""
import pandas as pd
import matplotlib.pyplot as plt

csvfileaggr = "./output_aggr.csv"
csvfiledisaggr = "./output_disaggr.csv"
csvfileaggr_ours = "./house_2_output_aggr.csv"
csvfiledisaggr_ours = "./house_2_output_disaggr.csv"

df = pd.read_csv(csvfileaggr, index_col = "Time") # read demo file with aggregated active power
df.index = pd.to_datetime(df.index)
dfd = pd.read_csv(csvfiledisaggr, index_col = "Time") # read file with ground truth disaggregated appliances
dfd.index = pd.to_datetime(dfd.index)

df_ours = pd.read_csv(csvfileaggr_ours, index_col = "Time") # read demo file with aggregated active power
df_ours.index = pd.to_datetime(df_ours.index)
dfd_ours = pd.read_csv(csvfiledisaggr_ours, index_col = "Time") # read file with ground truth disaggregated appliances
dfd_ours.index = pd.to_datetime(dfd_ours.index)

fig, axs = plt.subplots(3, 1, sharex=True)
axs[0].plot(df, label='theirs')
axs[0].plot(df_ours, label='ours')
axs[0].set_title("Aggregated power of house 2 from April 23th to 30th 2011, downsampled to 1 minute", size=8)
axs[0].legend(loc='upper left', fontsize=6)

axs[1].stackplot(dfd.index, dfd.values.T, labels=list(dfd.columns.values))
axs[1].set_title("Disaggregated appliance power [Theirs]", size=8)
axs[1].legend(loc='upper left', fontsize=6)

axs[2].stackplot(dfd_ours.index, dfd_ours.values.T, labels=list(dfd_ours.columns.values))
axs[2].set_title("Disaggregated appliance power [Ours]", size=8)
axs[2].legend(loc='upper left', fontsize=6)

plt.show()
