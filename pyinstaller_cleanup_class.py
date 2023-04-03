
# Less rudimentary workaround for https://github.com/pyinstaller/pyinstaller/issues/2379 :-)
# By Max1234Ita, 2023
#
# in the Class below, the initialization will store a flag file inside the temporary directory created by the
# running instance of PyInstaller.
# The file name will be the "app_id" passed as argument to the __init__ method, while the created file will contain
# the PID (Process ID) of the running script.
#
# The cleanup_mei method will then chack the directories present at the temp path (sys._MEIPASS): if the flag file
# is found AND the PID registerd there does not belong to any running process, then the entire directory can be
# removed.
#
# Usage:
#
#
# Just import the present module at the beginning of the main script and initialize the class;
# The cleanup_mei method can be then called at any time, even though it's recommended to use it
# at the begininng of the execution.
#
# Example:
#   from pyinstaller_cleanup import PynstallerCleanup
#   (... do stuff ...)
#   resource_dir = 'resources'
#   app_id = "MyApp"                  #  <--- File [tempdir]/resources/MyApp.pid will be created
#   pyinst = PynstallerCleanup(resource_dir, app_id)
#   pyinst.cleanup_mei()
#
#   (... do stuff ...)
#
# ------------------------------------------------------------------------------------------------------------------

import os
import sys
import psutil
from shutil import rmtree


class PynstallerCleanup:
    def __init__(self, resource_folder, app_id):
        """
        :param resource_folder:     Directory used in the app to store resources (pictures, etc.)
        :param app_id:              Any string. Used to uniquely identify the program being run
        """
        debug = True

        self.standalone_app = getattr(sys, 'frozen', False)
        usertemp = os.getenv("TEMP")

        if self.standalone_app:
            self.tempdir = sys._MEIPASS
            self.resource_folder = os.path.join(self.tempdir, resource_folder)

        else:
            self.tempdir = "."
            self.resource_folder = resource_folder

        if debug:
            self.tempdir = usertemp

        pid = os.getpid()
        self.pidfile = f"{app_id}_pid"
        pidfile_path = os.path.join(self.resource_folder, self.pidfile)
        f = open(pidfile_path, "w")
        f.write(str(pid))
        f.close()

    def cleanup_mei(self):
        """

        """
        if self.standalone_app:
            pass
        if True:
            running_processes = {}
            pidlist = psutil.pids()     # PID of every running process
            processlist = psutil.process_iter(['pid', 'name', 'username'])
            for proc in processlist:
                running_processes[str(proc.info["pid"])] = proc.info

            print("\nCleaning up temp files...")
            dirlist = os.listdir(self.tempdir)
            for item in dirlist:
                itempath = os.path.join(self.tempdir, item)
                if item.startswith("_MEI") and os.path.isdir(itempath):     # and not item.endswith(current_mei):
                    print(f"Checking '{itempath}' ")
                    pidfile_path = os.path.join(itempath, self.resource_folder, self.pidfile)
                    meipid = item[:-1].replace("_MEI", "")
                    print(f"    Temporary directory for PID '{meipid}' found")

                    if meipid in running_processes:
                        print(f"    Process {meipid} is running. Skipping.")
                    else:
                        # The temp dir does not belong to any running instance of this program. Remove it.
                        print(f"    Process not found. Removing '{itempath}'.")
                        try:
                            rmtree(itempath)
                            print("    Success.")
                        except PermissionError:  # mainly to allow simultaneous pyinstaller instances
                            print(f"    Can't remove {item}. PermissionError.")
                    pidfile_path = ""
