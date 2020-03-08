
from scipy.io import wavfile
from plot import plotFourier, plotSound, plotConstantQ
import sys
import os
import dataset
import classifier
import noteutils
import generateDataSet

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
    print("")
    print("python main.py generate_dataset <input folder> <output folder>")
    print("")
    print("python main.py process_dataset <path to directory with wav files>")
    print("    Creates a database with all the parameters from the audio files")
    print("")
    print("python main.py train")
    print("    Creates a database of the weights of the classificator")
    print("")
    print("python main.py classify <wav file>")
    print("    Returns the class where the wav belongs")


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
    if len(sys.argv) < 4:
        showHelp()
        exit
    generateDataSet.generateDataSet(sys.argv[2], sys.argv[3])

elif sys.argv[1] == "process_dataset":
    if len(sys.argv) <3:
        showHelp()
        exit

    d = dataset.DataSet()
    d.createFromAudioFiles( sys.argv[2], verbose = True )
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

elif sys.argv[1] == "trainNN":
    d = dataset.DataSet()
    d.load("database.db")
    d.prepareForTraining()

    c = classifier.Classifier()
    c.trainNN(d)

elif sys.argv[1] == "classifyNN":
    c = classifier.Classifier()
    c.classifyNN(sys.argv[2])    

elif sys.argv[1] == "notes":
    noteutils.printNotes()
else:
    showHelp()

