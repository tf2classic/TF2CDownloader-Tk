import variables
import json
import httpx
import hashlib
from platform import system
from sys import argv
from os import path

def update_version_list():
    version_remote = httpx.get(variables.SOURCE_URL + variables.SOURCE_JSON)
    variables.VERSION_LIST = json.loads(version_remote.text)

def latest_version():
    version_json = variables.VERSION_LIST["versions"]
    last_key = list(version_json.keys())[-1]
    lastver = version_json[last_key]
    return lastver

def update_rev_file():
    """
    The previous launcher/updater leaves behind a rev.txt file with the old internal revision number.
    To avoid file bloat, we reuse this, but replace it with the game's semantic version number.
    To obtain the game's semantic version number, we do some horrible parsing of the game's version.txt
    file, which is what the game itself uses directly to show the version number on the main menu, etc.
    """
    try:
        install_dir = path.join(variables.INSTALL_PATH, variables.GAME_DIR_NAME)
        with open( install_dir + "/version.txt", "r" ) as old_version_file:
            old_version = old_version_file.readlines()[1]
            _, _, after = old_version.partition('=')

            if len(after) > 0:
                old_version = after
            old_version = old_version.replace('.', '')

            with open( install_dir + "/rev.txt", "w" ) as new_version_file:
                new_version_file.write(old_version)
        return True
    except Exception as e:
        return False

def get_installed_version():
    if update_rev_file():
        install_dir = path.join(variables.INSTALL_PATH, variables.GAME_DIR_NAME)
        try:
            with open( install_dir + "/rev.txt", "r" ) as local_version_file:
                return local_version_file.read().rstrip('\n')
        except:
            return 0
    else:
        return 0

def check_for_game_updates(verify = False):
    """
    WARNING: Returns Exception upon error! Handle separately\n
    This function checks the local version against the list of remote versions and deems firstly, if an update is necessary, and secondarily, whether it's more efficient to update or reinstall.
    """
    local_version = get_installed_version()
    if not local_version:
        raise Exception("No game installation detected in this path!")

    # First, as a basic sanity check, do we know about this version at all?
    # We don't want to try to patch from 746 or some other nonexistent version.
    version_json = variables.VERSION_LIST["versions"]
    if local_version not in version_json:
        raise Exception("The version of your game is unknown.\nIt could be corrupted. Try reinstalling the game.")

    # Now we're checking the latest version, to see if we're already up-to-date.
    if not verify:
        latest_version = sorted(version_json.keys(), reverse=True)[0]
        if not verify and local_version == latest_version:
            raise Exception("The game is already up to date!")

        # Finally, we ensure our local version has a patch available before continuing.
        patches_json = variables.VERSION_LIST["patches"]
        if local_version not in patches_json:
            raise Exception("No patch could be found for your game version.\nIt could be too old. Try reinstalling the game.")
    
    return True

def hash_script():
    h = hashlib.sha512()
    with open(argv[0], 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)
    return h.hexdigest()

def check_downloader_update():
    try:
        if system() == 'Windows':
            print(f"{variables.SOURCE_URL}{variables.DOWNLOADER_HASH_WINDOWS}")
            remote_hash = httpx.get( f"{variables.SOURCE_URL}{variables.DOWNLOADER_HASH_WINDOWS}" )
        else:
            remote_hash = httpx.get( f"{variables.SOURCE_URL}{variables.DOWNLOADER_HASH_LINUX}" )
    except Exception as e:
        raise Exception(f"WARNING: TF2CDownloader failed to check itself for updates, potentially out-of-date.\n\nDownload the latest version from {variables.DOWNLOAD_PAGE_URL}")

    remote_hash_string = remote_hash.text
    remote_hash_string = remote_hash_string.rstrip('\n')

    if remote_hash_string != hash_script():
        raise Exception(f"TF2CDownloader has an update available. Your current version may not work properly.\n\nDownload the latest version from {variables.DOWNLOAD_PAGE_URL}")
