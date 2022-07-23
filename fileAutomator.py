from tkinter import *
from os.path import exists, expanduser
from shutil import move
from file_types import *

import binascii
import os

win = Tk()
win.title("FileOS - A modern file manager")
win.geometry("750x250")

label = Label(win, text="FileOS - A modern file manager for Windows/macOS")
label.pack(pady=20)

entry = Entry(win, width=20)
entry.focus_set()
entry.pack(pady=20)


def file_manager():
    # finds user home directory and gets desired directory to be organized
    parent_dir = expanduser("~") + "/" + entry.get() + "/"
    dir_files = os.listdir(parent_dir)

    # ignore .DS_Store and .localized Mac files
    if ".DS_Store" in dir_files:
        dir_files.pop(dir_files.index(".DS_Store"))
    if ".localized" in dir_files:
        dir_files.pop(dir_files.index(".localized"))

    for file in dir_files:
        full_file = parent_dir + file

        # open and read each file in binary format
        with open(full_file, "rb") as f:
            content = f.read()

        # convert file binary to hex signatures
        try:
            hex_bin = str(binascii.hexlify(content))[2:10].upper()
        except KeyError:
            print(f"Error reading the {file}")

        # create a directory with the file and its respective extension
        for item in bit_ext.keys():
            if item in hex_bin:
                directory = bit_ext[item]
                path = os.path.join(parent_dir, directory)

                # if directory exists, then move the file into it
                if exists(path):
                    move(full_file, path)
                # else create a new one first, then move the file into it
                else:
                    os.mkdir(path)
                    move(full_file, path)


button = Button(win, text="Run FileOS", width=20, command=file_manager)
button.pack(pady=20)


win.mainloop()
