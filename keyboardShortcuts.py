from pynput import keyboard
import win32api, win32con

import sys
sys.path.append("..")
from creed_modules import creedFunctions


def functionComboDetected():
    pass
    # print("Combo detected")


def functionOnPress(key):
    global comboReleased

    # print("Key was pressed: " + str(key))

    if key == keyboard.Key.caps_lock:
        # keyboardControllerObj.press(keyboard.Key.ctrl_l)
        keyboardControllerObj.press(keyboard.Key.f13)


    if key in comboList:
        # print(str(key) + " is one of the combo keys")
        currentPressedKeys.append(key)
        # print("currentPressedKeys is " + str(currentPressedKeys))

    if list(dict.fromkeys(currentPressedKeys)) == comboList and comboReleased:
        comboReleased = False
        functionComboDetected()


def functionOnRelease(key):
    global capsLockReleaseCount
    global comboReleased



    if key == keyboard.Key.caps_lock:

        capsLockReleaseCount = capsLockReleaseCount + 1
        print("capsLockReleaseCount: " + str(capsLockReleaseCount))

        if capsLockReleaseCount % 2 == 1:
            creedFunctions.pynputPressRel(keyboardControllerObj, keyboard.Key.caps_lock)
        elif capsLockReleaseCount % 2 == 0:
            # keyboardControllerObj.release(keyboard.Key.ctrl_l)
            keyboardControllerObj.release(keyboard.Key.f13)



    if key in comboList:
        #remove key from currentPressedKeys
        currentPressedKeys[:] = [x for x in currentPressedKeys if x != key]

    if len(currentPressedKeys) == 0:
        comboReleased = True


comboList = [keyboard.Key.caps_lock, keyboard.KeyCode(char="w")]
currentPressedKeys = []
capsLockReleaseCount = 0
comboReleased = True
keyboardControllerObj = keyboard.Controller()


if win32api.GetKeyState(win32con.VK_CAPITAL) == 1:
    creedFunctions.pynputPressRel(keyboardControllerObj, keyboard.Key.caps_lock)


with keyboard.Listener(on_press=functionOnPress, on_release=functionOnRelease) as listenerObj:
    listenerObj.join()







