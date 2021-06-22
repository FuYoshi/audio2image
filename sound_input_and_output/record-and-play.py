##################################################
# Multimedia 2020-2021
# Coen de Graaf & Lennaert Feijtes and Yoshi Fu
##################################################
#
# File created and functions implemented by: Lennaert Feijtes (13439103)
# Description:
# This program allows the user record and play .wav files.
#
# HELP: python3 record-and-play.py -h
#
##################################################


import pyaudio as pa
import wave
import argparse

# Parser used for command line arguments and for providing information on
# how to use this script.
def parser():
    parser = argparse.ArgumentParser()

    # Required and optional arguments
    required_name = parser.add_argument_group('required named arguments')
    required_name.add_argument('--option',
                               required='True',
                               choices=('record','play'),
                               dest='option',
                               default='record',
                               help='record or play a sound (default: record)',
                               type=str
                              )
    parser.add_argument('-p', '--play',
                        action='store',
                        metavar='file',
                        dest='file',
                        help='file that will be played')
    parser.add_argument('-r', '--record',
                        action='store',
                        metavar='file',
                        dest='filename',
                        help='filename if recording')
    parser.add_argument('-d', '--duration',
                        action='store',
                        metavar='duration',
                        dest='duration',
                        help='duration of recording',
                        type=int)
    args = parser.parse_args()

    mode = args.option
    play = args.file
    filename = args.filename
    duration = args.duration

    # Checks for the mode of the user and exectues the right based on the mode.
    if mode == "record":
        record(filename, duration)
    elif mode == "play":
        play_audio(play)

# This function lets the user record a sound using their microphone. This
# recording is converted to a .wav file.
def record(outputFile, duration):
    CHUNK = 1024
    FORMAT = pa.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = duration

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
    wf = wave.open(outputFile + '.wav', 'wb')
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

parser()