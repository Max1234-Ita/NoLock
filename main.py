
import os
import sys
import time
import ctypes
import random
from datetime import timedelta
import threading
import subprocess

import pystray
import winsound
import win32api
import pyautogui

from PIL import Image
from pynput.keyboard  import Listener, Key

from pyinstaller_cleanup import cleanup_mei
from mbk_config import MBKConfig

version = "0.1.0"
about = f"NoLock v.{version} -- By Massimo Mula, 2023"

standalone_app = getattr(sys, 'frozen', False)  # Packages created by PyInstaller have 'frozen' attribute == True.
temp_folder = ""

interval_start = None
user_activity = False
exit_app = None

# This part is used when the script runs as a standalone file (by PyInstaller)
# app_id = "NoLock"
# resource_dir = 'resources'


def init():
    clear()
    print_configuration()


def strtobool(boolean_string, optionname=''):
    """
    Converts a string representing a binary value into a real boolean
    NOTE:
        Only strings corresponding to a "positive value" (i.e. "True", "OK", "Good", etc.)
        are converted to True (bool). All the others are considered as False (bool).

    :param boolean_string:
    :param optionname:
    :return:
    """
    bool_result = False
    true_strings = ['true', 'yes', 'ok', 'on', 'good' 'pass']
    try:
        if boolean_string.lower() in true_strings:
            bool_result = True
    except BaseException:
        print(f"An error occurred while processing value '{str(boolean_string)}' for optiom {optionname}")
    return bool_result


def clear():
    # Clears the console window
    lambda: os.system('cls')  # on Windows System
    # os.system('cls')
    # os.system('clear') #on Linux System


def print_configuration():
    print('\n')
    print(f"{about}\n"
          f"---------------------------------------\n")
    if detectmouse:
        print("Mouse activity detection enabled.")
    else:
        print("Mouse activity detection disabled.")

    if detectkeys:
        print(f"Keyboard activity detection enabled.\n")
    else:
        print(f"Keyboard activity detection disabled.\n")

    print('')

    if movemouse:
        print("Mouse activity emulation is enabled.\n")
        print(f'    Max movement radius (x) is {maxradius_x}')
        print(f'    Max movement radius (y) is {maxradius_y}')
    else:
        print("Mouse activity emulation is disabled.\n")

    if presskeys:
        print("Keyboard activity emulation is enabled.")
        print(f'    Key(s) to be pressed: {str(keystopress)}')
        print(f'    Key delay is {keydelay} ms.\n')
    else:
        print("Keyboard activity emulation is disabled.\n")

    print(f'Intervention time is set to {waittime} seconds.')
    print('\n'
          '-------------------------------------------------------'
          '\n')


def move_mouse():
    """
    Uses PyAutoGUI to move mouse cursor as specified by settings.

    NOTE:
    under some circumstancies, mouse movement performed by pyautoGUI is not considered as user interaction,
    so it might not be able to prevent the PC from auto-locking. If this is the case, the press_keys method
    can be used.

    :return: Nothing
    """
    global count

    x_displacement = random.randint(-1 * maxradius_x, maxradius_x)
    y_displacement = random.randint(-1 * maxradius_y, maxradius_y)

    print(f"[{count}] - Moving mouse ({x_displacement}, {y_displacement})")
    pyautogui.moveRel(x_displacement, y_displacement, 1)


def press_keys(keys=None, key_delay_ms=200):
    """
    Uses PyAutoGUI (.press) to emulate keystrokes.
    Valid keys are:
    ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
    'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
    'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
    'command', 'option', 'optionleft', 'optionright'
    ]

    :param keys:            Keys to be pressed (list)
    :param key_delay_ms:    Delay between consecutive keys (milliseconds)
    :return:    Nothing
    """
    global count

    if isinstance(keys, str):
        keys = [str(keys)]

    if not isinstance(keys, list):
        raise ValueError("Invalid key format. Please provide a list.")

    wait_ms = key_delay_ms / 1000
    if not keys:
        keys = ['capslock', 'capslock']     # Caps Lock is particular: in most keyboards it has a nice LED on it :-)

    print(f"\r[{count}] - Pressing keys ({str(keys)})")

    keycount = 0
    for k in keys:
        pyautogui.press(k)
        keycount += 1
        if keycount < len(keys):
            # This will skip the waiting after the last key is pressed
            time.sleep(wait_ms)


def detect_keypress():
    """
    The pynput.Listener allows to detect keyboard activity.
    Unfortunately it's a blocking task, so we need to use a concurrent thread to run it asynchronously.
    If some intercation with keyboard is detected, then the key_pressed global variable is set to True
    (must be reset externally)

    :return: Nothing
    """

    def on_press(k):
        """
        Check if user has pressed any key on the keyboard
        :param k    Key pressed
        :return:    Nothing
        """
        global key_pressed
        listener._suppress = False
        key_pressed = True

    with Listener(on_press=on_press) as listener:
        listener.join()


def time_format(seconds):
    formatted_time = "0:00:00"
    s = seconds % 60
    m = int((seconds - s) / 60)
    h = int((seconds - s) / 3600)
    formatted_time = f"{format(m, '02d')}:{format(s, '02d')}"
    if h > 0:
        formatted_time = f"{format(h, '02d')}:{formatted_time}"
    return formatted_time


