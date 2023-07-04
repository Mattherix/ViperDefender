import winreg
import os
import ctypes
from ctypes import wintypes

def add_to_startup(program_path):
    # Chemin complet vers l'exécutable à ajouter
    exe_path = os.path.abspath(program_path)

    # Ouvrir la clé de registre avec les droits administrateurs
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)

    # Ajouter la valeur
    winreg.SetValueEx(key, "NomDeLExecutable", 0, winreg.REG_SZ, exe_path)

    # Fermer la clé de registre
    winreg.CloseKey(key)

    print(f"L'exécutable {exe_path} a été ajouté au démarrage de Windows avec les droits administrateurs.")

    # Lancer l'exécutable avec les droits administrateurs
    ctypes.windll.shell32.ShellExecuteW(None, "runas", exe_path, None, None, 1)

# Exemple d'utilisation
add_to_startup("./dist/main.exe")