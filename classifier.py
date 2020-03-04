from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

import dataset

import numpy as np

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

    def classifyET(self, dataset):

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

            #print("guess note: "+str(guess_note_name))
            #print("classified as: "+str(max_corr_note))
            if guess_note_name == max_corr_note:
                num_guess += 1
            else:
                num_fails += 1

            max_corr = -1
            max_corr_note = 0
                

        success_rate = num_guess/(num_guess + num_fails)
        print("num tests: " + str(num_guess + num_fails))
        print("success rate: "+str(success_rate*100) + "%")

        
