import os
import os
import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
import requests
from src.client.file_list_app import file_list_app
import hashlib

def get_file_hash(file_path, algorithm="sha256"):
    hash_obj = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        buf = file.read(65536)  # Read file in chunks for large files
        while len(buf) > 0:
            hash_obj.update(buf)
            buf = file.read(65536)
    return hash_obj.hexdigest()


class App:
    def __init__(self):
        self.path = os.path.expanduser("~\Downloads")
        self.userName = None
        self.userJwt = None
        self.files = os.listdir(self.path)
        # add a button to launch the app
        # self.base_url = "http://localhost:7071/api/"
        self.base_url = "https://viperdefense.azurewebsites.net/api/"
        self.app = None
        # Etape de choix du dossier
        self.launch_folder_finder()
        # Possible login
        # self.launch_action()


    def launch_action(self):
        self.app = file_list_app()
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
        url = f"{self.base_url}TestFile"
        id = None
        # create a readable stream

        with open(f"{self.path}/{name}", "rb") as file:
            files = {
                "file": open(f"{self.path}/{name}", "rb")
            }
            # Get the hash of the file
            # post session
            hash = get_file_hash(f"{self.path}/{name}")
            print("hash",hash)
            already_scan_test_response = requests.get(f"{self.base_url}Files?hash={hash}")
            print("already_scan_test_response",already_scan_test_response)
            if already_scan_test_response.status_code == 200:
                already_scan_test_response_json = already_scan_test_response.json()
                if already_scan_test_response_json["session_result"] == "clean":
                    self.app.update_item(index, name, "Clean")
                elif already_scan_test_response_json["session_result"] == "malicious":
                    self.app.update_item(index, name, "Malicious")
                return

            # Create session url
            create_session_url = f"{self.base_url}Session"
            create_session_response = requests.post(create_session_url)
            if create_session_response.status_code == 201:
                create_session_response_json = create_session_response.json()
                id = create_session_response_json["_id"]

            response = requests.post(url, files=files)
            print("VirusTOtalresp",response)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            if response_json["status"] == "clean":
                self.app.update_item(index, name, "Clean")
            elif response_json["status"] == "malicious":
                self.app.update_item(index, name, "Malicious")
            hash = get_file_hash(f"{self.path}/{name}")
            aza = requests.post(f"{self.base_url}Files?hash={hash}&result={response_json['status']}")
            print("aza",aza)
            requests.patch(f"{self.base_url}Session/{id}", json={"session_ended": True, "session_result": response_json['status']})
        else:
            self.app.update_item(index, name,"Error")