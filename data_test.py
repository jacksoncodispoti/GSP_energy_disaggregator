import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft
import scipy.integrate
from config import get_disagg_settings

# https://stats.stackexchange.com/questions/18238/characterizing-periodicity-level-of-signal
def fft_periodicity(series):
    frequency_space = np.square(scipy.fft.fft(series))
    autocorrelation = np.abs(scipy.fft.ifft(frequency_space))
    period = np.argmax(autocorrelation)
    print('Period: {}, Frequency: {}'.format(period, 1 / period))
    fig, axs = plt.subplots(2, 1, sharex=True)
    axs[0].plot(series)
    axs[1].plot(autocorrelation)
    frequency_space = np.abs(frequency_space)
    #plt.scatter(np.real(frequency_space), np.imag(frequency_space))
    plt.show()
    power = np.power(frequency_space, 4)
    return scipy.integrate.simps(power)

def measure_periodicity(series):
    return fft_periodicity(series)

print("Loading settings")
house_num = 2
settings = get_disagg_settings(house_num)

print("1 of 6> reading data")
csvfileaggr = './dataset/house_{}/output_aggr.csv'.format(house_num)
csvfiledisaggr = "./dataset/house_{}/output_disaggr.csv".format(house_num)
df = pd.read_csv(csvfileaggr, index_col = "Time") # read demo file with aggregated active power
df.index = pd.to_datetime(df.index)
dfd = pd.read_csv(csvfiledisaggr, index_col = "Time") # read file with ground truth disaggregated appliances
dfd.index = pd.to_datetime(dfd.index)

mask = (df.index > settings.start_time) & (df.index < settings.end_time)
df = df.loc[mask]
mask = (dfd.index > settings.start_time) & (dfd.index < settings.end_time)
dfd = dfd.loc[mask]

start = 240
window_size = 180

df = df[start:start + window_size]
dfd = dfd[start:start + window_size]

labels = list(dfd.columns.values)
frequency_results = []
for (result,label) in zip(dfd.values.T, labels):
    print(label)
    series = np.zeros(360)
    series[0:180] = result
    periodicty = measure_periodicity(np.nan_to_num(series, 0))

    frequency_results.append(periodicty)

for (label, result) in sorted(zip(labels, frequency_results), key=lambda x: -x[1]):
    print('{}: {}'.format(label, result))


labels = [ '{} {}'.format(label, result) for (label, result) in zip(labels, frequency_results)]

fig, axs = plt.subplots(2, 1, sharex=True)
axs[0].plot(df)
axs[0].set_title("Aggregated power of house 2 from April 23th to 30th 2011, downsampled to 1 minute", size=8)
axs[1].stackplot(dfd.index, dfd.values.T, labels=labels)
axs[1].set_title("Disaggregated appliance power [Ground Truth]", size=8)
axs[1].legend(loc='upper left', fontsize=6)
plt.show()
