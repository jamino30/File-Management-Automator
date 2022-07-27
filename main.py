# NaviFile - A file management automator for macOS and selfdows
# Designed and built by Jai Amin

from tkinter import ttk, filedialog
from os.path import exists
from shutil import move
from file_types import hexa_sig
from subprocess import call

import binascii as bin
import os as os
import tkinter as tk


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # set window title and icon
        self.title("NaviFile - File Management Made Easy")
        self.iconphoto(False, tk.PhotoImage(file="logo.png"))

        # configure window sizing
        self_width = 700
        self_height = 450
        cen_width = int(self.winfo_screenwidth() / 2 - (self_width / 2))
        cen_height = int(self.winfo_screenheight() / 2 - (self_height / 2))
        self.geometry(f"{self_width}x{self_height}+{cen_width}+{cen_height}")
        self.resizable(False, False)

        # initialize container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initialize frames
        self.frames = {}
        for F in (HomePage, MainPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # show home page frame first
        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.logo_image = tk.PhotoImage(file="logo.png").subsample(2, 2)
        logo_home = ttk.Label(self, image=self.logo_image)
        logo_home.pack(pady=(50, 35))

        heading = ttk.Label(self, text="Welcome!", font="Lato 20 bold")
        heading.pack()

        description = ttk.Label(self,
                                text="NaviFile is a file management automator for macOS and Windows that makes "
                                     "it easy to organize and navigate through a large variety of files based "
                                     "on its hexadecimal signatures (rather than its \"extension\").",
                                font="Lato 16", wraplength=400, justify="center")
        description.pack(pady=(20, 40))

        continue_button = ttk.Button(self, text="Enter NaviFile",
                                     command=lambda: controller.show_frame(MainPage))
        continue_button.pack()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Takes only 3 steps...", font="Lato 18 bold")
        label.pack(pady=(25, 0))

        self.logo_image = tk.PhotoImage(file="logo.png").subsample(5, 5)
        logo_main = ttk.Label(self, image=self.logo_image)
        logo_main.pack()
        logo_main.place(relx=0.02, rely=0.02)

        get_dir_num = ttk.Label(self, text="1. ", font="Lato 17 bold")
        get_dir_num.pack()
        get_dir_num.place(relx=0.1, rely=0.2)

        get_dir_num_desc = ttk.Label(self, text="Choose a folder whose files you would like to organize "
                                                "based on all the file's true extensions",
                                     font="Lato 15", wraplength=515)
        get_dir_num_desc.pack()
        get_dir_num_desc.place(relx=0.15, rely=0.2)

        self.get_dir_button = ttk.Button(self, text="Choose folder", width=15,
                                         command=self.get_dir)
        self.get_dir_button.pack()
        self.get_dir_button.place(relx=0.15, rely=0.32)

        # initialize with empty text in order to replace text when directory changes
        self.get_dir_label = ttk.Label(self, text="", font="Lato 14 bold")

        run_script_num = ttk.Label(self, text="2. ", font="Lato 17 bold")
        run_script_num.pack()
        run_script_num.place(relx=0.1, rely=0.45)

        run_script_num_desc = ttk.Label(self, text="Indicate whether or not you would like to organize all files "
                                                   "inside all first level subfolders in your selected folder.",
                                        font="Lato 15", wraplength=515)
        run_script_num_desc.pack()
        run_script_num_desc.place(relx=0.15, rely=0.45)

        self.var1 = tk.IntVar()
        include_subf = ttk.Checkbutton(self, text="Include subfolders", variable=self.var1, onvalue=1, offvalue=0)
        include_subf.pack()
        include_subf.place(relx=0.15, rely=0.57)

        run_script_num = ttk.Label(self, text="3. ", font="Lato 17 bold")
        run_script_num.pack()
        run_script_num.place(relx=0.1, rely=0.7)

        run_script_button_desc = ttk.Label(self, text="Before you \"Make changes\", confirm your selected folder.\n"
                                                      "Any changes made are not unreversible once made.",
                                           font="Lato 15", wraplength=515)
        run_script_button_desc.pack()
        run_script_button_desc.place(relx=0.15, rely=0.7)

        # when button clicked, file_manager() script runs
        self.run_script_button = ttk.Button(self, text="Complete step 1", width=15,
                                            command=lambda: [self.file_manager(self.dir_name),
                                                             self.success_actions()])
        self.run_script_button.pack()
        self.run_script_button.state(["disabled"])
        self.run_script_button.place(relx=0.15, rely=0.83)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=100, mode="determinate", value=0)
        self.progress_bar.pack(side="bottom")

    def get_dir(self):
        # ask user to select directory and display selection as label
        self.dir_name = filedialog.askdirectory(mustexist=True)
        short_dir_name = "📂 " + self.dir_name.split("/")[-1]

        if self.dir_name == "":
            short_dir_name = ""
            self.progress_bar["value"] = 0
            self.run_script_button.state(["disabled"])
            self.run_script_button["text"] = "Complete step 1"
        else:
            self.progress_bar["value"] = 50
            self.run_script_button.state(["!disabled"])
            self.run_script_button["text"] = "Make changes"

        self.get_dir_label["text"] = short_dir_name
        self.get_dir_label.pack()
        self.get_dir_label.place(relx=0.41, rely=0.3275)

        # change button features once directory selected
        self.get_dir_button["text"] = "Change folder"

    def file_manager(self, directory):
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
                    hex_bin = str(bin.hexlify(content))[2:10].upper()
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
                    if self.var1.get() == 1:
                        sub_parent = f"{self.dir_name}/{file}"
                        self.file_manager(sub_parent)
                except FileNotFoundError:
                    continue
                # add read sub-folders option here with if statement

    def success_actions(self):
        call(["open", self.dir_name])
        self.get_dir_label["text"] = "Changes made successfully ✅"
        self.progress_bar["value"] = 100


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
