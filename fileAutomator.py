from os.path import exists, expanduser
from shutil import move
from file_types import *

import binascii
import os

# finds user home directory
parent_dir = expanduser("~") + "/" + input("Choose a directory to organize: ") + "/"
dir_files = os.listdir(parent_dir)

# ignore .DS_Store and .localized Mac files
dir_files.pop(dir_files.index(".DS_Store"))
dir_files.pop(dir_files.index(".localized"))

print(dir_files)

for file in dir_files:
    full_file = parent_dir + file

    # open and read each file in binary format
    with open(full_file, "rb") as f:
        content = f.read()

    # convert file binary to hex signatures
    hexbin = str(binascii.hexlify(content))[2:8].upper()

    print(f"File {file} has a hexbin of {hexbin} so it is a .{bit_ext[hexbin]} file")

    # create a directory with the file and its respective extension
    for item in bit_ext.keys():
        if hexbin == item:
            directory = f"{bit_ext[item]}'s".upper()
            path = os.path.join(parent_dir, directory)

            if exists(path):
                move(full_file, path)
            else:
                os.mkdir(path)
                move(full_file, path)
