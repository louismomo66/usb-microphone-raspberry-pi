import pyaudio
import schedule
import time
import audioop
import math
import wave
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publishi
from datetime import datetime
wave_output_filename = 'wave1.wav'

Broker = "192.168.43.141"
sub_topic = "mic/spldb"

class Noisemonitor():
    def __init__(self,channels=1,rate=44100,chunk = 1024*2,clip_duration=4):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.clip_duration=clip_duration
        self._pa = pyaudio.PyAudio()
        self.stream = None
        self.frame = []

    def start(self):
        fps = int(self.rate/self.chunk)
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.chunk,
                                     )
        #for i in range(0,):
        while True:
            data = self._stream.read(self.chunk,exception_on_overflow=False)
            rms = audioop.rms(data,2)
            db = 20*math.log10(rms/20)
            db = round(db,2)
            #print(db)
            #schedule.run_pending()
            mqttc=mqtt.Client("node-red")
            mqttc.connect(Broker,1883,60)
            mqttc.publish(sub_topic,db)

    def record(self):
        fps = int(self.rate/self.chunk*self.clip_duration)
        self._stream.start_stream()
        clip =[]
        for i in range(0,fps):
            data=self._stream.read(self.chunk,exception_on_overflow=False)
            clip.append(data)
        print('recorded')
        self._stream.stop_stream()
        self._stream.close()
        slelf._pa.terminate()

        wavefile=wave.open(wave_output_filename,'wb')
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        wavefilr.writeframes(b''.join(clip))
        wavefile.close()

    schedule.every(0.1).minutes.do(record)




bst = Noisemonitor()
bst.start()
