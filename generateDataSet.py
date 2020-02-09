import numpy as np
from matplotlib import pyplot as plt
#from skimage import feature
from scipy.ndimage.filters import maximum_filter
from scipy.io import wavfile
from numpy import convolve

import os
import sys


def generateDataSet(inputFile, outputFolder):
    # get name & extension
    filename = os.path.basename(inputFile)
    filename, fileextension = os.path.splitext(filename)

    rate, original_data = wavfile.read( inputFile )

    data = original_data[:,0]

    max_filter_win_size = 2000

    # max filter
    max_data = maximum_filter(data, max_filter_win_size)

    # get zones with amplitude > min_amp
    min_amp = 1000
    peak_mask = np.logical_not(max_data < min_amp)

    # apply a derivate to detect borders of zones
    conv_mask = [-1, 2, -1]
    peak_mask = np.convolve(peak_mask, conv_mask)

    # pairs of [begin, end] that mark the zones
    max_places = np.where(peak_mask > 0)[0]

    # optionally plot it
    fig, ax = plt.subplots()
    r = range(data.shape[0])
    ax.plot(r, data, 'k')
    ax.plot(max_places, data[max_places], 'xr')
    ax.grid()
    plt.show()

    # export each zone as a file
    for i in range( 0, int(len(max_places)/2 ) ):
        start = max_places[2*i]
        end = max_places[2*i+1]
        wavfile.write(outputFolder + filename +"_"+ str(i) + fileextension, rate, original_data[start:end,:])


def showHelp():
    print("Usage:")
    print("")
    print("generateDataSet.py /home/alice/media/c1.wav /home/alice/dataset")


print (len(sys.argv))
if len(sys.argv) <3:
    showHelp()
else:
    generateDataSet(sys.argv[1], sys.argv[2])
