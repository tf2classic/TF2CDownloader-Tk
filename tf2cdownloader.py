import setup
import variables
import sys
from gui import gui_init
from tui import tui_init
from os import path

if __name__ == "__main__":
    variables.TF2CDOWNLOADER_PATH = path.abspath(path.dirname(__file__))
    setup.init_console()
    setup.init_version_list()
    setup.init_downloader_update()
    setup.init_install_path()
    setup.init_binaries()

    if not variables.SCRIPT_MODE:
        gui_init()
    else:
        tui_init()