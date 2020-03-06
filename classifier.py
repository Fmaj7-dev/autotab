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
        #tf.keras.layers.Flatten(input_shape=(1, 84)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10)
        ])

        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

        model.compile(optimizer='adam',
              loss=loss_fn,
              metrics=['accuracy'])

        # minimize loss
        #print(dataset.x_train)
        #print(dataset.y_train)
        y_train = []
        for y in dataset.y_train:
            if y == 28:
                y_train.append(0)
            elif y == 31:
                y_train.append(1)
            elif y == 36:
                y_train.append(2)
            elif y == 41:
                y_train.append(3)
            elif y == 64:
                y_train.append(4)


        model.fit(np.array(dataset.x_train), np.array(y_train), epochs=10)

        # evaluate loss
        y_test = []
        for y in dataset.y_test:
            if y == 28:
                y_test.append(0)
            elif y == 31:
                y_test.append(1)
            elif y == 36:
                y_test.append(2)
            elif y == 41:
                y_test.append(3)
            elif y == 64:
                y_test.append(4)

        model.evaluate( np.array(dataset.x_test),  np.array(y_test), verbose=2)

        tf.keras.models.save_model(model, "model")

    def classifyNN(self, wavfilename):
        #FIXME: move this to a common audio reader
        rate, data = wavfile.read( wavfilename ) #pylint: disable=unused-variable
        C = np.abs( librosa.cqt(data[:,0] / float(65535), sr=44100, norm=0, filter_scale=3) )

        # add all samples
        result = np.sum( C, axis=1 )

        # normalize
        amax = np.amax(result)
        result = result/amax

        r = []
        r.append(result)
        r.append(result)

        model = tf.keras.models.load_model("model")

        prediction = model.predict(np.array(r))
        print(prediction)



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

    
    def classifyET(self, wavfilename):
        #FIXME: move this to a common audio reader
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
            print("correlation " + str(noteutils.num2note(note_name)) + " = " + str(corr[0][1] ))
            if corr[0][1] > max_corr:
                max_corr = corr[0][1]
                max_corr_note = note_name

        print(wavfilename+" classified as: "+noteutils.num2note(max_corr_note)+" "+str(max_corr*100)+"%")
