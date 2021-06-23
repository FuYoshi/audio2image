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
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import cryptography
import io
from pydub.playback import play

def cryptify(image_data, key):
    """ Function that encrypts file with password, replacing original file
        with encrypted file.
    """

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000000,
        backend=cryptography.hazmat.backends.default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(key, "ASCII")))
    marker = bytes("STARTHASH", encoding="ASCII")
    fernet = Fernet(key)
    encData = fernet.encrypt(image_data)
    return encData, marker, salt

def decryptify(image_data, key, salt):
    """ Function that decrypts file with password, replacing encrypted file
        with decrypted file.
    """

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000000,
        backend=cryptography.hazmat.backends.default_backend()
    )
    try:
        key = base64.urlsafe_b64encode(kdf.derive(bytes(key, "ASCII")))
        fernet = Fernet(key)
        decdata = fernet.decrypt(image_data)
    except:
        print("incorrect password")
        sys.exit(1)
    return decdata


# Converts a .wav file to an image based on the data of the .wav file.
def wav_to_pixel(audio_file, output_filename, password):

    # Extracts data from the audio_file.
    with open(audio_file, 'rb') as f:
        data = binascii.hexlify(f.read())
    if password is not None:
        data, marker, salt = cryptify(data, password)

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
            gcd2 = int(num)
            gcd = int(w)
            break

    # Places pixels in the resolution grid.
    im = np.zeros([gcd2, gcd, 3], dtype=np.uint8)
    l = 0
    for q in range(0, gcd2):
        for p in range(0, gcd):
            im[q][p] = pixels[l]
            l += 1

    img = Image.fromarray(im)
    img.save(output_filename + '.png')
    if password is not None:
        with open(output_filename + '.png', 'ab') as fsf:
            fsf.write(marker + salt)


# Reconverts an image to an audio file based on the pixel values.
def image_to_wav(image, output_filename, password, output_type):
    # Extracts image data from image.
    if password is not None:
        with open(image, 'rb') as flf:
            marker = bytes("STARTHASH", encoding="ASCII")
            data = flf.read()
            salt = data.split(marker, 1)[1]
            data = data.split(marker, 1)[0]

    # Extracts image data from image.
    if password is not None:
        im = Image.open(io.BytesIO(data))
    else:
        im = Image.open(image).convert('RGB')
    width, height = im.size
    data = []

    # Extracts data from each individual pixel and puts them in an data list.
    for i in range(0, height):
        for j in range(0, width):
            if j == width - 1 and i == height - 1:
                r, g, b = im.getpixel((j,i))
                data.append(r)
                data.append(g)
                data.append(b)
            else:
                r, g, b = im.getpixel((j,i))
                data.append(r)
                data.append(g)
                data.append(b)

    # Data list is converted to a bytearry and the unhexified.
    sound_data = bytearray(data)
    if password is not None:
        sound_data = bytes(sound_data)
        sound_data = decryptify(sound_data, password, salt)
    sound_data2 = binascii.unhexlify(sound_data)

    # Sound data is converted into a .wav or .mp3 file based on the user
    # defined output type.
    song = AudioSegment.from_file(io.BytesIO(sound_data2), format="mp3")
    if output_type == "mp3":
        song.export(output_filename + ".mp3", format="mp3")
    else:
        song.export('temp.mp3', format="mp3")
        mp3_to_wav('temp.mp3', output_filename)
        os.remove('temp.mp3')

# Coverts a .wav file to a .mp3 file.
def wav_to_mp3(wav_file, output_filename):
    wav_audio = AudioSegment.from_file(wav_file, format="wav")
    wav_audio.export(output_filename + '.mp3', format="mp3")

# Converts a .mp3 file to a .wav file.
def mp3_to_wav(mp3_file, output_filename):
    mp3_audio = AudioSegment.from_file(mp3_file, format="mp3")
    mp3_audio.export(output_filename + '.wav', format="wav")

# Converts wav to compressed image.
def wav_to_image(sound, name, password):
    wav_to_mp3(sound, 'temp')
    wav_to_pixel('temp.mp3', name, password)
    os.remove('temp.mp3')

def mp3_to_image(sound, name):
    wav_to_pixel(sound, name)

# Parser used for command line arguments and for providing information on
# how to use this script.

def parser():
    parser = argparse.ArgumentParser()

        # Required and optional arguments
    required_name = parser.add_argument_group('required named arguments')
    parser.add_argument('-e', '--export-type',
                        dest='export_type',
                        help='export type when converting image to sound. Options are "mp3" and "wav"',
                        type=str)
    parser.add_argument('-p', '--password',
                        dest='password',
                        help='provide password for optional encryption/decryption, if none provided, encryption will not take place')
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
    password = args.password
    export_type = args.export_type
    mode = args.mode
    file = args.file
    filename = args.filename

    # Checks for the converter mode and uses the function.
    if mode == "ati":
        wav_to_image(file, filename, password)
    elif mode == "ita":
        image_to_wav(file, filename, password, export_type)


