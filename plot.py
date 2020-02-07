
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

def plotFourier(data):
    N = len(data)
    T = 1.0 / 44100

    yf = fft(data[:,0])
    xf = np.linspace(int(0.0), int(1.0/(2.0*T)), int(N/2))

    plt.plot(xf, 2.0/N * np.abs(yf[0:int(N/2)]))
    plt.grid()
    plt.show()
