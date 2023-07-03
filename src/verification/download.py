import urllib.request
import zipfile
import os
import shutil
from pathlib import Path

FILES_URL = "https://github.com/Mattherix/ViperDefender/archive/refs/heads/main.zip"
FILES_PATH = os.path.join(os.path.expanduser('~'), "Desktop")
ZIP_FILE = "files.zip"

EXTRACTED_FILES_PATH = os.path.join(FILES_PATH, "ViperDefender-main/tests-files/")

def download_and_unzip_files(url = FILES_URL, path = FILES_PATH):
    with urllib.request.urlopen(url) as f:
        with open(ZIP_FILE, "wb") as archive:
            archive.write(f.read())

    with zipfile.ZipFile(ZIP_FILE) as archive:
        for file in archive.namelist():
            if file.startswith('ViperDefender-main/tests-files/'):
                archive.extract(file, path)

if __name__ == '__main__':
    download_and_unzip_files(FILES_URL)
