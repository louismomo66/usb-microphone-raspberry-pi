import pyaudio
import schedule
import time
import audioop
import math
import wave
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publishi
from datetime import datetime
fname = 'wave1.wav'

Broker = "192.168.43.141"
sub_topic = "mic/spldb"
class MicRecorder():

    def __init__(self,channels=1, rate=44100, frames_per_buffer=1024*2, clip_duration=4, overlap=0):
        #self.output_path = output_path
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self.clip_duration = clip_duration
        self.overlap = overlap
        self._pa = pyaudio.PyAudio()
        self._stream = None
        self.frames = []

    def start_recording(self):
        fps = int(self.rate / self.frames_per_buffer * self.clip_duration)
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                     channels=self.channels,
                                     rate=self.rate,
                                     input=True,
                                     frames_per_buffer=self.frames_per_buffer)
                                     #stream_callback=self.get_callback())
        print('Begin recording...')
        self._stream.start_stream()
        try:
            while True:
                if len(self.frames) > fps:
                    clip = []
                    for i in range(0, fps):
                        clip.append(self.frames[i])
                    #fname = ''.join([self.output_path, '/clip-', datetime.utcnow().strftime('%Y%m%d%H%M%S'), '.wav'])
                    wavefile = self._prepare_file(fname)
                    wavefile.writeframes(b''.join(clip))
                    wavefile.close()
                    self.frames = self.frames[(self.clip_duration - self.overlap - 1):]
        except KeyboardInterrupt as e:
            print('Terminating recording...', end='')
            self.stop_recording()
            print('OK')

    def stop_recording(self):
        self._stream.stop_stream()

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.frames.append(in_data)
            return in_data, pyaudio.paContinue
        return callback

    def _prepare_file(self, filename, mode='wb'):
        wavefile = wave.open(filename, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile


MicRecorder()
