
from scipy.io import wavfile
from plot import plotFourier, plotSound, plotConstantQ
import sys
import os


def analysis(file):
    rate, data = wavfile.read( file )
    filename = os.path.splitext(file)[0] + ".png"
    #plotFourier(filename, data )
    #plotSound(data)
    plotConstantQ(file)

def showHelp():
    print("Usage:")
    print("")
    print("generateDataSet.py /home/alice/media/c1.wav /home/alice/dataset")


print (len(sys.argv))
if len(sys.argv) <2:
    showHelp()
else:
    analysis(sys.argv[1])