"""
Tiny module that currently just establishes
the temp paths and some variables for other
modules to use.
"""
SCRIPT_MODE = False

GAME_DIR_NAME = "tf2classic"
STAGING_DIR_NAME = "tf2cdownloader-staging"
BUTLER_STAGING_DIR_NAME = "butler-staging"
SOURCE_URL = 'https://wiki.tf2classic.com/kachemak/'
CURRENT_PROCESS = None

TF2CDOWNLOADER_PATH = None
INSTALL_PATH = None
STAGING_PATH = None

VERSION_LIST = None

# GUI Elements
GUI_TITLE = "TF2CDownloader"
GUI_ICON = "tf2c.ico"
GUI_BANNER = "tf2cbanner.png"
GUI_BANNER_DIMENSIONS = (479, 115)
GUI_LOCKSTATE = False
GUI_LOCKSTATE_PARITY = False

BUTLER_BINARY = None
ARIA2C_BINARY = None
ARIA2C_DEFAULT_ARGS = [
    '--max-connection-per-server=16', 
    '-UTF2CDownloader2023-05-27',
    '--allow-piece-length-change=true', 
    '--disable-ipv6=true', 
    '--max-concurrent-downloads=16', 
    '--optimize-concurrent-downloads=true', 
    '--check-certificate=false', 
    '--check-integrity=true', 
    '--auto-file-renaming=false', 
    '--continue=true', 
    '--allow-overwrite=true', 
    '--console-log-level=error', 
    '--summary-interval=0', 
    '--bt-hash-check-seed=false', 
    '--seed-time=0', 
]

# Only on Linux
TO_SYMLINK = [
    ["/bin/server.so", "/bin/server_srv.so"]
]