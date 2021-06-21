import binascii
import sys

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

args = sys.argv
if len(args) < 3:
    print("usage: hex_reader.py <image_name>.png <audio_name>.mp3")
    sys.exit(1)
file_merge(args[1], args[2])