def show_info():
    """
    Displays a Windows MessageBox with some information about this program.
    Called when the "About" option in the system tray bar is clicked.
    TODO - Same for Linux?

    MessageBox Styles:
     0 : OK
     1 : OK | Cancel
     2 : Abort | Retry | Ignore
     3 : Yes | No | Cancel
     4 : Yes | No
     5 : Retry | Cancel
     6 : Cancel | Try Again | Continue
    """
    if os.name == "nt":
        ctypes.windll.user32.MessageBoxW(None, about, "Info", 0)


def open_configfile():
    # Opens the configuration file in the default text editor.
    if os.name == "nt":
        p = subprocess.Popen(["notepad", "config.ini"])

    else:
        pass    # TODO -- Same for Linux?


def systray_clicked(icon, item):
    """
    Event reacting to clicks on sytem tray icon. Will show the option menu.
    :param icon:    Needed by pystray
    :param item:    needed by pystray
    :return:        Nothing
    """
    global exit_app
    if str(item) == "About":
        show_info()
        exit_app = False

    elif str(item) == "Open configuration file":
        open_configfile()

    elif str(item) == "Quit":
        icon.stop()
        exit_app = True
        sys.exit(0)


def show_systray_icon():
    global exit_app

    if standalone_app:
        # sys._MEIPASS is a temporary folder created by PyInstaller. Not available in standard environment.
        image_path = os.path.join(sys._MEIPASS, 'resources', "moon.ico")
    else:
        image_path = os.path.join('resources', 'moon.ico')

    icon_image = Image.open(image_path)

    systray_icon = pystray.Icon("NoLock", icon_image,
                                menu=pystray.Menu(
                                    pystray.MenuItem("Open configuration file", systray_clicked),
                                    pystray.MenuItem("About", systray_clicked),
                                    pystray.MenuItem("Quit", systray_clicked)
                                ))
    systray_icon.run_detached()     # This will display the icon in the traybar as asynchronous process.


if __name__ == '__main__':
    # Load program settings from config.ini
    if os.path.exists("config.ini"):
        programsettings = MBKConfig()
        detectkeys = strtobool(programsettings.get_option("Settings", "DetectKeyPress"), "DetectKeyPress")
        detectmouse = strtobool(programsettings.get_option("Settings", "DetectMouseMove"), "DetectMouseMove")
        presskeys = strtobool(programsettings.get_option("Settings", "PressKeys"), "PressKeys")
        kp = programsettings.get_option("Keyboard", "KeysToPress")
        keystopress = kp.replace(" ", "").split(",")
        keydelay = int(programsettings.get_option("Keyboard", "KeyDelay"))
        movemouse = strtobool(programsettings.get_option("Settings", "MoveMouse"), "MoveMouse")
        maxradius_x = int(programsettings.get_option("Mouse", "MaxRadius_X"))
        maxradius_y = int(programsettings.get_option("Mouse", "MaxRadius_Y"))
        waittime = int(programsettings.get_option("Settings", "WaitTime"))
        skipifuseractivity = strtobool(programsettings.get_option("Settings", "SkipIfUserActivity"), "SkipIfUserActivity")
        makesound = strtobool(programsettings.get_option("Settings", "MakeSound"), "MakeSound")

        mmover_enabled = True
        key_pressed = False
        t_elapsed = None
        keyboard_start = None

        count = 0

        pyautogui.FAILSAFE = False

        cleanup_mei()
        init()

        kb_thread = threading.Thread(target=detect_keypress)
        kb_thread.start()

        systray_thread = threading.Thread(target=show_systray_icon)
        systray_thread.start()

        ignore_keys = False     # Used when simulating keyboard activity
        user_activity = False
        interval_start = time.perf_counter()
        mouse_start = win32api.GetCursorPos()

        t_prev = 0
        interventions = 0
        last_remaining = -1
        while True:
            time.sleep(0.01)

            current_time = time.perf_counter()
            t_delta = current_time - interval_start
            t_remaining = waittime - int(t_delta)

            if detectkeys:
                # Reset the intervention countdown if user presses any key
                if key_pressed and not ignore_keys:
                    user_activity = True
                key_pressed = False

            if detectmouse:
                try:
                    current_position = win32api.GetCursorPos()
                    if current_position != mouse_start:
                        mouse_start = current_position
                        user_activity = True

                except BaseException as ex:
                    # Exception can occur when the PC is locked by the User.
                    pass

            if user_activity:
                interval_start = time.perf_counter()
                user_activity = False
                count = 0

            elif t_delta > waittime and mmover_enabled:
                # Start new time interval
                if makesound:
                    winsound.Beep(12000, 2)

                count += 1
                if movemouse:
                    # Move the mpuse pointer
                    move_mouse()
                if presskeys:
                    # Simulate key press
                    ignore_keys = True
                    press_keys(keystopress, keydelay)
                    key_pressed = False
                    ignore_keys = False

                interval_start = time.perf_counter()
                user_activity = False

            if t_remaining != last_remaining:
                print(f"\rActivity emulation will occur in {time_format(t_remaining)}.", end=" ")
                last_remaining = t_remaining

            elif exit_app:
                systray_thread.join()
                break

    else:
        print("\n\nFile 'config.ini' not found. Can't start program")

    print("\n\nProgram ended.")
    sys.exit(0)
