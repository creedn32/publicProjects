import pyWinhook, pythoncom, pyautogui, win32gui
import time

import sys
sys.path.append("..")
from creed_modules import creedFunctions


# import win32gui, win32process, psutil


def functionComboDetected(outputCombo, **otherArg):

    # print(keyDownInfoObj.autoKeyDown)

    if not keyDownInfoObj.autoKeyDown:

        fillForm = False

        if otherArg:
            if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != "Executor":
                fillForm = True


        for outKey in outputCombo:
            keyDownInfoObj.autoKeyDown.append(outKey)

            if outKey == "lmenu":
                pyautogui.keyDown("alt")
            else:
                pyautogui.keyDown(outKey.lower())


        for outKey in reversed(outputCombo):
            pyautogui.keyUp(creedFunctions.convertKey(outKey.lower()))

        if fillForm:
            time.sleep(.05)
            for char in otherArg["outputString"]:
                print(creedFunctions.convertKey(char))
                keyDownInfoObj.autoKeyDown.append(char)
                pyautogui.hotkey(creedFunctions.convertKey(char))
                # pyautogui.press(char)


        # if otherArg and otherArg["fillForm"]:
        #

        #     for char in otherArg["outputString"]:
        #         pyautogui.press(char)
        #





def functionAutoKeyPress(event):


    # print("Key pressed down automatically: " + event.Key.lower())
    # print("Allowed to send automatic press to OS? " + str(True))
    return True


def functionKeyPress(event):

    print(str(event.Key))

    toReturn = True

    # if event.Key == "Tab":
    #     win32guiObj = win32gui
    #     win32guiObj.GetWindowText(win32guiObj.GetForegroundWindow())
    #     processID = win32process.GetWindowThreadProcessId(win32guiObj.GetForegroundWindow())
    #     # print(psutil.Process(processID[-1]))
    #
    #     if psutil.Process(processID[-1]).name() == "Executor.exe":
    #         keyDownInfoObj.notAllowedToRelease = "Tab"
    #         pyautogui.press("right")
    #         toReturn = False



    for combo in comboList:

        if event.Key.lower() in combo["inputKeys"] and event.Key.lower() not in currentPressedKeys:
            currentPressedKeys.append(event.Key.lower())


        if currentPressedKeys == combo["inputKeys"]:
            if "outputComboKeys" in combo.keys():
                if "outputString" in combo.keys():
                    functionComboDetected(combo["outputComboKeys"], outputString=combo["outputString"])
                else:
                    functionComboDetected(combo["outputComboKeys"])
            elif "printToScreen" in combo.keys():
                print(combo["printToScreen"])

        if event.Key.lower() not in keyDownInfoObj.autoKeyDown and "capital" in currentPressedKeys:
            toReturn = False


    # print("Key pressed: " + event.Key.lower())
    # print("Allowed to send press to OS? " + str(toReturn))

    return toReturn



def functionKeyRelease(event):

    # print("release")

    toReturn = True


    #
    # if event.Key == "Capital":
    #     toReturn = False


    for combo in comboList:

        if event.Key.lower() in combo["inputKeys"] and event.Key.lower() in currentPressedKeys:

            #
            #remove that key from currentPressedKeys
            currentPressedKeys.remove(event.Key.lower())
            toReturn = False
            # currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]

    # if event.Key == "D":
    #     print(toReturn)
    #
    # print("keydown is " + str(keyDownInfoObj.autoKeyDown))
    # print("event.key is " + str(event.Key))

    if event.Key.lower() in keyDownInfoObj.autoKeyDown:
        # if event.Key == "D":
        #     print("here: " + str(toReturn))
        keyDownInfoObj.autoKeyDown.remove(event.Key.lower())
        # keyDownInfoObj.autoKeyDown[:] = [x for x in keyDownInfoObj.autoKeyDown if x != event.Key]
    elif "capital" in currentPressedKeys:
        toReturn = False

        if event.Key.lower() == "d":
            print("here " + str(toReturn))



    # print(str(currentPressedKeys))
    # print("Key released: " + event.Key.lower())
    # print("Allowed to send release to OS? " + str(toReturn))
    return toReturn




def OnKeyboardEvent(event):


    if event.MessageName in ["key sys down", "key down"]:

        if event.Key.lower() in keyDownInfoObj.autoKeyDown:
            # print("event.Key: " + event.Key)
            # print("keyDownInfoObj.autoKeyDown: " + str(keyDownInfoObj.autoKeyDown))
            return functionAutoKeyPress(event)
        else:
            return functionKeyPress(event)

    elif event.MessageName in ["key up", "key sys up"]:
        return functionKeyRelease(event)



class keyDownInfo():
    def __init__(self, autoKeyDown):
        self.autoKeyDown = autoKeyDown




keyDownInfoObj = keyDownInfo([])


comboList = [
                {"inputKeys": ["capital", "j"], "outputComboKeys": ["left"]},
                {"inputKeys": ["capital", "k"], "outputComboKeys": ["right"]},
                {"inputKeys": ["capital", "u"], "outputComboKeys": ["up"]},
                {"inputKeys": ["capital", "m"], "outputComboKeys": ["down"]},
                {"inputKeys": ["capital", "a"], "outputComboKeys": ["lmenu", "space"], "outputString": ["c", "oem_1", "oem_5", "u", "s", "e", "r", "s", "oem_5", "c", "r", "e", "e", "d"]},
                {"inputKeys": ["capital", "s"], "printToScreen": "hi"}
            ]



currentPressedKeys = []
pyautogui.PAUSE = 0


# pathList = []
#
# for char in "c:\\users\\creed":
#     pathList.append(char)
#
# print(pathList)



hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
print("ready")
pythoncom.PumpMessages()








# def functionOtherComboDetected(outputKeys):
#
#
#k     # windowsExplorerApp = pywinauto.Application(backend="uia").connect(path="explorer.exe")
#     # systemTrayObj = windowsExplorerApp.window(class_name="Shell_TrayWnd")
#     # systemTrayObj.child_window(title="Executor").click()
#
#     # windowsExplorerApp = pywinauto.Application(backend="uia").connect(path="explorer.exe")
#     print(1)
#
#
#     # for outKey in outputKeys:
#     #     pyautogui.press(outKey.lower())

