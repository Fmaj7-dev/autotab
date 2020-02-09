
from scipy.io import wavfile
from plot import *
#from db split *

rate, data = wavfile.read("/Users/enrique/projects/guitar_dataset/shortc.wav")
# res = A_weighting(data[1000][0])
# print(res)

plotFourier(data)
plotSound(data)
