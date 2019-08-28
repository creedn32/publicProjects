import pyWinhook, pythoncom, pyautogui
# import win32gui, win32process, psutil


def functionComboDetected(outputCombo):

    for outKey in outputCombo:
        keyDownInfoObj.autoKeyDown.append(outKey)
        pyautogui.keyDown(outKey.lower())


    for outKey in reversed(outputCombo):
        pyautogui.keyUp(outKey.lower())



def functionAutoKeyPress(event):
    # print("Key pressed down automatically: " + event.Key)
    # print(str(currentPressedKeys))
    return True


def functionKeyPress(event):

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
            functionComboDetected(combo["outputComboKeys"])


        if combo["inputKeys"][0] in currentPressedKeys:
            toReturn = False


    return toReturn



def functionKeyRelease(event):

    toReturn = True


    for combo in comboList:

        if event.Key in combo["inputKeys"]:

            #remove that key from currentPressedKeys
            currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]


    if "Capital" in currentPressedKeys:
        toReturn = False


    if event.Key in keyDownInfoObj.autoKeyDown:
        keyDownInfoObj.autoKeyDown[:] = [x for x in keyDownInfoObj.autoKeyDown if x != event.Key]



    # print(str(currentPressedKeys))
    # print("Key released: " + event.Key)
    # print("Allowed to send release to OS? " + str(toReturn))
    return toReturn




def OnKeyboardEvent(event):

    if event.MessageName == "key down" and event.Key in keyDownInfoObj.autoKeyDown:
        print("event.Key: " + event.Key)
        print("keyDownInfoObj.autoKeyDown: " + str(keyDownInfoObj.autoKeyDown))
        return functionAutoKeyPress(event)
    elif event.MessageName == "key down":
        return functionKeyPress(event)
    elif event.MessageName == "key up":
        return functionKeyRelease(event)
    else:
        return True








class keyDownInfo():
    def __init__(self, autoKeyDown):
        self.autoKeyDown = autoKeyDown




keyDownInfoObj = keyDownInfo([])


comboList = [
                {"inputKeys": ["Capital", "J"], "outputComboKeys": ["Left"]},
                {"inputKeys": ["Capital", "K"], "outputComboKeys": ["Right"]},
                {"inputKeys": ["Capital", "U"], "outputComboKeys": ["Up"]},
                {"inputKeys": ["Capital", "M"], "outputComboKeys": ["Down"]}
                # {"inputKeys": ["Capital", "A"], "outputComboKeys": ["Alt", "Space"], "outputKeys": ["A", "D"]}
            ]


currentPressedKeys = []
pyautogui.PAUSE = 0

hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
pythoncom.PumpMessages()







