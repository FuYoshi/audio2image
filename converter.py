import binascii
import sys
import argparse


def file_extract(image):
    with open(image, 'rb') as f:
        data = binascii.hexlify(f.read())
    marker = binascii.hexlify(bytes("STARTSOUND", encoding="ASCII"))
    data_s = binascii.a2b_hex(data.split(marker, 2)[2])
    ext = str(binascii.unhexlify(data.split(marker, 2)[1])).split("'", 2)[1]
    with open("result." + ext, 'wb') as image_file:
        image_file.write(data_s)


def file_merge(image, audio):
    with open(image, 'rb') as f:
        data = binascii.hexlify(f.read())
    marker = binascii.hexlify(bytes("STARTSOUND" + audio.split('.', 2)[2] +
                                    "STARTSOUND", encoding="ASCII"))
    with open(audio, 'rb') as fp:
        music = binascii.hexlify(fp.read())
    data = binascii.a2b_hex(data + marker + music)
    with open("result." + image.split('.', 2)[2], 'wb') as image_file:
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
