""" This script is designed to append the data of an audio file to the data of
    an already existing image, deleting the audio file. The process can be re-
    verted, the audio and image data are extracted from the "2 in 1" image. And
    will both be stored in an audio and image file with the original names,
    deleting the "2 in 1" image.
"""

import sys
import argparse
import os


def file_merge(image, audio):
    """ Function for merging image and audio file, deleting original audio
        file.
    """
    if not os.path.isfile(image):
        print("This image does not exist in the current directory.")
        sys.exit(1)
    if not os.path.isfile(audio):
        print("This audio file does not exist in the current directory.")
        sys.exit(1)
    with open(audio, 'rb') as a:
        audio_data = a.read()

    ext = bytes(audio, "ascii")
    marker = bytes("STARTSOUND", "ascii")

    with open(image, 'ab') as i:
        i.write(marker + ext + marker + audio_data)
    os.remove(audio)
    return i


def file_extract(image):
    """ Function for extracting audio and image from "2 in 1" image, storing
        the audio and image in seperate files, and deleting the "2 in 1" image.
    """

    if not os.path.isfile(image):
        print("This image does not exist in the current directory.")
        sys.exit(1)
    with open(image, 'rb') as i:
        data = i.read()

    marker = bytes("STARTSOUND", "ascii")
    audio_data = data.split(marker, 2)[2]
    ext_audio = data.split(marker, 2)[1].decode()
    image_data = data.split(marker, 2)[0]

    os.remove(image)
    with open(image, 'wb') as im:
        im.write(image_data)
    with open(ext_audio, 'wb') as a:
        a.write(audio_data)
    return im, a


parser = argparse.ArgumentParser()

parser.add_argument("-m", "--merge", nargs=2, help="Merge image and audio",
                    metavar=("image", "audio"))
parser.add_argument("-e", "--extract", help="Extract audio from image",
                    metavar="image")

args = parser.parse_args()

# if (args.extract is None and args.merge is None):
#     print("Incorrect usage, add flag --help for help")
#     sys.exit(1)

if (args.extract is not None):
    file_extract(args.extract)
if (args.merge is not None):
    file_merge(args.merge[0], args.merge[1])
