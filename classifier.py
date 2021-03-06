from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf

import dataset
import librosa
import numpy as np
from scipy.io import wavfile

import noteutils

from matplotlib import pyplot as plt
import pandas as pd

class Classifier:
    def __init__(self):
        self.valuesET = {}
        # difference between the first note (C0) and the first classified note (E2)
        self.OFFSET = 28
        self.NUM_NOTES = 36

    def plot_the_loss_curve(self, epochs, rmse):
        """Plot the loss curve, which shows loss vs. epoch."""

        plt.figure()
        plt.xlabel("Epoch")
        plt.ylabel("Root Mean Squared Error")

        plt.plot(epochs, rmse, label="Loss")
        plt.legend()
        plt.ylim([rmse.min()*0.97, rmse.max()])
        plt.show()

    def trainNN(self, dataset):
        model = tf.keras.models.Sequential([
        #tf.keras.layers.Flatten(input_shape=(1, 84)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(self.NUM_NOTES)
        ])

        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        #loss_fn = tf.keras.losses.BinaryCrossentropy()

        model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

        history = model.fit(np.array(dataset.x_train), np.array(dataset.y_train), epochs=100)

        plot = True

        if plot:        
            epochs = history.epoch
            hist = pd.DataFrame( history.history )
            rmse = hist["loss"]
            self.plot_the_loss_curve(epochs, rmse)

        # evaluate loss
        model.evaluate( np.array(dataset.x_test),  np.array(dataset.y_test), verbose=2)

        tf.keras.models.save_model(model, "model")

    def testNN(self, dataset):
        num_guess = 0
        num_fails = 0

        model = tf.keras.models.load_model("model")

        for i in range(0, len(dataset.x_test)):
            # get known values
            guess_spectrum = dataset.x_test[i]
            guess_note_name = dataset.y_test[i]

            r = []
            r.append(guess_spectrum)

            prediction = model.predict(np.array(r))
            #note_name = prediction[0].index(max( prediction[0] ))
            result = np.where(prediction[0] == np.amax(prediction[0]))
            note_name = result[0]

            if guess_note_name == note_name:
                num_guess += 1
            else:
                num_fails += 1

                print("failed guess note: "+str(guess_note_name))
                print("classified as: "+str(note_name[0]))

        success_rate = num_guess/(num_guess + num_fails)
        print("num tests: " + str(num_guess + num_fails))
        print("success rate: "+str(success_rate*100) + "%")

    def classifyNN(self, wavfilename):
        #FIXME: move this to a common audio reader
        rate, data = wavfile.read( wavfilename ) #pylint: disable=unused-variable

        if len(data.shape) == 2:
            data=data[:,0]
        C = np.abs( librosa.cqt(data / float(65535), sr=44100, norm=0, filter_scale=3) )

        # add all samples
        result = np.sum( C, axis=1 )

        # normalize
        amax = np.amax(result)
        result = result/amax

        r = []
        r.append(result)

        model = tf.keras.models.load_model("model")

        prediction = model.predict(np.array(r))

        result = np.where(prediction[0] == np.amax(prediction[0]))
        note_name = result[0]

        print(prediction)
        print()

        print(wavfilename+" classified as: "+noteutils.num2note(note_name + self.OFFSET)+" "+str(prediction.max()))

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

            
            if guess_note_name == max_corr_note:
                num_guess += 1
            else:
                num_fails += 1
                print("failed guess note: "+str(guess_note_name))
                print("classified as: "+str(max_corr_note)+" "+str(max_corr*100)+"%")

            max_corr = -1
            max_corr_note = 0
                

        success_rate = num_guess/(num_guess + num_fails)
        print("num tests: " + str(num_guess + num_fails))
        print("success rate: "+str(success_rate*100) + "%")

    
    def classifyET(self, wavfilename):
        #FIXME: move this to a common audio reader
        rate, data = wavfile.read( wavfilename ) #pylint: disable=unused-variable
        
        if len(data.shape) == 2:
            data=data[:,0]

        C = np.abs( librosa.cqt(data / float(65535), sr=44100, norm=0, filter_scale=3) )

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
            print("correlation " + str(noteutils.num2note(note_name + self.OFFSET)) + " = " + str(corr[0][1] ))
            if corr[0][1] > max_corr:
                max_corr = corr[0][1]
                max_corr_note = note_name

        print(wavfilename+" classified as: "+noteutils.num2note(max_corr_note + self.OFFSET)+" "+str(max_corr*100)+"%")
