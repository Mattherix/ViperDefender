import os
import sys
import time
import tkinter as tk


def checkFiles(window, files):
    total_files = 0
    files_printed = []
    while True:
        new_files = os.listdir(path)
        window.update()
        print("Checking files")
        if new_files != files:
            # list the new files founded
            files_founded = list(set(new_files) - set(files))
            files = new_files
            print("New files found!")
            for i in files_founded:
                total_files += 1
                # add the name of the file to the window
                label = tk.Label(window, text=i + " - Checking...")
                label.pack()
                label.place(y=(10 + 20 * total_files), x=10)
                files_printed.append(
                    {
                        "file" : i,
                        "label" : label,
                        "y" : (10 + 20 * total_files),
                        "x" : 10,
                        "status" : "Checking"
                    }
                )
                # add some styles to the label
                label.config(fg="black", font=("Courier", 9))
                print("Checking file: " + i)
        time.sleep(3)





if __name__ == '__main__':
    # Path to the Downloads folder
    path = os.path.expanduser("~/Downloads")

    # List of files in the Downloads folder
    files = os.listdir(path)

    # Create a tkinter window
    window = tk.Tk()
    window.title = "Files Ransom Checker"
    window.geometry("600x500")
    window.after(1000, checkFiles, window, files)
    window.mainloop()
    # Check if there are new files in the Downloads folder

