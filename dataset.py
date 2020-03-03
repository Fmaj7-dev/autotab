import librosa
import numpy as np
import os
import time

from scipy.io import wavfile

# Represents a simple sample of music
class Sample:
    def __init__(self, note_index, spectrum_values):
        self.note_index = note_index
        self.spectrum_values = spectrum_values
    
    def __str__(self):
        return "index: " + str(self.note_index) + " \nvalue: " + str(self.spectrum_values)

    def getNoteIndex(self):
        return self.note_index
    
    def getSpectrumValues(self):
        return self.spectrum_values

# Dataset of wav files (we only store the CQT array that represents the sound)
# It can be processed from wav files, or read from a file if previously processed
class DataSet:
    def __init__(self):
        self.samples = []

    def __str__(self):
        ret = str(len(self.samples)) + " samples loaded\n" 
        if len(self.samples) > 0:
            #print (self.samples[0])
            ret =  ret + self.samples[0].__str__()

        return ret

    def getNumSamples(self):
        return len(self.samples)

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

            s = Sample(note_order, result)
            self.samples.append(s)

        total_time = time.time() - start_time
        if verbose:
            print("processing time: " + str(total_time))

    # save ascii array of samples
    def save( self, file_name ):
        File = open( file_name, "w" )
        
        # write number of samples
        File.write(str(len(self.samples)))
        File.write("\n")

        # for each sample write classification and array 
        for sample in self.samples:
            File.write( str(sample.getNoteIndex()) +"\n" )
            sample.getSpectrumValues().tofile(File, " ")
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
            new_sample = Sample(index, spectrum)

            # into the array of samples
            self.samples.append(new_sample)

        File.close()
        total_time = time.time() - start_time #pylint: disable=unused-variable
        #print("loading time: " + str(total_time))
        