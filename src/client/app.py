import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
import requests
from src.client.file_list_app import file_list_app
import hashlib
import shutil
import subprocess

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
        self.quarantine_path = os.path.expanduser("~\quarantine")
        self.verified_download_path = os.path.expanduser("~\\verified")
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
                    # if file is not a .tmp
                    if file.endswith(".tmp") or file.endswith(".crdownload") or file.endswith(".part") or file.endswith(".download"):
                        continue
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
        # move to quarantine
        self.move_to_quarantine(f"{self.path}/{name}")

        with open(f"{self.quarantine_path}/{name}", "rb") as file:
            files = {
                "file": open(f"{self.quarantine_path}/{name}", "rb")
            }
            # Get the hash of the file
            # post session
            hash = get_file_hash(f"{self.quarantine_path}/{name}")
            print("hash",hash)
            already_scan_test_response = requests.get(f"{self.base_url}Files?hash={hash}")
            print("already_scan_test_response",already_scan_test_response)
            if already_scan_test_response.status_code == 200:
                already_scan_test_response_json = already_scan_test_response.json()
                if already_scan_test_response_json["session_result"] == "clean":
                    self.move_out_of_quarantine(name)
                    self.app.update_item(index, name, "Clean")
                elif already_scan_test_response_json["session_result"] == "malicious":
                    self.app.update_item(index, name, "Malicious")
                    self.delete_file(name)
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
            hash = get_file_hash(f"{self.quarantine_path}/{name}")
            requests.post(f"{self.base_url}Files?hash={hash}&result={response_json['status']}")
            requests.patch(f"{self.base_url}Session/{id}", json={"session_ended": True, "session_result": response_json['status']})
            if response_json["status"] == "clean":
                self.move_out_of_quarantine(name)
                self.app.update_item(index, name, "Clean")
            elif response_json["status"] == "malicious":
                self.delete_file(name)
                self.app.update_item(index, name, "Malicious")
        else:
            self.app.update_item(index, name,"Error")

    def move_to_quarantine(self, file_path):
        # if there are a folder called quarantine at the root of the os
        # move the file to the folder
        if (not os.path.isdir(self.quarantine_path)):
            os.mkdir(self.quarantine_path)

        # if the folder quarantine doesn't need admin rights
        # give the rights to the folder to accept only admin to open it
        # Define the icacls command to check the existing permissions
        existing_permissions = os.stat(self.quarantine_path).st_file_attributes
        administrators_permission = 0x40000000  # Full control permission for Administrators

        if existing_permissions & administrators_permission == 0:

            # Specify the path to the folder
            folder_path = self.quarantine_path

            # Define the icacls command to modify the permissions
            command = f"icacls \"{folder_path}\" /inheritance:r /remove *S-1-5-32-545 /T"

            # Run the command using subprocess
            result = subprocess.run(command, shell=True, text=True)

            # Print the output and error messages

            if result.returncode == 0:
                print("Folder permissions modified successfully.")
            else:
                print("Failed to modify folder permissions.")

        else:
            print("Folder already has the specified permissions.")

        # move the file to the folder
        shutil.move(file_path, self.quarantine_path)

    def move_out_of_quarantine(self, file):
        # if there are a folder called quarantine at the root of the os
        # move the file to the folder
        if (not os.path.isdir(self.verified_download_path)):
            os.mkdir(self.verified_download_path)

        source_file = f"{self.quarantine_path}/{file}"
        destination_file = f"{self.verified_download_path}/{file}"
        retry_limit = 5  # Maximum number of retries
        retry_delay = 10  # Delay between retries in seconds

        for retry_count in range(retry_limit):
            try:
                # copy the file to the folder
                shutil.copy(source_file, destination_file)
                break  # File moved successfully, exit the loop
            except PermissionError:
                print(f"File '{file}' is in use by another process. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        else:
            print(f"Failed to move file '{file}' after {retry_limit} retries.")

    def delete_file(self, file):
        pass

