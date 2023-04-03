# NoLock   &nbsp;&nbsp;    <img src="/resources/moon.png" style="width:48px;height:48px;">
 Prevents the PC from auto-locking due to user inactivity.

This program will run in background and simulate user activity either by moving the mouse pointer or emulating some key press.

A small icon in the system tray will indicate the program is active.

If the user moves the mouse pointer or presses any key on the keyboard, then the inactivity timer will be reset, so no action will
be taken if the computer is actually used.

Program configuration is stored in file _config.ini_ : so far, the file must be changed manually (no configuration utility yet).

; EXAMPLE

```ini
; NoLock Configuration

[Keyboard]
; Keyboard parameters
KeysToPress = capslock, capslock  ; Keys to be pressed. Full list of accepted key names: https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys
KeyDelay = 500                    ; Delay between consecutive keystrokes (if more than one key is being pressed)

[Mouse]
; Mouse movement parameters
MaxRadius_X = 200                 ; Maximum horizontal cursor offset
MaxRadius_Y = 200                 ; Maximum vertical cursor offset

[Settings]
; Direct intervention
WaitTime = 180                    ; Timeout for user emulation (action will take place on expiry)
MoveMouse = False                 ; Enable/disable mouse emulation
PressKeys = True                  ; Enable disable keyboard emulation
MakeSound = True                  ; If True, the program will emit a short beep when inactivity timeout is reached

; User activity detection
DetectKeyPress = True             ; Enable/disable detection of keyboard activity (from user)
DetectMouseMove = True            ; Enable/disable detection of mouse activity (from user)
SkipIfUserActivity = True         ; True: program will take no action if the user presses a key and/or moves the mouse. False: Activity emulation will take place anyway.
```

