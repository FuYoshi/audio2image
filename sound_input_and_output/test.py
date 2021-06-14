
# Can record, play and display sounds from .wav files and user input.

import os
from random import sample
import pyaudio as pa
import wave
#import sys
#import struct
import numpy as np
#import librosa
from scipy import signal
#import scipy
import scipy.io
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy.signal.spectral import spectrogram
import IPython.display as ipd

# This function lets the user record a sound using their microphone. This
# recording is converted to a .wav file.
def record(outputFile):
    CHUNK = 1024
    FORMAT = pa.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 3

    # Makes a PyAudio object.
    p = pa.PyAudio()

    # Open stream based on the defined values.
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Recording")

    frames = []

    # Input from stream is read and stored in the frames list.
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # .wav file is made based on the information that hase been collected.
    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function playes a .wav file.
def play_audio(audio_file):
    chunk = 1024

    # Reads .wav file.
    wf = wave.open(audio_file, 'rb')

    # Makes a PyAudio object.
    p = pa.PyAudio()

    # Strem is opened based on the information of the .wav file.
    stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)
    data = wf.readframes(chunk)

    # .wav file is outputed to the stream based on the collected data.w
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate()

def create_spectorgram(audio_file):
    sample_rate, samples = wavfile.read('output1.wav')
    freq, times, spectrogram = signal.spectrogram(samples, sample_rate)

    plt.pcolormesh(np.log(spectrogram))
    plt.xlabel('Frequency (HZ)')
    plt.ylabel('Time (SEC)')
    plt.show()

record('output1.wav')
play_audio('output1.wav')
create_spectorgram('output1.wav')

