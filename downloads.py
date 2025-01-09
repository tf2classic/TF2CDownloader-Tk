import utilities
from os import path
import variables
from shutil import move, rmtree
import versions
import traceback

# ###################
#
# INSTALL
#
# ###################

def downloads_game_install(smpath):
    """
    Download and extract the latest version of the game
    """
    variables.GUI_LOCKSTATE = True

    try:
        utilities.setup_staging_dirs(smpath)
        versions.update_version_list()
        lastver = versions.latest_version()

        print( "Downloading the archive..." )
        aria2c_args = [variables.ARIA2C_BINARY, *variables.ARIA2C_DEFAULT_ARGS, "-d", variables.STAGING_PATH, variables.SOURCE_URL + lastver["url"]]
        utilities.run_process(aria2c_args)

        print( "Download complete!\nExtracting the archive, please wait patiently." )

        utilities.extract_file( variables.STAGING_PATH, lastver["file"] )
        print( "Extraction complete!\nMoving game files..." )
        move( path.join( variables.STAGING_PATH, variables.GAME_DIR_NAME ), variables.INSTALL_PATH )

        utilities.cleanup_staging_dirs()
        utilities.displayinfo( "Installation complete! Remember to restart Steam.", True )

    except Exception as e:
        traceback.print_exc()
        print( str(e) )
        utilities.displayerror( "Installation failed! See console for details.", True )

    variables.GUI_LOCKSTATE = False

# ###################
#
# UPDATE
#
# ###################

def butler_verify(local_version):
    version_json = variables.VERSION_LIST["versions"]
    signature_url = version_json[local_version]["signature"]
    heal_url = version_json[local_version]["heal"]

    butler_verify_args = [ variables.BUTLER_BINARY, "verify", variables.SOURCE_URL + signature_url, path.join( variables.INSTALL_PATH, variables.GAME_DIR_NAME ), "--heal=archive," + variables.SOURCE_URL + heal_url ]
    
    print( "Verifying..." )
    utilities.run_process(butler_verify_args)

def butler_patch(local_version):
    patch_json = variables.VERSION_LIST["patches"]
    patch_url = patch_json[local_version]["url"]
    patch_file = patch_json[local_version]["file"]

    if path.isdir(variables.STAGING_PATH):
        rmtree(variables.STAGING_PATH)
    
    utilities.displayinfo( "Downloading the archive..." )
    aria2c_args = [ variables.ARIA2C_BINARY, *variables.ARIA2C_DEFAULT_ARGS, "-d", variables.STAGING_PATH, variables.SOURCE_URL + patch_url ]
    utilities.run_process(aria2c_args)

    utilities.displayinfo( "Download complete!" )
          
    utilities.displayinfo( "Patching your game with the new update, please wait patiently." )
    butler_path = path.join(variables.STAGING_PATH, variables.BUTLER_STAGING_DIR_NAME)
    patch_path = path.join(variables.STAGING_PATH, patch_file)
    game_path = path.join(variables.INSTALL_PATH, variables.GAME_DIR_NAME)
    butler_args = [ variables.BUTLER_BINARY, "apply", "--staging-dir", butler_path, patch_path, game_path ]
    utilities.run_process(butler_args)

def downloads_game_update(smpath):
    variables.GUI_LOCKSTATE = True

    try:
        versions.check_for_game_updates()
    except Exception as e:
        utilities.displayerror( str(e), True )
        variables.GUI_LOCKSTATE = False
        return

    try:
        utilities.setup_staging_dirs(smpath)
        local_version = versions.get_installed_version()
        print(local_version)
        butler_verify(local_version)
        butler_patch(local_version)
        utilities.cleanup_staging_dirs()
        utilities.displayinfo( "Update complete!", True )

    except Exception as e:
        traceback.print_exc()
        print( str(e) )
        utilities.displayerror( "Update failed! See console for details.", True )

    variables.GUI_LOCKSTATE = False

# ###################
#
# VERIFY
#
# ###################

def downloads_game_verify(smpath):
    variables.GUI_LOCKSTATE = True

    try:
        versions.check_for_game_updates(True)
    except Exception as e:
        utilities.displayerror( str(e), True )
        variables.GUI_LOCKSTATE = False
        return

    try:
        local_version = versions.get_installed_version()
        butler_verify(local_version)
        utilities.displayinfo( "Verification complete!", True )

    except Exception as e:
        traceback.print_exc()
        print( str(e) )
        utilities.displayerror( "Verification failed! See console for details.", True )

    variables.GUI_LOCKSTATE = False