import numpy as np
from matplotlib import pyplot as plt
from skimage import feature
from scipy.ndimage.filters import maximum_filter
from scipy.io import wavfile
from numpy import convolve

"""
# put your data here
#data = np.array([0, 79, 75, 69, 69, 7, ...])
rate, data = wavfile.read("/Users/enrique/projects/guitar_dataset/c16.wav")

data = data[:,0]

filter_win_size = 20000
peak_intensity_threshold = 100

max_data = maximum_filter(data, filter_win_size)
min_data = -maximum_filter(-data, filter_win_size)

# select places where we detect maximum but not minimum -> we dont want long plateaus
peak_mask = np.logical_and(max_data == data, min_data != data)
peak_mask = np.logical_and(peak_mask, data > 1000)
# select peaks where we have enough elevation
peak_mask = np.logical_and(peak_mask, max_data - min_data > peak_intensity_threshold)
# a trick to convert True to 1, False to -1
peak_mask = peak_mask * 2 - 1
# select only the up edges to eliminate multiple maximas in a single peak
peak_mask = np.correlate(peak_mask, [-1, 1], mode='same') == 2

max_places = np.where(peak_mask)[0]

fig, ax = plt.subplots()
r = range(data.shape[0])
ax.plot(r, data, 'k')
ax.plot(max_places, data[max_places], 'xr')
ax.grid()
#ax.axis((0, 4000, 0, 130))
plt.show()
"""
