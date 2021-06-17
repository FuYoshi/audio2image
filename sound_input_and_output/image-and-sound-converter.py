
# Can record, play and display sounds from .wav files and user input.
import argparse
import pyaudio as pa
import wave
import binascii
import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
from PIL import Image

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


def create_spectorgram(audio_file):
    sample_rate, samples = wavfile.read('output1.wav')
    freq, times, spectrogram = signal.spectrogram(samples, sample_rate)

    plt.pcolormesh(np.log(spectrogram))
    plt.xlabel('Frequency (HZ)')
    plt.ylabel('Time (SEC)')
    plt.show()

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

    gcd = np.gcd(len(pixels), 700)
    im = np.zeros([gcd, int((len(pixels) / gcd)), 3], dtype=np.uint8)
    l = 0
    for q in range(0, gcd):
        for p in range(0, (int(len(pixels) / gcd))):
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

def mp3_to_pixel(audio_file):
    data = bytearray(open('output1.mp3', 'rb').read())
    pixels = []
    pixel = []

    for i in range(0, len(data)):
        if len(pixel) == 3:
            pixels.append(pixel)
            pixel = []
        else:
            pixel.append(data[i])

    print(pixels)
    print(len(pixels))
    gcd = np.gcd(len(pixels), 500)

    im = np.zeros([gcd, int((len(pixels) / gcd)), 3], dtype=np.uint8)
    l = 0
    for q in range(0, gcd):
        for p in range(0, (int(len(pixels) / gcd))):
            im[q][p] = pixels[l]
            l += 1

    img = Image.fromarray(im)
    img.save('test.png')

parser()
