from pynput import keyboard
import win32api, win32con, pyautogui



def functionComboDetected():
    print("Combo detected")


def functionOnPress(key):
    # print("Key was pressed: " + str(key))

    if key in comboList:
        # print(str(key) + " is one of the combo keys")
        # currentSet.add(key)
        currentList.append(key)
        print("currentSet is " + str(currentList))

    if currentList == comboList:
        functionComboDetected()


def functionOnRelease(key):
    # print("Key was released: " + str(key))
    global capsLockReleaseCount

    if key in comboList:
        # print(str(key) + " is one of the combo keys")
        currentList.pop()
        print("currentSet is " + str(currentList))


    if key == keyboard.Key.caps_lock:

        if capsLockReleaseCount % 2 == 0:
            pyautogui.press("capslock")

        print("capsLockReleaseCount = " + str(capsLockReleaseCount))
        capsLockReleaseCount = capsLockReleaseCount + 1






comboList = [keyboard.Key.caps_lock, keyboard.KeyCode(char="s")]
# currentSet = set()
currentList = []
capsLockReleaseCount = 0


if win32api.GetKeyState(win32con.VK_CAPITAL) == 1:
    pyautogui.press("capslock")





with keyboard.Listener(on_press=functionOnPress, on_release=functionOnRelease) as listenerObj:
    listenerObj.join()




