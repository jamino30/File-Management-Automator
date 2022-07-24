# FileMan - A modern file manager and organizer for Windows/macOS
# Designed and built by Jai Amin

from libraries import *

# setup tkinter GUI
win = tk.Tk()
win.title("FileMan - A file management automator")
win.geometry("700x450")
win.resizable(False, False)

# default style widgets
s = ttk.Style()
s.configure(".", font=("Lato", 15, "bold"))

# logo
old_image = tk.PhotoImage(file="~/Pictures/bg.png")
image = old_image.subsample(3, 3)
logo = ttk.Label(win, image=image)
logo.pack(pady=(30, 0))

heading1 = ttk.Label(win, text="FileMan", font="Lato 30 bold")
heading1.pack()

heading2 = ttk.Label(win, text="A modern file manager for Windows/macOS", font="Lato 17 bold")
heading2.pack(pady=(10, 0))

get_dir_num = ttk.Label(win, text="1. ", font="Lato 15 bold")
get_dir_num.pack(padx=(80, 5), side="left")

# initialize with empty text in order to replace text when directory changes
get_dir_label = ttk.Label(win, text="", wraplength=500)


def get_dir():
    global dir_name

    # ask user to select directory and display selection as label
    dir_name = filedialog.askdirectory()
    get_dir_label["text"] = dir_name
    get_dir_label.pack(padx=(0, 0))
    get_dir_label.place(relx=0.15, rely=0.85)

    # change button features once directory selected
    get_dir_button["text"] = "Change directory"


get_dir_button = ttk.Button(win, text="Choose directory", width=15, command=get_dir)
get_dir_button.pack(side="left")


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

                def path_exists(p):
                    if exists(p):
                        move(full_file, p)
                        # else create a new one first, then move the file into it
                    else:
                        os.mkdir(p)
                        move(full_file, p)

                try:
                    if item in hex_bin:
                        directory = bit_ext[item]
                        path = os.path.join(parent_dir, directory)
                        path_exists(path)

                except FileNotFoundError:
                    dir_unknown = "Unknown"
                    path_unknown = os.path.join(parent_dir, dir_unknown)
                    path_exists(path_unknown)
                    continue

        except IsADirectoryError:
            continue
            # add read sub-folders option here with if statement

    messagebox.showinfo("Status Update", "FileMan Successful")


# When button clicked, file_manager() script runs
run_script = ttk.Button(win, text="Run FileMan", width=15, command=file_manager)
run_script.pack(pady=40, padx=(5, 80), side="right")

run_script_num = ttk.Label(win, text="2. ", font="Lato 15 bold")
run_script_num.pack(side="right")


win.mainloop()

