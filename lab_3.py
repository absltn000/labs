import struct
import wave

import time
from scipy.fft import *
import numpy as np
import matplotlib.pyplot as plt


timer = time.time()

with wave.open("signal_25.wav", "r") as file:
    wavefile = file

length = wavefile.getnframes()
wave = list()

for i in range(0, length//4):
    wavedata = wavefile.readframes(1)
    data = struct.unpack("<h", wavedata)
    wave.append(data[0])


N = length
T = 1/wavefile.getframerate()
x = np.linspace(0, N*T, N, endpoint=False)
xf = fftfreq(N, T)
y = dct(wave)
plt.plot(xf[:(length)//4],y)
plt.show()
