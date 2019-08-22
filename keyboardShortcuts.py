from pynput import keyboard
import win32api, win32con, pyautogui
import tkinter


def functionComboDetected():
    global labelText
    # labelText = labelText + " Combo detected"

    print("Combo detected")


def functionOnPress(key):
    global comboReleased

    # print("Key was pressed: " + str(key))

    if key in comboList:
        # print(str(key) + " is one of the combo keys")
        # currentSet.add(key)
        currentList.append(key)
        # print("currentSet is " + str(currentList))

    if list(dict.fromkeys(currentList)) == comboList and comboReleased:
        comboReleased = False
        functionComboDetected()


def functionOnRelease(key):
    # print("Key was released: " + str(key))
    global capsLockReleaseCount
    global comboReleased

    if key == keyboard.Key.caps_lock:

        if capsLockReleaseCount % 2 == 0:
            pyautogui.press("capslock")

        print("capsLockReleaseCount = " + str(capsLockReleaseCount))
        capsLockReleaseCount = capsLockReleaseCount + 1


    if key in comboList:
        # print(str(key) + " is one of the combo keys")
        currentList[:] = [x for x in currentList if x != key]
        # currentList.pop()
        print("currentSet is " + str(currentList))

    if len(currentList) == 0:
        comboReleased = True
        print("currentList is empty")


# comboList = [keyboard.Key.caps_lock, keyboard.KeyCode(char="s")]
comboList = [keyboard.Key.ctrl_l, keyboard.KeyCode(char="s")]
# currentSet = set()
currentList = []
capsLockReleaseCount = 0
comboReleased = True
labelText = "Opening..."


if win32api.GetKeyState(win32con.VK_CAPITAL) == 1:
    pyautogui.press("capslock")

windowObj = tkinter.Tk()
windowObj.title("Welcome!")
labelObj = tkinter.Label(windowObj, text=labelText)
labelObj.pack()
windowObj.mainloop()


with keyboard.Listener(on_press=functionOnPress, on_release=functionOnRelease) as listenerObj:
    listenerObj.join()



