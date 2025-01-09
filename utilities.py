from os import path, mkdir, remove, symlink
from tkinter import messagebox
from tarfile import TarFile
from pyzstd import ZstdFile
from shutil import rmtree
from subprocess import Popen, CalledProcessError, CompletedProcess
from tqdm import tqdm
import variables

class ZstdTarFile(TarFile):
    """
    Butler makes use of Zstd for patch files, so we make a thin wrapper for it here
    """
    def __init__( self, name, mode='r', *, level_or_option=None, zstd_dict=None, **kwargs ):
        self.zstd_file = ZstdFile( name, mode, level_or_option=level_or_option, zstd_dict=zstd_dict )
        try:
            super().__init__( fileobj=self.zstd_file, mode=mode, **kwargs )
        except:
            self.zstd_file.close()
            raise

    def close( self ):
        try:
            super().close()
        finally:
            self.zstd_file.close()

def extract_file( staging_path, zip_file ):
    """
    Moved to fileutils.py
    """
    with ZstdTarFile( path.join( staging_path, zip_file ), mode='r' ) as tar:
        for member in tqdm(iterable=tar.getmembers(), total=len(tar.getmembers())):
            tar.extract(member=member, path=staging_path )
        
def do_symlink(installpath):
    """
    Linux servers require server.so to be symlinked to server_srv.so in order to run
    """
    for s in variables.TO_SYMLINK:
        if path.isfile(installpath + s[1]) and not path.islink(installpath + s[1]):
            remove(installpath + s[1])

        if not path.isfile(installpath + s[1]):
            symlink(installpath + s[0], installpath + s[1])

def run_process(process_args):
    """
    subprocess.run() does not have a way to terminate and keep track of subprocesses.
    So we keep track of the current process here, using a wrapper for POpen() instead.
    It's used in GUI when TKinter exits unexpectedly.
    """
    with Popen(process_args) as variables.CURRENT_PROCESS:
        try:
            stdout, stderr = variables.CURRENT_PROCESS.communicate()
        except:
            variables.CURRENT_PROCESS.kill()
            variables.CURRENT_PROCESS = None
            raise

        retcode = variables.CURRENT_PROCESS.poll()
        if retcode:
            variables.CURRENT_PROCESS = None
            raise CalledProcessError( retcode, process_args, output=stdout, stderr=stderr )

    variables.CURRENT_PROCESS = None
    return CompletedProcess(process_args, retcode, stdout, stderr)

def setup_staging_dirs(smpath):
    variables.STAGING_PATH = path.join( smpath, variables.STAGING_DIR_NAME )
    variables.INSTALL_PATH = smpath

    if not path.isdir(variables.STAGING_PATH):
        mkdir(variables.STAGING_PATH, 511)

def cleanup_staging_dirs():
    if path.isdir(variables.STAGING_PATH):
        rmtree(variables.STAGING_PATH)

def displayinfo(message: str, gui = False):
    print( message )
    if gui and not variables.SCRIPT_MODE:
        messagebox.showinfo(variables.GUI_TITLE, message)

def displayerror(message: str, gui = False):
    print(message)
    if gui and not variables.SCRIPT_MODE:
        messagebox.showerror(variables.GUI_TITLE, message)