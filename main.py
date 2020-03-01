
from scipy.io import wavfile
from plot import plotFourier, plotSound, plotConstantQ
import sys
import os
import dataset


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


if len(sys.argv) <3:
    showHelp()
else:
    if sys.argv[1] == "analysis":
        analysis(sys.argv[2])
    elif sys.argv[1] == "generate_dataset":
        pass
    elif sys.argv[1] == "process_dataset":
        d = dataset.DataSet()
        d.createFromAudioFiles( sys.argv[2] )