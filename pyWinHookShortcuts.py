import pyWinhook, pythoncom, pyautogui


# import win32gui, win32process, psutil


def functionComboDetected(outputCombo, **otherArg):

    for outKey in outputCombo:
        keyDownInfoObj.autoKeyDown.append(outKey)

        if outKey == "Lmenu":
            pyautogui.keyDown("alt")
        else:
            pyautogui.keyDown(outKey.lower())


    for outKey in reversed(outputCombo):
        if outKey == "Lmenu":
            pyautogui.keyUp("alt")
        else:
            pyautogui.keyUp(outKey.lower())

    time.sleep(2)

    if otherArg:
        for char in otherArg["outputString"]:
            pyautogui.press(char)



    print("Key pressed down automatically: " + event.Key)
    print("Key pressed down automatically: " + event.Key)
    print("Allowed to send automatic press to OS? " + str(True))
    return True


def functionKeyPress(event):

    print("press")


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

        if event.Key in combo["inputKeys"] and event.Key not in currentPressedKeys:
            currentPressedKeys.append(event.Key)


        if list(dict.fromkeys(currentPressedKeys)) == combo["inputKeys"]:
            if "outputComboKeys" in combo.keys():
                if "outputString" in combo.keys():
                    functionComboDetected(combo["outputComboKeys"], outputString=combo["outputString"])
                else:
                    functionComboDetected(combo["outputComboKeys"])

        if "Capital" in currentPressedKeys:
            toReturn = False


    print("Key pressed: " + event.Key)
    print("Allowed to send press to OS? " + str(toReturn))

    return toReturn



def functionKeyRelease(event):

    print("release")

    toReturn = True

    if event.Key == "Capital":
        toReturn = False


    for combo in comboList:

        if event.Key in combo["inputKeys"] and event.Key in currentPressedKeys:

            #remove that key from currentPressedKeys
            currentPressedKeys.remove(event.Key)
            # currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]






    if event.Key in keyDownInfoObj.autoKeyDown:
        keyDownInfoObj.autoKeyDown.remove(event.Key)
        # keyDownInfoObj.autoKeyDown[:] = [x for x in keyDownInfoObj.autoKeyDown if x != event.Key]
    elif "Capital" in currentPressedKeys:
        toReturn = False



    # print(str(currentPressedKeys))
    print("Key released: " + event.Key)
    print("Allowed to send release to OS? " + str(toReturn))
    return toReturn




def OnKeyboardEvent(event):


    if event.MessageName in ["key sys down", "key down"]:

        if event.Key in keyDownInfoObj.autoKeyDown:
            # print("event.Key: " + event.Key)
            # print("keyDownInfoObj.autoKeyDown: " + str(keyDownInfoObj.autoKeyDown))
            return functionAutoKeyPress(event)
        else:
            return functionKeyPress(event)

    elif event.MessageName in ["key up", "key sys up"]:
        return functionKeyRelease(event)

    # else:
    #
    #
    #     print('MessageName: %s' % event.MessageName)
    #     # print("Key pressed down: " + event.Key)	    print('Message: %s' % event.Message)
    #     # print("Allowed to send press to OS? " + str(toReturn))	    print('Time: %s' % event.Time)
    #     print('Window: %s' % event.Window)
    #     print('WindowName: %s' % event.WindowName)
    #     print('Ascii: %s' % event.Ascii, chr(event.Ascii))
    #     print('Key: %s' % event.Key)
    #     print('KeyID: %s' % event.KeyID)
    #     print('ScanCode: %s' % event.ScanCode)
    #     print('Extended: %s' % event.Extended)
    #     print('Injected: %s' % event.Injected)
    #     print('Alt %s' % event.Alt)
    #     print('Transition %s' % event.Transition)
    #     print('---')
    #
    #     return True
#

#





class keyDownInfo():
    def __init__(self, autoKeyDown):
        self.autoKeyDown = autoKeyDown




keyDownInfoObj = keyDownInfo([])


comboList = [
                {"inputKeys": ["Capital", "J"], "outputComboKeys": ["Left"]},
                {"inputKeys": ["Capital", "K"], "outputComboKeys": ["Right"]},
                {"inputKeys": ["Capital", "U"], "outputComboKeys": ["Up"]},
                {"inputKeys": ["Capital", "M"], "outputComboKeys": ["Down"]},
                {"inputKeys": ["Capital", "A"], "outputComboKeys": ["Lmenu", "Space"], "outputString": "C:\\Users\\creed"}
            ]




currentPressedKeys = []
pyautogui.PAUSE = 0

hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
print("ready")
pythoncom.PumpMessages()








# def functionOtherComboDetected(outputKeys):
#
#
#     # windowsExplorerApp = pywinauto.Application(backend="uia").connect(path="explorer.exe")
#     # systemTrayObj = windowsExplorerApp.window(class_name="Shell_TrayWnd")
#     # systemTrayObj.child_window(title="Executor").click()
#
#     # windowsExplorerApp = pywinauto.Application(backend="uia").connect(path="explorer.exe")
#     print(1)
#
#
#     # for outKey in outputKeys:
#     #     pyautogui.press(outKey.lower())

