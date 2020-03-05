
from scipy.io import wavfile
from plot import plotFourier, plotSound, plotConstantQ
import sys
import os
import dataset
import classifier

def analysis(file):
    rate, data = wavfile.read( file ) #pylint: disable=unused-variable
    filename = os.path.splitext(file)[0] + ".png" #pylint: disable=unused-variable
    #plotFourier(filename, data )
    #plotSound(data)
    plotConstantQ(file)

def showHelp():
    print("Usage:")
    print("")
    print("python main.py analysis <wav file>")
    print("python main.py generate_dataset")
    print("python main.py process_dataset <path to directory with wav files>")
    print("python main.py train")


# option parameter not given
if len(sys.argv) <2:
    showHelp() 
    exit

if sys.argv[1] == "analysis":
    if len(sys.argv) <3:
        showHelp()
        exit
    analysis(sys.argv[2])
elif sys.argv[1] == "generate_dataset":
    pass
elif sys.argv[1] == "process_dataset":
    if len(sys.argv) <3:
        showHelp()
        exit

    d = dataset.DataSet()
    d.createFromAudioFiles( sys.argv[2], verbose = True )
    #print(d)
    d.save("database.db")
elif sys.argv[1] == "train":
    d = dataset.DataSet()
    d.load("database.db")
    d.prepareForTraining()

    c = classifier.Classifier()
    c.trainET(d)
    c.testET(d)
    c.save("classif.db")
elif sys.argv[1] == "classify":
    c = classifier.Classifier()
    c.load("classif.db.npy")
    c.classifyET(sys.argv[2])

