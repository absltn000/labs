import struct
import wave

import matplotlib.pyplot as plt
import time

timer = time.time() #Получение текущего времени

wavefile = wave.open("signal_25.wav", "r") #Открытие файла

length = wavefile.getnframes() #Количество фремов
wave = list()

#Создание списка фреймов с их преобразованием в десятичный вид
for i in range(0, length//4):
    wavedata = wavefile.readframes(1)
    data = struct.unpack("<h", wavedata)
    wave.append(data[0])
#График с заданными параметрами
plt.plot(wave, color='black', marker='*', linestyle='--', linewidth=0.5, markersize=3)
plt.title('График звуковых сигналов')
plt.xlabel('Фрейм')
plt.ylabel('Частота')


print(time.time() - timer,"seconds") #Вывод времени работы программы
plt.show()
