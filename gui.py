from tkinter import Tk, constants
from tkinter.ttk import Button, Frame, Entry, Label
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog, StringVar
from os import path, getcwd
from threading import Thread
import variables
from downloads import downloads_game_install, downloads_game_update, downloads_game_verify
import versions

def gui_on_entry_update(*args):
    variables.INSTALL_PATH = sourcemodspath_entry.get()
    gui_update_state(True)

def gui_open_directory():
    directory = filedialog.askdirectory()
    if directory:
        variables.INSTALL_PATH = directory
        sourcemodspath_entry.delete( 0, constants.END )
        sourcemodspath_entry.insert( 0, directory )

def gui_confirm_close():
    """
    Need to keep track of subprocesses in other threads when quitting the main thread.
    """
    if variables.GUI_LOCKSTATE:
        if variables.CURRENT_PROCESS:
            if messagebox.askokcancel( "Quit", "An operation is running! You might end up with corrupted files! Are you sure you want to exit?" ):
                variables.CURRENT_PROCESS.kill()
    
    root.destroy()

def gui_update_state(forceupdate = False):
    """
    Check button state every single frame. Only runs with TKinter enabled
    """
    if variables.SCRIPT_MODE:
        return

    root.after(1, gui_update_state)

    if not forceupdate:
        if variables.GUI_LOCKSTATE == variables.GUI_LOCKSTATE_PARITY:
            return
        
        variables.GUI_LOCKSTATE_PARITY = variables.GUI_LOCKSTATE

    if variables.GUI_LOCKSTATE:
        open_dir_button.config( state="disabled" )
        sourcemodspath_entry.config( state="disabled" )
        install_button.config( state="disabled" )
        update_button.config( state="disabled" )
        verify_button.config( state="disabled" )
    else:
        open_dir_button.config( state="active" )
        sourcemodspath_entry.config( state="normal" )

        # disable buttons for existing or missing installations
        installed_version = versions.get_installed_version()
        latest_version = list(variables.VERSION_LIST["versions"])[-1]

        if installed_version:
            current_revision_panel.config(foreground="#000")
            current_revision_panel.config(text=f"Current Revision: {installed_version}")
            latest_revision_panel.config(text=f"Latest Revision: {latest_version}")

            install_button.config( state="disabled" )

            if installed_version == latest_version:
                latest_revision_panel.config(foreground="#000")
                update_button.config( state="disabled" )
            else:
                latest_revision_panel.config(foreground="#f00")
                update_button.config( state="active" )

            verify_button.config( state="active" )
        else:
            current_revision_panel.config(text=f"Current Revision: Not found!")
            current_revision_panel.config(foreground="#f00")
            latest_revision_panel.config(foreground="#f00")

            latest_revision_panel.config(text=f"Latest Revision: {latest_version}")

            install_button.config( state="active" )
            update_button.config( state="disabled" )
            verify_button.config( state="disabled" )


def gui_game_install():
    if variables.CURRENT_PROCESS:
        return
    
    sourcemodspath = sourcemodspath_entry.get()
    if not sourcemodspath:
        messagebox.showerror( "Error", "Please enter a path to the Sourcemods folder..." )
        return
    
    Thread( name="gui_game_install_thread", target=downloads_game_install, args=[sourcemodspath], daemon=True ).start()

def gui_game_update():
    if variables.CURRENT_PROCESS:
        return
    
    sourcemodspath = sourcemodspath_entry.get()
    if not sourcemodspath:
        messagebox.showerror( "Error", "Please enter a path to the Sourcemods folder..." )
        return
    
    Thread( name="gui_game_update_thread", target=downloads_game_update, args=[sourcemodspath], daemon=True ).start()

def gui_game_verify():
    if variables.CURRENT_PROCESS:
        return
    
    sourcemodspath = sourcemodspath_entry.get()
    if not sourcemodspath:
        messagebox.showerror( "Error", "Please enter a path to the Sourcemods folder..." )
        return
    
    Thread( name="gui_game_verify_thread", target=downloads_game_verify, args=[sourcemodspath], daemon=True ).start()

def gui_init():
    global root
    global sourcemodspath_entry
    global open_dir_button
    global install_button
    global update_button
    global verify_button
    global current_revision_panel
    global latest_revision_panel

    # main window
    root = Tk()
    root.title(variables.GUI_TITLE)
    root.resizable(False, False)
    root.iconbitmap( path.join( variables.TF2CDOWNLOADER_PATH, variables.GUI_ICON ) )

    # banner
    image = Image.open( path.join( variables.TF2CDOWNLOADER_PATH, variables.GUI_BANNER ) )
    image = image.resize(variables.GUI_BANNER_DIMENSIONS)
    photo = ImageTk.PhotoImage(image)
    banner = Label(root, image=photo)
    banner.image = photo
    banner.pack(fill=constants.X)       

    # text above entry box frame
    current_revision_panel = Label(root, text="Current Revision:")
    current_revision_panel.pack()

    latest_revision_panel = Label(root, text="Latest Revision:")
    latest_revision_panel.pack()

    # entry box frame
    entry_frame = Frame(root, name="sourcemodspathentryboxframe")
    entry_frame.pack()

   # entry box itself. deferred until later due to button state management
    sourcemodspath_entry = Entry( entry_frame, width=65, name="sourcemodspathentrybox" )
    sourcemodspath_entry.grid( row=0, column=0, padx=10 )

    # select button next to entry box
    open_dir_button = Button(entry_frame, text="Select", width=5, command=gui_open_directory)
    open_dir_button.grid(row=0, column=1, padx=10)

    # action button frame
    button_frame = Frame(root, name="globalbuttonframe")
    button_frame.pack(pady=10)

    # install button
    install_button = Button(button_frame, text="Install", width=15, command=gui_game_install)
    install_button.grid(row=0, column=0, padx=10)

    # update button
    update_button = Button(button_frame, text="Update", width=15, command=gui_game_update)
    update_button.grid(row=0, column=1, padx=10)

    # verify button
    verify_button = Button(button_frame, text="Verify", width=15, command=gui_game_verify)
    verify_button.grid(row=0, column=2, padx=10)

    # set default path in entry fox. deferred until later for button management
    entry_var = StringVar()
    entry_var.trace_add("write", gui_on_entry_update)
    if variables.INSTALL_PATH is None:
        variables.INSTALL_PATH = getcwd()
    sourcemodspath_entry.config(textvariable=entry_var)
    sourcemodspath_entry.insert( 0, variables.INSTALL_PATH )

    # check for currently running threads upon exit
    root.protocol("WM_DELETE_WINDOW", gui_confirm_close)

    # start button state check
    gui_update_state(True)

    root.mainloop()