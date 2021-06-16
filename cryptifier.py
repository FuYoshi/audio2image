import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import sys
import os
import argparse
import pathlib


def cryptify(image, key):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000000
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(key, "ASCII")))
    marker = bytes("STARTHASH", encoding="ASCII")
    with open(image, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encData = fernet.encrypt(data)
    ext = pathlib.Path(image).suffix
    with open("result" + ext, 'wb') as image_file:
        image_file.write(encData + marker + salt)


def decryptify(image, key):
    with open(image, 'rb') as f:
        data = f.read()

    marker = bytes("STARTHASH", encoding="ASCII")
    extracted_salt = data.split(marker, 1)[1]
    extracted_data = data.split(marker, 1)[0]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=extracted_salt,
        iterations=1000000
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(key, "ASCII")))
    try:
        fernet = Fernet(key)
        decdata = fernet.decrypt(extracted_data)
    except:
        print("Incorrect password")
        sys.exit(1)
    ext = pathlib.Path(image).suffix
    with open("result2" + ext, 'wb') as image_file:
        image_file.write(decdata)

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--decrypt", help="Decrypt data",
                    metavar="file")
parser.add_argument("-e", "--encrypt", help="Encrypt data",
                    metavar="file")
parser.add_argument("-p", "--password",
                    help="Set password for decryption/encryption",
                    metavar="password")

args = parser.parse_args()

if ((args.encrypt is None and args.decrypt is None) or args.password is None):
    print("Incorrect usage, add flag --help for help")
    sys.exit(1)
if args.decrypt is not None:
    decryptify(args.decrypt, args.password)
else:
    cryptify(args.encrypt, args.password)
