# NaviFile - A file management automator for macOS and Windows
# Designed and built by Jai Amin

from libraries import *

# setup tkinter GUI
win = tk.Tk()
win.title("NaviFile - File Management Made Easy")

# window setup
win_width = 700
win_height = 450
cen_width = int(win.winfo_screenwidth()/2 - (win_width/2))
cen_height = int(win.winfo_screenheight()/2 - (win_height/2))
win.geometry(f"{win_width}x{win_height}+{cen_width}+{cen_height}")
win.resizable(False, False)

# default style widgets
s = ttk.Style()
s.configure(".", font="Lato 14")
s.configure("TButton", font="Lato 15")

# logo
old_image = tk.PhotoImage(file="~/Pictures/navifile/logo.png")
image = old_image.subsample(2, 2)
logo = ttk.Label(win, image=image)
logo.pack(pady=(30, 15))

heading1 = ttk.Label(win, text="NaviFile", font="Lato 30 bold")
heading1.pack()

heading2 = ttk.Label(win, text="A file management automator for macOS & Windows that makes it"
                               " easy to organize and navigate through a variety of files.",
                     font="Lato 17", wraplength=350, justify="center")
heading2.pack(pady=(10, 0))

get_dir_num = ttk.Label(win, text="1. ", font="Lato 17 bold")
get_dir_num.pack(pady=(0, 75), padx=(80, 5), side="left")

# initialize with empty text in order to replace text when directory changes
get_dir_label = ttk.Label(win, text="", wraplength=500, font="Lato 14 bold")


def get_dir():
    global dir_name

    # ask user to select directory and display selection as label
    dir_name = filedialog.askdirectory(mustexist=True)
    short_dir_name = "📂 " + dir_name.split("/")[-1]

    if dir_name == "":
        short_dir_name = "❌ None"
        progress_bar["value"] = 0
        run_script_button.state(["disabled"])
        run_script_button["text"] = "Complete step 1"
    else:
        progress_bar["value"] = 50
        run_script_button.state(["!disabled"])
        run_script_button["text"] = "Make changes"

    get_dir_label["text"] = f"Selected folder:  {short_dir_name}"
    get_dir_label.pack(padx=(0, 0))
    get_dir_label.place(relx=0.15, rely=0.85)

    # change button features once directory selected
    get_dir_button["text"] = "Change folder"


get_dir_button = ttk.Button(win, text="Choose folder", width=15, command=get_dir)
get_dir_button.pack(pady=(0, 75), side="left")

var1 = tk.IntVar()
include_subf = ttk.Checkbutton(win, text="Include subfolders", variable=var1,
                               onvalue=1, offvalue=0)
include_subf.pack(padx=(0, 0))
include_subf.place(relx=0.1537, rely=0.766)


def file_manager(directory):
    # finds user home directory and gets desired directory
    parent_dir = f"{directory}/"
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
            try:
                with open(full_file, "rb") as f:
                    content = f.read()
            except RecursionError:
                continue

            # convert file binary to hex signatures
            try:
                hex_bin = str(binascii.hexlify(content))[2:10].upper()
            except KeyError:
                print(f"Error reading the {file}")

            # create a directory with the file and its respective extension
            for item in hexa_sig.keys():

                def path_exists(p):
                    if exists(p):
                        move(full_file, p)
                        # else create a new one first, then move the file into it
                    else:
                        os.mkdir(p)
                        move(full_file, p)

                try:
                    if item in hex_bin:
                        directory = hexa_sig[item]
                        path = os.path.join(parent_dir, directory)
                        path_exists(path)

                except FileNotFoundError:
                    dir_unknown = "Unknown"
                    path_unknown = os.path.join(parent_dir, dir_unknown)
                    path_exists(path_unknown)
                    continue

        except IsADirectoryError:
            try:
                if var1.get() == 1:
                    sub_parent = f"{dir_name}/{file}"
                    file_manager(sub_parent)
            except FileNotFoundError:
                continue
            # add read sub-folders option here with if statement


def success_actions():
    call(["open", dir_name])
    get_dir_label["text"] = "Changes made successfully ✅"
    progress_bar["value"] = 100


# when button clicked, file_manager() script runs
run_script_button = ttk.Button(win, text="Complete step 1", width=15,
                               command=lambda: [file_manager(dir_name),
                                                success_actions()])
run_script_button.pack(pady=(0, 75), padx=(5, 80), side="right")
run_script_button.state(["disabled"])

run_script_num = ttk.Label(win, text="2. ", font="Lato 17 bold")
run_script_num.pack(pady=(0, 75), side="right")

progress_bar = ttk.Progressbar(win, orient="horizontal", length=100,
                               mode="determinate", value=0)
progress_bar.pack(side="bottom", pady=(0, 10))

win.mainloop()
