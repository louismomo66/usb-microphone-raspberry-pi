import pyaudio
import struct
#import matplotlib.pyplot as plt
from time import sleep
import audioop

form_1 = pyaudio.paInt16
chans = 1
samp_rate = 44100
chunk = 44100
dev_index = 1
record_seconds = 1
threshold = 10
reading =0
previousreading = 0


p = pyaudio.PyAudio()

while True:
    stream = p.open(
        format=form_1,
        channels = chans,
        rate = samp_rate,
        input_device_index = dev_index,
        input = True,
        output=True,
        frames_per_buffer=chunk
    )
    frames = []
    for i in range(0, int(samp_rate/chunk*record_seconds)):
        data = stream.read(70)
        frames.append(data)
        sleep(0.001)

    reading = audioop.max(data,2)
    if reading - previousreading > threshold:
        print(reading)
    previousreading = reading

    stream.stop_stream()
    stream.close()
# clearing the resources
stream.stop_stream()
stream.close()
audio.terminate()

    
