
# Less rudimentary workaround for https://github.com/pyinstaller/pyinstaller/issues/2379 :-)
# By Max1234-Ita, 2023
#
# Usage: just import the present module and call the cleanup_mei routine at the beginning of the main program.
# This will ensure that all tenmporary directories not belonging to any running instance of pyinstaller
# will be deleted.
#
# Example:
#
#   from pyinstaller_cleanup import cleanup_mei
#   cleanup_mei()
#
#   (continue program)
#
# ------------------------------------------------------------------------------------------------------------------

import os
import sys
import time

import psutil
from shutil import rmtree


def cleanup_mei():
    """
    :param resource_folder:     Directory used in the app to store resources (pictures, etc.)
    :param app_id:              Any string. Used to uniquely identify the program being run
    """
    debug = False

    standalone_app = getattr(sys, 'frozen', False)
    usertemp = os.getenv("TEMP")

    if standalone_app:
       tempdir = sys._MEIPASS

    else:
        tempdir = "."

    if debug:
        standalone_app = True
        tempdir = usertemp

    if standalone_app:
        pass
    if True:
        print("\nCleaning up temp files.")
        running_processes = {}
        print("Obtaining a list of running processes...")
        processlist = psutil.process_iter(['pid', 'name', 'username'])
        for proc in processlist:
            running_processes[str(proc.info["pid"])] = proc.info

        meicount = 0
        dirlist = os.listdir(tempdir)
        for item in dirlist:
            itempath = os.path.join(tempdir, item)
            if item.startswith("_MEI") and os.path.isdir(itempath):
                print(f"Checking '{itempath}' ")
                meipid = item[:-1].replace("_MEI", "")  # This is the PID of the launched script
                print(f"    Temporary directory for PID '{meipid}' found")

                if meipid in running_processes:
                    # The temp dir is in use, leave it alone.
                    print(f"    Process {meipid} is still running.\n    Skipped.\n")
                else:
                    # The temp dir does not belong to any running instance of PyInstaller. Remove it.
                    print(f"    Process not found. Removing '{itempath}'.\n")
                    try:
                        rmtree(itempath)
                        meicount += 1
                        print("    Success.")
                    except PermissionError:  # mainly to allow simultaneous pyinstaller instances
                        print(f"    Can't remove {item}. PermissionError.\n")

        print(f"{meicount} temporary folders deleted.\n")
        if not standalone_app and meicount > 0:
            time.sleep(5)
