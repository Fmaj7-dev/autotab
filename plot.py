
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

def plotSound(data):
    time = (1/44100)*len(data)
    xf = np.linspace( 0.0, time, len(data) )
    plt.plot(xf, data)
    plt.grid()
    plt.show()
    

def plotFourier(*datas):

    data1 = datas[0]
    N = len(data1)
    T = 1.0 / 44100

    arrayOfYf=[]

    for data in datas:
        yf = fft(data[:,0])
        arrayOfYf.append(yf)
    
    xf = np.linspace(int(0.0), int(1.0/(2.0*T)), int(N/2))

    for yf in arrayOfYf:
        plt.plot(xf, 2.0/N * np.abs(yf[0:int(N/2)]))

    plt.grid()
    plt.show()
