from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

import dataset
import librosa
import numpy as np
from scipy.io import wavfile

import noteutils

class Classifier:
    def __init__(self):
        self.valuesET = {}

    def trainNN(self, dataset):
        model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(1, 84)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
        ])
    def classifyNN(self, x_value):
        pass

    def trainET(self, dataset):

        for i in range(0, len(dataset.x_train)):
            note_name = dataset.y_train[i]
            spectrum = dataset.x_train[i]

            if note_name not in self.valuesET:
                self.valuesET[note_name] = spectrum
            else:
                self.valuesET[note_name] += spectrum

        for note_name, spectrum in self.valuesET.items():
            amax = np.amax(spectrum)
            self.valuesET[note_name] = spectrum/amax

    def save(self, filename):
        np.save(filename, self.valuesET) 

    def load(self, filename):
        self.valuesET = np.load(filename, allow_pickle='TRUE').item()

    def testET(self, dataset):
        num_guess = 0
        num_fails = 0

        for i in range(0, len(dataset.x_test)):
            # get known values
            guess_spectrum = dataset.x_test[i]
            guess_note_name = dataset.y_test[i]

            max_corr = -1
            max_corr_note = 0

            # find the maximum correlation
            for note_name, spectrum in self.valuesET.items():
                corr = np.corrcoef(guess_spectrum, spectrum)
                #print("correlation between"+str(guess_note_name) + " and " + str(note_name) + " = " + str(corr[0][1] ))
                if corr[0][1] > max_corr:
                    max_corr = corr[0][1]
                    max_corr_note = note_name

            print("guess note: "+str(guess_note_name))
            print("classified as: "+str(max_corr_note)+" "+str(max_corr*100)+"%")
            if guess_note_name == max_corr_note:
                num_guess += 1
            else:
                num_fails += 1

            max_corr = -1
            max_corr_note = 0
                

        success_rate = num_guess/(num_guess + num_fails)
        print("num tests: " + str(num_guess + num_fails))
        print("success rate: "+str(success_rate*100) + "%")

    #FIXME: move this to a common audio reader
    def classifyET(self, wavfilename):
        rate, data = wavfile.read( wavfilename ) #pylint: disable=unused-variable
        C = np.abs( librosa.cqt(data[:,0] / float(65535), sr=44100, norm=0, filter_scale=3) )

        # add all samples
        result = np.sum( C, axis=1 )

        # normalize
        amax = np.amax(result)
        result = result/amax

        max_corr = -1
        max_corr_note = 0

        # find the maximum correlation
        for note_name, spectrum in self.valuesET.items():
            corr = np.corrcoef(result, spectrum)
            #print("correlation between"+str(guess_note_name) + " and " + str(note_name) + " = " + str(corr[0][1] ))
            if corr[0][1] > max_corr:
                max_corr = corr[0][1]
                max_corr_note = note_name

        print(wavfilename+" classified as: "+noteutils.num2note(max_corr_note)+" "+str(max_corr*100)+"%")
