import binascii
import sys
import argparse


def file_extract(image):
    with open(image, 'rb') as f:
        data = binascii.hexlify(f.read())

    marker = bytes("STARTSOUND", encoding="ASCII")
    marker = binascii.hexlify(marker)
    data = data.split(marker, 1)[1]

    data = binascii.a2b_hex(data)
    with open("result.mp3", 'wb') as image_file:
        image_file.write(data)


def file_merge(image, audio):
    with open(image, 'rb') as f:
        data = binascii.hexlify(f.read())

    marker = bytes("STARTSOUND", encoding="ASCII")
    data += binascii.hexlify(marker)

    with open(audio, 'rb') as fp:
        music = binascii.hexlify(fp.read())

    data += music

    data = binascii.a2b_hex(data)
    with open("result.png", 'wb') as image_file:
        image_file.write(data)


parser = argparse.ArgumentParser()

parser.add_argument("-m", "--merge", nargs=2, help="Merge image and audio",
                    metavar=("image", "audio"))
parser.add_argument("-e", "--extract", help="Extract audio from image",
                    metavar="image")

args = parser.parse_args()

if (args.extract is None and args.merge is None):
    print("bruh")
    sys.exit(1)

if (args.extract is not None):
    file_extract(args.extract)
if (args.merge is not None):
    file_merge(args.merge[0], args.merge[1])
