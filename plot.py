
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import librosa.display
import librosa

from scipy.io import wavfile

def plotSound(data):
    time = (1/44100)*len(data)
    xf = np.linspace( 0.0, time, len(data) )
    plt.plot(xf, data)
    plt.grid()
    plt.show()
    

def plotFourier(name, *datas):

    data1 = datas[0]
    N = len(data1)
    T = 1.0 / 44100

    arrayOfYf=[]

    for data in datas:
        yf = fft(data[:,0])
        arrayOfYf.append(yf)
    
    xf = np.linspace(int(0.0), int(1.0/(2.0*T)), int(N/2))

    plt.figure(figsize=(16, 10))
    plt.ylim(0, 1800)
    plt.xlim(0,5000)
    for yf in arrayOfYf:
        plt.plot(xf, 2.0/N * np.abs(yf[0:int(N/2)]))

    
    plt.grid()
    #plt.savefig(name)
    plt.show()
    
def plotConstantQ(file):
    print ("constant Q")
    
    rate, data = wavfile.read( file ) #pylint: disable=unused-variable
    print( "samples: " + str(len(data[:,0]) ) )

    C = np.abs(librosa.cqt(data[:,0] / float(65535), sr=44100, norm=0, filter_scale=3))
    print("Shape: "+ str(C.shape ) )

    plt.title(file)

    # add all samples
    result = np.sum(C, axis=1)

    # normalize
    amax = np.amax(result)
    result = result/amax

    plt.plot(result)
    plt.show()

    #librosa.display.specshow( librosa.amplitude_to_db(C, ref=np.max), sr=44100, x_axis='time', y_axis='cqt_note' )
    #plt.colorbar(format='%+2.0f dB')
    #plt.title('Constant-Q power spectrum')
    #plt.tight_layout()
    #plt.show()
