import librosa
import numpy as np
import os

from scipy.io import wavfile

class DataSet:
    def __init__(self):
        self.training_samples = []

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

    def createFromAudioFiles(self, folder):
        for file in os.listdir(folder):
            print("processing " + file)

            # iterate wav only
            if not file.endswith(".wav"):
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

    def save(self, path):
        pass

    def load(self, path):
        pass