from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from os.path import exists, expanduser
from shutil import move
from file_types import *

import binascii
import os

# setup tkinter GUI
win = Tk()
win.title("FileOS - A modern file manager")
win.geometry("700x250")
win.resizable(False, False)

# style widgets
s = ttk.Style()
s.configure(".", font=("Lato", 15, "bold"))

heading1 = ttk.Label(win, text="FileOS", font="Lato 30 bold")
heading1.pack(pady=(50, 0))

heading2 = ttk.Label(win, text="A modern file manager for Windows/macOS", font="Lato 17 bold")
heading2.pack(pady=(10, 0))

get_dir_label = ttk.Label(win, text="1. ", font="Lato 15 bold")
get_dir_label.pack(padx=(80, 5), side="left")


# get desired directory
def get_dir():
    global dir_name
    dir_name = fd.askdirectory()


get_dir = ttk.Button(win, text="Choose a directory", width=15, command=get_dir)
get_dir.pack(side="left")


def file_manager():
    # finds user home directory and gets desired directory
    parent_dir = dir_name + "/"
    dir_files = os.listdir(parent_dir)

    # ignore .DS_Store and .localized Mac files
    if ".DS_Store" in dir_files:
        dir_files.pop(dir_files.index(".DS_Store"))
    if ".localized" in dir_files:
        dir_files.pop(dir_files.index(".localized"))

    for file in dir_files:
        try:
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

        except IsADirectoryError:
            continue


# When button clicked, file_manager() script runs
run_script = ttk.Button(win, text="Run FileOS", width=15, command=file_manager)
run_script.pack(pady=40, padx=(5, 80), side="right")

run_script_label = ttk.Label(win, text="2. ", font="Lato 15 bold")
run_script_label.pack(side="right")

win.mainloop()
