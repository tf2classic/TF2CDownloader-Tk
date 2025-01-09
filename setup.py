
from platform import system
from os import path
import variables
from tkinter import messagebox
import sys
from versions import update_version_list

if system() == 'Windows':
    import winreg

def init_install_path():
    """
    Find path to sourcemod folder.
    """
    if system() == 'Windows':
        try:
            steam_registry_path = r"SOFTWARE\\Valve\\Steam"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, steam_registry_path) as key:
                variables.INSTALL_PATH, _ = winreg.QueryValueEx(key, "SourceModInstallPath")
        except:
            variables.INSTALL_PATH = None
    else:
        try:
            sourcepath = None
            with open(path.expanduser(r"~/.steam/registry.vdf"), encoding="utf-8") as file:
                for _, line in enumerate(file):
                    if 'SourceModInstallPath' in line:
                        sourcepath = line[line.index('/home'):-1].replace(r'\\', '/')
                        break
                file.close()
            variables.INSTALL_PATH = sourcepath
        except Exception:
            variables.INSTALL_PATH = None
        
def init_binaries():
    """
    Select paths for required binaries.
    """
    if system() == 'Windows':
        # When we can detect that we're compiled using PyInstaller, we use their
        # suggested method of determining the location of the temporary runtime folder
        # to point to Aria2 and Butler.
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            variables.ARIA2C_BINARY = path.abspath(path.join(path.dirname(__file__), 'aria2c.exe'))
            variables.BUTLER_BINARY = path.abspath(path.join(path.dirname(__file__), 'butler.exe'))
        else:
            # When running as a script, we just select the Binaries folder directly for Aria2 and Butler.
            variables.ARIA2C_BINARY = 'Binaries/aria2c.exe'
            variables.BUTLER_BINARY = 'Binaries/butler.exe'
    else:
        # If we're running on Linux...
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            variables.ARIA2C_BINARY = path.abspath(path.join(path.dirname(__file__), 'aria2c'))
            variables.BUTLER_BINARY = path.abspath(path.join(path.dirname(__file__), 'butler'))
        else:
            variables.BUTLER_BINARY = 'Binaries/butler'
            variables.ARIA2C_BINARY = 'Binaries/aria2c'

def init_version_list():
    try:
        update_version_list()
        print("Fetched version list!")
    except:
        print("Could not get version list")
        if not variables.SCRIPT_MODE:
            messagebox.showerror("Error!", "Could not get version list!\n\nIf your internet connection is fine, our server could be having technical issues.")
        sys.exit(1)

def init_console():
    variables.SCRIPT_MODE = len(sys.argv) > 1

    if not sys.stdin or not sys.stdin.isatty():
        print("Looks like we're running in the background. We don't want that, so we're exiting.")
        sys.exit(1)

    # Disable QuickEdit so the process doesn't pause when clicked
    if system() == 'Windows':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), (0x4|0x80|0x20|0x2|0x10|0x1|0x00|0x100))

    if sys.stdout.encoding == 'ascii':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding == 'ascii':
        sys.stderr.reconfigure(encoding='utf-8')