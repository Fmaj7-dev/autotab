import librosa
import numpy as np
import os
import time
import random

from scipy.io import wavfile
from sklearn.utils import shuffle

# Represents a simple sample of music
#class Sample:
#    def __init__(self, note_index, spectrum_values):
#        self.note_index = note_index
#        self.spectrum_values = spectrum_values
#    
#    def __str__(self):
#        return "index: " + str(self.note_index) + " \nvalue: " + str(self.spectrum_values)
#
#    def getNoteIndex(self):
#        return self.note_index
#    
#    def getSpectrumValues(self):
#        return self.spectrum_values

# Dataset of wav files (we only store the CQT array that represents the sound)
# It can be processed from wav files, or read from a file if previously processed
class DataSet:
    def __init__(self):
        self.x_samples = []
        self.y_samples = []

        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []

    def __str__(self):
        ret = str(len(self.x_samples)) + " samples loaded\n" 
        if len(self.x_samples) > 0:
            #print (self.samples[0])
            ret =  ret + self.x_samples[0].__str__()

        return ret

    def getNumSamples(self):
        return len(self.x_samples)

    # each musical note has a name and a order, being C0 the first one.
    def getNoteOrder(self, file):
        note = file.split("_")[0]
        octave = int(note[-1])
        note_name = note[:-1]
        offset = 0

        if note_name == "c":
            offset = 0
        elif note_name == "cs":
            offset = 1
        elif note_name == "d":
            offset = 2
        elif note_name == "ds":
            offset = 3
        elif note_name == "e":
            offset = 4
        elif note_name == "f":
            offset = 5
        elif note_name == "fs":
            offset = 6
        elif note_name == "g":
            offset = 7
        elif note_name == "gs":
            offset = 8
        elif note_name == "a":
            offset = 9
        elif note_name == "as":
            offset = 10
        elif note_name == "b":
            offset = 11

        return octave*12 + offset

    # create a database of samples based on wav files
    def createFromAudioFiles(self, folder, verbose=False):
        start_time = time.time()

        for file in os.listdir(folder):
            if verbose:
                print("processing " + file)

            # iterate wav only
            if not file.endswith(".wav"):
                if verbose:
                    print("ignoring "+file)
                continue

            # get note order
            note_order = self.getNoteOrder(file)

            # get cqt from file            
            rate, data = wavfile.read( folder+"/"+file ) #pylint: disable=unused-variable
            C = np.abs(librosa.cqt(data[:,0] / float(65535), sr=44100, norm=0, filter_scale=3))

            # add all samples
            result = np.sum(C, axis=1)

            # normalize
            amax = np.amax(result)
            result = result/amax

            #s = Sample(note_order, result)
            self.x_samples.append(result)
            self.y_samples.append(note_order)

        total_time = time.time() - start_time
        if verbose:
            print("processing time: " + str(total_time))

    # save ascii array of samples
    def save( self, file_name ):
        File = open( file_name, "w" )
        
        # write number of samples
        File.write(str(len(self.x_samples)))
        File.write("\n")

        # for each sample write classification and array 
        for i in range(0, len(self.x_samples)):
            File.write( str(self.y_samples[i]) +"\n" )
            #sample.getSpectrumValues().tofile(File, " ")
            self.x_samples[i].tofile(File, " ")
            File.write( "\n" )
        File.close()
        pass

    # load ascii array of samples
    def load(self, file_name):
        start_time = time.time()
        File = open( file_name, "r" )
        num_samples = int(File.readline())

        # read all samples
        for i in range(0, num_samples): #pylint: disable=unused-variable
            index = int(File.readline())
            array = File.readline()
            spectrum = np.fromstring(array, sep=' ')
            #new_sample = Sample(index, spectrum)
            self.x_samples.append(spectrum)
            self.y_samples.append(index)

            # into the array of samples
            #self.samples.append(new_sample)

        File.close()
        total_time = time.time() - start_time #pylint: disable=unused-variable
        #print("loading time: " + str(total_time))

    def prepareForTraining(self):
        # randomize
        #random.shuffle(self.samples)
        (self.x_samples, self.y_samples) = shuffle(self.x_samples, self.y_samples)

        # move a percentage of original
        percentage = 20/100

        training_size = int(len(self.x_samples ) * percentage)

        self.x_test = self.x_samples[:training_size]
        self.x_train = self.x_samples[training_size:]

        self.y_test = self.y_samples[:training_size]
        self.y_train = self.y_samples[training_size:]

        # empty samples
        #self.samples = []
        