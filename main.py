
from scipy.io import wavfile
from plot import plotFourier, plotSound
import sys


def analysis(file):
    rate, data = wavfile.read( file )
    # res = A_weighting(data[1000][0])
    # print(res)

    plotFourier(data)
    plotSound(data)

def showHelp():
    print("Usage:")
    print("")
    print("generateDataSet.py /home/alice/media/c1.wav /home/alice/dataset")


print (len(sys.argv))
if len(sys.argv) <2:
    showHelp()
else:
    analysis(sys.argv[1])