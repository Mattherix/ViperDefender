import os
import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
import requests
from src.client.fileListApp import FileListApp


class App:
    def __init__(self):
        self.path = os.path.expanduser("~\Downloads")
        self.userName = None
        self.userJwt = None
        self.files = os.listdir(self.path)
        # add a button to launch the app
        self.base_url = "http://localhost:7071/api"
        self.app = None
        # Etape de choix du dossier
        self.launch_folder_finder()
        # Possible login
        # self.launch_action()


    def launch_action(self):
        self.app = FileListApp()
        # daemon = Thread(target=self.app.mainloop)
        # daemon.setDaemon(True)
        # daemon.start()
        check_files = Thread(target=self.checkFiles)
        check_files.setDaemon(True)
        check_files.start()
        self.app.mainloop()

    def launch_folder_finder(self):
        self.window = tk.Tk()
        self.window.title("Viper Defender")
        # add the png logo
        self.logo = tk.PhotoImage(file="./assets/logo.png")
        self.window.iconphoto(False, self.logo)
        style = ttk.Style(self.window)
        style.theme_use("clam")
        self.window.geometry("400x200")
        self.window.resizable(False, False)
        # add an folder input
        # add a button to choose the folder
        self.folder_label = ttk.Label(self.window, text="Choose a folder to watch")
        # increase the size of the label
        self.folder_label.config(font=("Helvetica", 16))
        # remove the background of the label
        self.folder_label.config(background=self.window.cget("background"))
        self.folder_label.pack(pady=10)
        self.folder_button = ttk.Button(self.window, text="Choose folder", command=self.choose_folder)
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
            if new_files != self.files:
                # list the new files founded
                files_founded = list(set(new_files) - set(self.files))
                self.files = new_files
                for count, file in enumerate(files_founded):
                    # get the file to send them to an API
                    # send the file to the API
                    check_file_daemon = Thread(target=self.sendFile, args=(file, len(files_printed)))
                    check_file_daemon.setDaemon(True)
                    check_file_daemon.start()
                    total_files += 1
                    # add the name of the file to the window
                    files_printed.append(
                        {
                            "file": file,
                            "status": "Checking"
                        }
                    )
                    self.app.add_item(file, "Checking")
                    # add some styles to the label
            time.sleep(0.5)

    def sendFile(self,name, index):
        url = f"{self.base_url}/TestFile"
        # create a readable stream
        with open(f"{self.path}/{name}", "rb") as file:
            files = {
                "file": open(f"{self.path}/{name}", "rb")
            }
            response = requests.post(url, files=files)
            print(response)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            if response_json["status"] == "clean":
                self.app.update_item(index, name, "Clean")
            elif response_json["status"] == "malicious":
                self.app.update_item(index, name, "Malicious")
        else:
            self.app.update_item(index, name,"Error")