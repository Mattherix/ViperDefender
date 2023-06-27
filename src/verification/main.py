import os
from threading import Thread
import time


def check():
    # Get all the files in the documents folder
    path = os.path.abspath("../../tests-files")
    files = os.listdir(path)
    # Get the size and content of each file
    files_content = []
    for file in files:
        object = {
            "size": os.stat(path + "\\" + file).st_size,
            "content": open(path + "\\" + file, "rb").read(),
            "name": file,
            "path": os.path.abspath(path + "\\" + file)
        }
        files_content.append(object)

    # Get the executable file that we want to run to test if it's a virus
    exectutable = os.path.abspath("../../tests-files\\test.exe")

    # Run the executable
    daemon = Thread(target=os.system, args=(exectutable,), daemon=True)
    daemon.start()
    time.sleep(30)
    

    # Test if the files have changed
    for file in files_content:
        # Check if the file have been deleted
        if not os.path.exists(file["path"]):
            print(f"File {file['name']} have been deleted")
            return False
        else:
            # Check if the file size have changed
            if os.stat(file["path"]).st_size != file["size"]:
                print(f"File {file['name']} have been modified")
                return False
            # Check if the file content have changed
            elif open(file["path"], "rb").read() != file["content"]:
                print(f"File {file['name']} have been modified")
                return False
    return True

if check():
    print("No virus detected")
else:
    print("Virus detected")