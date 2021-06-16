import binascii
import sys
import argparse
from hashlib import sha256
import string
import random


def rand_gen(size=15, chars=string.digits + string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))


def hasher(password, salt):
    h = sha256()
    password_salted = password + salt
    h.update(password_salted.encode('utf-8'))
    return h.hexdigest()


def file_extract(image, password):
    with open(image, 'rb') as f:
        data = binascii.hexlify(f.read())

    if (password is None and
       binascii.hexlify(bytes("STARTHASH", encoding="ASCII")) in data):
        print("file is password protected")
        sys.exit(1)
    if password is not None:
        if binascii.hexlify(bytes("STARTHASH", encoding="ASCII")) not in data:
            print("file is not password protected")
            sys.exit(1)
        extracted_hash = binascii.hexlify(bytes("STARTHASH", encoding="ASCII"))
        extracted_hash = binascii.unhexlify(data.split(extracted_hash, 1)[1])
        extracted_hash = str(extracted_hash)[2:len(extracted_hash)+2]
        password_hash = hasher(password, extracted_hash[:15])

    marker = binascii.hexlify(bytes("STARTSOUND", encoding="ASCII"))
    data_s = data.split(marker, 2)[2]
    if password is not None:
        shash = binascii.hexlify(bytes("STARTHASH", encoding="ASCII"))
        data_s = data_s.split(shash, 1)[0]
    ext = str(binascii.unhexlify(data.split(marker, 2)[1])).split("'", 2)[1]
    if password is not None:
        if extracted_hash[15:len(extracted_hash)] == password_hash:
            pass_string = ''.join(str(ord(c)) for c in password)
            data_s = str(binascii.a2b_hex(data_s)).strip("'b")
            decrypted_data = int(data_s) // int(pass_string)
            decrypted_data = bytes.fromhex(f'{decrypted_data:x}')
            with open("result." + ext, 'wb') as image_file:
                image_file.write(decrypted_data)
        else:
            print("password is incorrect")
            sys.exit(1)
    else:
        data_s = binascii.a2b_hex(data_s)
        with open("result." + ext, 'wb') as image_file:
            image_file.write(data_s)


def file_merge(image, audio, password):
    with open(image, 'rb') as f:
        data = binascii.hexlify(f.read())
    marker = binascii.hexlify(bytes("STARTSOUND" + audio.split('.', 2)[2] +
                                    "STARTSOUND", encoding="ASCII"))
    with open(audio, 'rb') as fp:
        music = binascii.hexlify(fp.read())

    marker2 = binascii.hexlify(bytes("STARTHASH", encoding="ASCII"))

    if password is not None:
        salt = rand_gen()
        hash = salt + hasher(password, salt)
        pass_string = ''.join(str(ord(c)) for c in password)
        data_sample = music
        encrypted_data = int(data_sample, 16) * int(pass_string)
        encrypted_data = bytes(str(encrypted_data), encoding="utf-8")
        encrypted_data = binascii.hexlify(encrypted_data)
        hash = binascii.hexlify(bytes(hash, encoding="utf-8"))
        data = binascii.a2b_hex(data + marker + encrypted_data +
                                marker2 + hash)
        with open("result." + image.split('.', 2)[2], 'wb') as image_file:
            image_file.write(data)
    else:
        data = binascii.a2b_hex(data + marker + music)
        with open("result." + image.split('.', 2)[2], 'wb') as image_file:
            image_file.write(data)


parser = argparse.ArgumentParser()

parser.add_argument("-m", "--merge", nargs=2, help="Merge image and audio",
                    metavar=("image", "audio"))
parser.add_argument("-e", "--extract", help="Extract audio from image",
                    metavar="image")
parser.add_argument("-p", "--password",
                    help="Set password for decryption/encryption",
                    metavar="password")

args = parser.parse_args()

# if (args.extract is None and args.merge is None):
#     print("Incorrect usage, add flag --help for help")
#     sys.exit(1)

if (args.extract is not None):
    file_extract(args.extract, args.password)
if (args.merge is not None):
    file_merge(args.merge[0], args.merge[1], args.password)
