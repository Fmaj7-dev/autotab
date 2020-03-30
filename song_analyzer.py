import noteutils
from tablature import Tablature
from plot import plotSound

import matplotlib.pyplot as plt
from scipy.io import wavfile
import librosa
import numpy as np
import tensorflow as tf
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage import gaussian_filter1d

#from scipy.signal import argrelextrema
from scipy.signal import find_peaks

""" def analyze2(inputFile):
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
            if cur_time != previous_time:
                previous_time = cur_time//3
                tablature.addTime(str(cur_time))
            tablature.print() """


def analyze(file):
    # Feature extraction example
    import numpy as np
    import librosa

    # Load the example clip
    y, sr = librosa.load(file)

    # Set the hop length; at 22050 Hz, 512 samples ~= 23ms
    hop_length = 512

    # Separate harmonics and percussives into two waveforms
    y_harmonic, y_percussive = librosa.effects.hpss(y)

    y_harmonic = abs(y_harmonic)
    y_percussive = abs(y_percussive)

    # FIXME: this should be sampling rate dependant
    max_filter_win_size = 1000
    y_harmonic = maximum_filter(y_harmonic, max_filter_win_size)
    y_harmonic = gaussian_filter1d(y_harmonic, 1000)

    y_percussive = maximum_filter(y_percussive, max_filter_win_size)
    y_percussive = gaussian_filter1d(y_percussive, 1000)

    # normalize
    amax = np.amax(y_harmonic)
    y_harmonic = y_harmonic/amax

    amax = np.amax(y_percussive)
    y_percussive = y_percussive/amax

    y_total = y_percussive + y_harmonic
    

    #max_positions = argrelextrema(y_total, np.greater)[0]
    max_positions, _ = find_peaks(y_total, distance=150, prominence=0.1)


    # plot
    time = (1/sr) * len(y_total)
    xf = np.linspace( 0.0, time, len(y_total) )
    plt.plot(xf, y_total)
    plt.plot(max_positions/sr, y_total[max_positions], "x")
    plt.show()

    # open file with wavfile 
    # FIXME: check if we can reuse previous one
    rate, original_data = wavfile.read( file )
    data = original_data[:,0]

    previous_result = [0] * 84

    model = tf.keras.models.load_model("model")
    tablature = Tablature()

    for pulse in range(0, len(max_positions)-1):
        time_from = max_positions[pulse]
        time_to = max_positions[pulse+1]
        diff = time_to-time_from

        C = np.abs( librosa.cqt(data[time_from : time_from + int(diff*0.5)] / float(65535), sr=sr, norm=0, filter_scale=3) )

        # add all samples
        result = np.sum( C, axis=1 )
        
        new_result = result - previous_result
        previous_result = result

        # normalize
        amax = np.amax(new_result)
        
        # ignore silence pulses 
        if amax <0.01:
            continue

        new_result = new_result/amax

        # predict values
        prediction = model.predict(np.array([new_result]))

        new_result = np.where(prediction[0] == np.amax(prediction[0]))
        note_name = new_result[0]
  
        tablature.addNotes( note_name )
        """if cur_time != previous_time:
            previous_time = cur_time//3
            tablature.addTime(str(cur_time))"""
        tablature.print()

    # Beat track on the percussive signal
"""     tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,
                                                sr=sr)

    # Compute MFCC features from the raw signal
    mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)

    # And the first-order differences (delta features)
    mfcc_delta = librosa.feature.delta(mfcc)

    # Stack and synchronize between beat events
    # This time, we'll use the mean value (default) instead of median
    beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),
                                        beat_frames)

    # Compute chroma features from the harmonic signal
    chromagram = librosa.feature.chroma_cqt(y=y_harmonic,
                                            sr=sr)

    # Aggregate chroma features between beat events
    # We'll use the median value of each feature between beat frames
    beat_chroma = librosa.util.sync(chromagram,
                                    beat_frames,
                                    aggregate=np.median)

    # Finally, stack all beat-synchronous features together
    beat_features = np.vstack([beat_chroma, beat_mfcc_delta]) """
