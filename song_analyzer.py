import noteutils
from tablature import Tablature

from scipy.io import wavfile
import librosa
import numpy as np
import tensorflow as tf

def analyze(inputFile):
    rate, original_data = wavfile.read( inputFile )
    data = original_data[:,0]

    WINDOW_SIZE = rate//10
    print("window: "+ str(WINDOW_SIZE))

    times = len(data)//WINDOW_SIZE
    print("times: "+ str(times))

    model = tf.keras.models.load_model("model")

    previous_note = 0
    previous_time = 0

    tablature = Tablature()

    for i in range(0, times-1):
        C = np.abs( librosa.cqt(data[i*WINDOW_SIZE : (i+1)*WINDOW_SIZE] / float(65535), sr=44100, norm=0, filter_scale=3) )

        # add all samples
        result = np.sum( C, axis=1 )

        # normalize
        amax = np.amax(result)
        
        if amax <0.01:
            continue

        result = result/amax

        

        r = []
        r.append(result)

        prediction = model.predict(np.array(r))

        result = np.where(prediction[0] == np.amax(prediction[0]))
        note_name = result[0]

        cur_time = i*WINDOW_SIZE/rate

        if note_name != previous_note:
            previous_note = note_name
            
            #print( noteutils.num2note(note_name + 28) )
            #print( i*WINDOW_SIZE/rate )
            
            tablature.addNotes( note_name )
            if cur_time//3 != previous_time:
                previous_time = cur_time//3
                tablature.addTime(str(cur_time))
            tablature.print()

    