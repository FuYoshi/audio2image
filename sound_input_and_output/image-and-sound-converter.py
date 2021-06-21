##################################################
# Multimedia 2020-2021
# Coen de Graaf & Lennaert Feijtes and Yoshi Fu
##################################################
#
# File created and functions implemented by: Lennaert Feijtes (13439103)
# Description:
# This program allows the user to convert .wav and .mp3 files to .png images
# with the goal of compression in mind. It allows the user to store big audio
# files as smaller images which take up less space.
#
# HELP: python3 image-and-sound-converter.py -h
#
##################################################

# Libraries used for this program.
import argparse
import pyaudio as pa
import wave
import os
import binascii
import numpy as np
from PIL import Image
from pydub import AudioSegment

# Parser used for command line arguments and for providing information on
# how to use this script.
def parser():
    parser = argparse.ArgumentParser()

    # Required and optional arguments
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

    # Checks for the converter mode and uses the function.
    if mode == "ati":
        wav_to_pixel(file, filename)
    elif mode == "ita":
        image_to_wav(file, filename)

# Converts a .wav file to an image based on the data of the .wav file.
def wav_to_pixel(audio_file, output_filename):

    # Extracts data from the audio_file.
    with open(audio_file, 'rb') as f:
        data = binascii.hexlify(f.read())

    pixels = []
    pixel = []

    # Converts the data to pixels. Each pixel contains three data elements.
    for i in range(0, len(data)):
        if len(pixel) == 3:
            pixels.append(pixel)
            pixel = []

        pixel.append(data[i])

    if len(pixel) == 3:
        pixels.append(pixel)

    # Checks if the last pixel is complets filled and otherwise enters
    # generated data.
    if len(pixel) < 3 and len(pixel) > 0:
        while(len(pixel) < 3):
            pixel.append(0)

        pixels.append(pixel)

    gcd = 0
    gcd2 = 0

    # Determines the resolution for the image based on a divisor that is
    # greater than 100.
    for w in range(1, len(pixels)):
        num = len(pixels) / w
        if w >= 100 and num.is_integer() == True:
            gcd = int(num)
            gcd2 = int(w)
            break

    # Places pixels in the resolution grid.
    im = np.zeros([gcd2, gcd, 3], dtype=np.uint8)
    l = 0
    for q in range(0, gcd2):
        for p in range(0, gcd):
            im[q][p] = pixels[l]
            l += 1

    # Image is generated.
    img = Image.fromarray(im)
    img.save(output_filename + '.png')

# Reconverts an image to an audio file based on the pixel values.
def image_to_wav(image, output_filename):
    # Extracts image data from image.
    im = Image.open(image).convert('RGB')
    width, height = im.size
    data = []

    # Extracts data from each individual pixel and puts them in an data list.
    for i in range(0, height):
        for j in range(0, width):
            r, g, b = im.getpixel((j,i))
            data.append(r)
            data.append(g)
            data.append(b)

    # Data list is converted to a bytearry and the unhexified.
    sound_data = bytearray(data)
    sound_data2 = binascii.unhexlify(sound_data)

    # Sound data is converted into a .wav file.
    p = pa.PyAudio()
    wf = wave.open(output_filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pa.paInt16))
    wf.setframerate(44100)
    wf.writeframes(sound_data2)
    wf.close()

# Coverts a .wav file to a .mp3 file.
def wav_to_mp3(wav_file, output_filename):
    wav_audio = AudioSegment.from_file(wav_file, format="wav")
    wav_audio.export(output_filename + '.mp3', format="mp3")

# Converts a .mp3 file to a .wav file.
def mp3_to_wav(mp3_file, output_filename):
    mp3_audio = AudioSegment.from_file(mp3_file, format="mp3")
    mp3_audio.export(output_filename + '.wav', format="wav")

# Converts a .mp3 file to an image.
def mp3_to_image(mp3_file, image_filename):
    mp3_to_wav(mp3_file, "wav69")
    wav_to_pixel('wav69.wav', image_filename)
    os.remove("wav69.wav")

# Converts a image to a .mp3 file.
def image_to_mp3(png_image, output_filename):
    image_to_wav(png_image, 'wav69')
    wav_to_mp3('wav69.wav', output_filename)
    os.remove("wav69.wav")

parser()
