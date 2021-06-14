import binascii
import sys

def file_extract(image):
    with open(image, 'rb') as f:
        data = binascii.hexlify(f.read())

    marker = bytes("STARTSOUND", encoding="ASCII")
    marker = binascii.hexlify(marker)
    data = data.split(marker, 1)[1]

    data = binascii.a2b_hex(data)
    with open("result.mp3", 'wb') as image_file:
        image_file.write(data)

args = sys.argv
if len(args) < 2:
    print("usage: img_to.py <image_name>.png")
    sys.exit(1)
file_extract(args[1])