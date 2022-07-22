# Files - A modern file manager & organizer for Windows/macOS

from os.path import exists, expanduser
from shutil import move
from file_types import *

import binascii
import os

# find home directory, get directory to be organized
parent_dir = expanduser("~") + "/" + input("Choose a directory to organize: ") + "/"
dir_files = os.listdir(parent_dir)

# ignore .DS_Store and .localized Mac files
dir_files.pop(dir_files.index(".DS_Store"))
dir_files.pop(dir_files.index(".localized"))

for file in dir_files:
    full_file = parent_dir + file

    # open and read file in binary format
    with open(full_file, "rb") as f:
        content = f.read()

    # convert binary to hex signatures
    try:
        hex_bin = str(binascii.hexlify(content))[2:10].upper()
    except KeyError:
        print(f"Error reading the {file}")

    # create directory with file and its extension
    for item in bit_ext.keys():
        if item in hex_bin:
            directory = bit_ext[item]
            path = os.path.join(parent_dir, directory)

            # if directory exists, move the file into it
            if exists(path):
                move(full_file, path)
            # else create new directory first, then move the file into it
            else:
                os.mkdir(path)
                move(full_file, path)
