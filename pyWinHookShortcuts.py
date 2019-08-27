import pyWinhook, pythoncom, pyautogui
# import win32gui, win32process, psutil


def functionComboDetected(outputCombo):
    # print("Combo detected")

    for outKey in outputCombo:
        keyDownInfoObj.autoKeyDown.append(outKey)
        # keyDownInfoObj.autoKeyDown.append(outKey)
        # print(1)
        # print(keyDownInfoObj.autoKeyDown)
        pyautogui.keyDown(outKey.lower())


    for outKey in reversed(outputCombo):
        pyautogui.keyUp(outKey.lower())


    # for outKey in output:
    #     keyDownInfoObj.autoKeyDown.append(outKey)
    #     pyautogui.press(outKey)




def functionAutoKeyPress(event):
    # print("Key pressed down automatically: " + event.Key)
    # print(str(currentPressedKeys))
    return True


def functionKeyPress(event):

    # print(comboList)
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


    # print('MessageName: %s' % event.MessageName)
    # print('Message: %s' % event.Message)
    # print('Time: %s' % event.Time)
    # print('Window: %s' % event.Window)
    # print('WindowName: %s' % event.WindowName)
    # print('Ascii: %s' % event.Ascii, chr(event.Ascii))
    # print('Key: %s' % event.Key)
    # print('KeyID: %s' % event.KeyID)
    # print('ScanCode: %s' % event.ScanCode)
    # print('Extended: %s' % event.Extended)
    # print('Injected: %s' % event.Injected)
    # print('Alt %s' % event.Alt)
    # print('Transition %s' % event.Transition)
    # print('---')

    # print(str(currentPressedKeys))
    # print("Key pressed down: " + event.Key)
    # print("Allowed to send press to OS? " + str(toReturn))

    return toReturn



def functionKeyRelease(event):

    toReturn = True

    # if event.Key == keyDownInfoObj.notAllowedToRelease:
    #     toReturn = False
    #     keyDownInfoObj.notAllowedToRelease = None



    for combo in comboList:

        if event.Key in combo["inputKeys"]:

            # if list(dict.fromkeys(currentPressedKeys)) == combo["inputKeys"] and combo["waitUntilRelease"]:
            #     functionComboDetected(combo["outputKeys"], combo["waitUntilRelease"])

            #remove that key from currentPressedKeys
            currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]


    if "Capital" in currentPressedKeys:
        toReturn = False


    if event.Key in keyDownInfoObj.autoKeyDown:
        keyDownInfoObj.autoKeyDown[:] = [x for x in keyDownInfoObj.autoKeyDown if x != event.Key]

        # keyDownInfoObj.autoKeyDown = [x for x in keyDownInfoObj.autoKeyDown if x != event.Key]


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
    def __init__(self, autoKeyDown, notAllowedToRelease):
        self.autoKeyDown = autoKeyDown
        self.notAllowedToRelease = notAllowedToRelease




keyDownInfoObj = keyDownInfo([], None)


comboList = [
                {"inputKeys": ["Capital", "J"], "outputComboKeys": ["Left"]},
                {"inputKeys": ["Capital", "K"], "outputComboKeys": ["Right"]},
                {"inputKeys": ["Capital", "U"], "outputComboKeys": ["Up"]},
                {"inputKeys": ["Capital", "M"], "outputComboKeys": ["Down"]},
                {"inputKeys": ["Capital", "A"], "outputComboKeys": ["Alt", "Space"], "outputKeys": ["A", "D"]}
            ]


currentPressedKeys = []
pyautogui.PAUSE = 0

hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
pythoncom.PumpMessages()











# if len(currentPressedKeys) == 0:
        #     pass

           # print("Key released automaticaly: " + event.Key)

        # else:
        #     pass
            # print("Key released: " + event.Key)

        # print(str(currentPressedKeys))

# print('MessageName: %s' % event.MessageName)
# print('Message: %s' % event.Message)
# print('Time: %s' % event.Time)
# print('Window: %s' % event.Window)
# print('WindowName: %s' % event.WindowName)
# print('Ascii: %s' % event.Ascii, chr(event.Ascii))
# print('Key: %s' % event.Key)
# print('KeyID: %s' % event.KeyID)
# print('ScanCode: %s' % event.ScanCode)
# print('Extended: %s' % event.Extended)
# print('Injected: %s' % event.Injected)
# print('Alt %s' % event.Alt)
# print('Transition %s' % event.Transition)
# print('---')


# return True to pass the event to other handlers
# return False to stop the event from propagating