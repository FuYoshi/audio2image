
# Can record, play and display sounds from .wav files and user input.
import argparse
import pyaudio as pa
import wave
import os
import binascii
import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from PIL import Image
from pydub import AudioSegment, audio_segment

def parser():
    parser = argparse.ArgumentParser()

    required_name = parser.add_argument_group('required named arguments')
    parser.add_argument('-e', '--encryption',
                        action='store_true',
                        dest='encrypt',
                        help='encription of file')
    required_name.add_argument('--mode',
                        required='True',
                        choices=('ati', 'ita'),
                        dest='mode',
                        default='ati',
                        help='conversion option (default: audio to image)',
                        type=str)
    required_name.add_argument('-i', '--input',
                        required='True',
                        action='store',
                        dest='file',
                        metavar='file',
                        help='input file for conversion')
    required_name.add_argument('-o', '--output',
                        required='True',
                        action='store',
                        dest='filename',
                        metavar='filename',
                        help='filename for output file',
                        type=str)
    args = parser.parse_args()

    encr = args.encrypt
    mode = args.mode
    file = args.file
    filename = args.filename

    if mode == "ati":
        wav_to_pixel(file, filename)
    elif mode == "ita":
        image_to_wav(file, filename)

def wav_to_pixel(audio_file, output_filename):
    with open(audio_file, 'rb') as f:
        data = binascii.hexlify(f.read())

    pixels = []
    pixel = []
    for i in range(0, len(data)):
        if len(pixel) == 3:
            pixels.append(pixel)
            pixel = []

        pixel.append(data[i])

    if len(pixel) == 3:
        pixels.append(pixel)

    if len(pixel) < 3 and len(pixel) > 0:
        while(len(pixel) < 3):
            pixel.append(0)

        pixels.append(pixel)
    gcd = 0
    gcd2 = 0
    for w in range(1, len(pixels)):
        num = len(pixels) / w
        if w >= 100 and num.is_integer() == True:
            gcd = int(num)
            gcd2 = int(w)
            break

    im = np.zeros([gcd2, gcd, 3], dtype=np.uint8)
    l = 0
    for q in range(0, gcd2):
        for p in range(0, gcd):
            im[q][p] = pixels[l]
            l += 1

    img = Image.fromarray(im)
    img.save(output_filename + '.png')

def image_to_wav(image, output_filename):
    im = Image.open(image).convert('RGB')
    width, height = im.size
    data = []
    for i in range(0, height):
        for j in range(0, width):
            r, g, b = im.getpixel((j,i))
            data.append(r)
            data.append(g)
            data.append(b)
    sound_data = bytearray(data)
    sound_data2 = binascii.unhexlify(sound_data)

    p = pa.PyAudio()
    wf = wave.open(output_filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pa.paInt16))
    wf.setframerate(44100)
    wf.writeframes(sound_data2)
    wf.close()

def wav_to_mp3(wav_file, output_filename):
    wav_audio = AudioSegment.from_file(wav_file, format="wav")
    wav_audio.export(output_filename + '.mp3', format="mp3")

def mp3_to_wav(mp3_file, output_filename):
    mp3_audio = AudioSegment.from_file(mp3_file, format="mp3")
    mp3_audio.export(output_filename + '.wav', format="wav")

def mp3_to_image(mp3_file, image_filename):
    mp3_to_wav(mp3_file, "wav69")
    wav_to_pixel('wav69.wav', image_filename)
    os.remove("wav69.wav")

def image_to_mp3(png_image, output_filename):
    image_to_wav(png_image, 'wav69')
    wav_to_mp3('wav69.wav', output_filename)
    os.remove("wav69.wav")

#parser()
mp3_to_image('output1.mp3', 'imageMP3')
image_to_mp3('imageMP3.png', 'newMP3')