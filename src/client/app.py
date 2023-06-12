import os
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog
from threading import Thread
from src.client.fileListApp import FileListApp


class App:
    def __init__(self):
        self.path = os.path.expanduser("~\Downloads")
        self.userName = None
        self.userJwt = None
        self.files = os.listdir(self.path)
        # add a button to launch the app
        self.app = None
        # Etape de choix du dossier
        self.launch_folder_finder()

        # Possible login
        # self.launch_action()


    def launch_action(self):
        self.app = FileListApp()
        daemon = Thread(target=self.app.mainloop)
        daemon.setDaemon(True)
        daemon.start()
        self.checkFiles()

    def launch_folder_finder(self):
        self.window = tk.Tk()
        self.window.title("Choose a folder")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        self.window.config(bg="#2C2F33")
        # add an folder input
        # add a button to choose the folder
        self.folder_button = tk.Button(self.window, text="Choose folder", command=self.choose_folder)
        self.folder_button.pack(pady=10)
        self.window.mainloop()
    def choose_folder(self):
        self.folder_input = filedialog.askdirectory()
        self.path = self.folder_input
        self.files = os.listdir(self.path)
        self.window.destroy()
        self.launch_action()

    def checkFiles(self):
        total_files = 0
        files_printed = []
        while True:
            new_files = os.listdir(self.path)
            self.app.update()
            print("Checking files")
            if new_files != self.files:
                # list the new files founded
                files_founded = list(set(new_files) - set(self.files))
                self.files = new_files
                print("New files found!")
                for i in files_founded:
                    total_files += 1
                    # add the name of the file to the window
                    files_printed.append(
                        {
                            "file": i,
                            "status": "Checking"
                        }
                    )
                    self.app.add_item(i, "Checking")
                    # add some styles to the label
                    print("Checking file: " + i)
            time.sleep(3)