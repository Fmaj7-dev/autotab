import librosa
import numpy as np
import os
import time
import random

from scipy.io import wavfile
from sklearn.utils import shuffle

import noteutils

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
            ret =  ret + self.x_samples[0].__str__()

        return ret

    def getNumSamples(self):
        return len(self.x_samples)

    # each musical note has a name and a order, being C0 the first one.
    def getNoteOrder(self, file):
        note = file.split("_")[1]
        octave = file.split("_")[2]

        return noteutils.note2num(note, octave)

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
            self.y_samples.append(note_order -28)

        total_time = time.time() - start_time
        if verbose:
            print("processing time: " + str(total_time))

    # save ascii array of samples
    def save( self, file_name ):
        #np.savez("x_samples.npz", x=self.x_samples)
        #np.savez("y_samples.npz", y=self.y_samples)
        #return

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

    # load ascii array of samples
    def load(self, file_name):
        #x = np.load("x_samples.npz")
        #y = np.load("y_samples.npz")

        #self.x_data = x['x']
        #self.y_data = y['y']
        #print(self.x_samples)
        #return 

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

        File.close()
        total_time = time.time() - start_time #pylint: disable=unused-variable
        #print("loading time: " + str(total_time))

    def prepareForTraining(self):
        # randomize
        (self.x_samples, self.y_samples) = shuffle(self.x_samples, self.y_samples)

        # move a percentage of original to test
        percentage = 20/100

        training_size = int(len(self.x_samples ) * percentage)

        self.x_test = self.x_samples[:training_size]
        self.x_train = self.x_samples[training_size:]

        self.y_test = self.y_samples[:training_size]
        self.y_train = self.y_samples[training_size:]

        # samples still have the data
        
        