import sys
from os import getcwd
import versions
from downloads import downloads_game_install, downloads_game_update, downloads_game_verify
import variables

def tui_setup_path():
    """
    Choose setup path, but without user interference.
    """
    if len(sys.argv) > 2:
        variables.INSTALL_PATH = sys.argv[2].rstrip('"')
    else:
        if variables.INSTALL_PATH is None:
            variables.INSTALL_PATH = getcwd()

        print(f"Installation location not specified, will assume: {variables.INSTALL_PATH}")

def tui_init():
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print(
        '''Usage: TF2CDownloader [COMMAND] [PATH]
Installation utility for TF2 Classic.

If no arguments are provided, the downloader will be ran in setup mode, in
which a series of questions will be asked to install the game for a regular
user. This is what's used when opening the downloader from the desktop.

Valid commands:
--install           installs TF2 Classic into a new folder inside PATH
--update            updates the pre-existing TF2 Classic installation in its
                    folder inside PATH
--verify            verifies existing installation in the folder inside PATH
--help              shows this

PATH is the folder containing TF2 Classic's folder. This is usually the
sourcemods folder for clients, or the Source dedicated server folder for
servers.

If PATH isn't provided, then it'll be replaced with the detected path to the
sourcemods folder in the Steam directory. If it couldn't be detected, then the
path will be the current work directory.'''
        )
        sys.exit(0)

    tui_setup_path()

    if sys.argv[1] == "--install":
        if versions.get_installed_version():
            print( f"TF2 Classic is already installed in {variables.INSTALL_PATH}. Aborting!" )
            sys.exit(1)

        downloads_game_install(variables.INSTALL_PATH)
        sys.exit(0)
    elif sys.argv[1] == "--update":
        if not versions.get_installed_version():
            print( f"TF2 Classic is not installed in {variables.INSTALL_PATH}. Aborting!" )
            sys.exit(1)

        downloads_game_update(variables.INSTALL_PATH)
        sys.exit(0)
    elif sys.argv[1] == "--verify":
        if not versions.get_installed_version():
            print( f"TF2 Classic is not installed in {variables.INSTALL_PATH}. Aborting!" )
            sys.exit(1)

        downloads_game_verify(variables.INSTALL_PATH)
        sys.exit(0)
    else:
        print(_("Unrecognised command. Try --help"))
        sys.exit(1)
