import pyWinhook, pythoncom, pyautogui
import win32gui, win32process, psutil


def functionComboDetected(output):
    print("Combo detected")

    for outKey in output:
        keyDownInfoObj.autoKeyDown = outKey #output[0].upper() + output[1:]
        pyautogui.press(outKey.lower())


def functionAutoKeyPress(event):
    print("Key pressed down automatically: " + event.Key)
    # print(str(currentPressedKeys))
    return 1


def functionKeyPress(event):

    # print(comboList)
    toReturn = 1

    if event.Key == "Tab":
        win32guiObj = win32gui
        win32guiObj.GetWindowText(win32guiObj.GetForegroundWindow())
        processID = win32process.GetWindowThreadProcessId(win32guiObj.GetForegroundWindow())
        # print(psutil.Process(processID[-1]))

        if psutil.Process(processID[-1]).name() == "Executor.exe":
            keyDownInfoObj.notAllowedToRelease = "Tab"
            pyautogui.press("right")
            toReturn = 0



    for combo in comboList:

        if event.Key in combo["inputKeys"] and event.Key not in currentPressedKeys:
            currentPressedKeys.append(event.Key)


        if list(dict.fromkeys(currentPressedKeys)) == combo["inputKeys"]:
            functionComboDetected(combo["outputKeys"])


        if combo["inputKeys"][0] in currentPressedKeys:
            toReturn = 0

    print('MessageName: %s' % event.MessageName)
    print('Message: %s' % event.Message)
    print('Time: %s' % event.Time)
    print('Window: %s' % event.Window)
    print('WindowName: %s' % event.WindowName)
    print('Ascii: %s' % event.Ascii, chr(event.Ascii))
    print('Key: %s' % event.Key)
    print('KeyID: %s' % event.KeyID)
    print('ScanCode: %s' % event.ScanCode)
    print('Extended: %s' % event.Extended)
    print('Injected: %s' % event.Injected)
    print('Alt %s' % event.Alt)
    print('Transition %s' % event.Transition)
    print('---')

    print(str(currentPressedKeys))
    print("Key pressed down: " + event.Key)
    print("Allowed to send press to OS? " + str(toReturn))
    return toReturn



def functionKeyRelease(event):

    toReturn = 0

    if event.Key == keyDownInfoObj.notAllowedToRelease:
        toReturn = 0
        keyDownInfoObj.notAllowedToRelease = None


    for combo in comboList:

        if event.Key in combo["inputKeys"]:

            #remove that key from currentPressedKeys
            currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]

        if combo["inputKeys"][0] in currentPressedKeys:
            toReturn = 0


    if event.Key == keyDownInfoObj.autoKeyDown:
        keyDownInfoObj.autoKeyDown = None


    print(str(currentPressedKeys))
    print("Key released: " + event.Key)
    print("Allowed to send release to OS? " + str(toReturn))
    return toReturn




def OnKeyboardEvent(event):

    if event.MessageName == "key down" and keyDownInfoObj.autoKeyDown != None:
        return functionAutoKeyPress(event)
    elif event.MessageName == "key down":
        return functionKeyPress(event)
    elif event.MessageName == "key up":
        return functionKeyRelease(event)
    else:
        return 1








class keyDownInfo():
    def __init__(self, autoKeyDown, notAllowedToRelease):
        self.autoKeyDown = autoKeyDown
        self.notAllowedToRelease = notAllowedToRelease




keyDownInfoObj = keyDownInfo(None, None)
comboList = [
                {"inputKeys": ["Capital", "J"], "outputKeys": ["Left"]},
                {"inputKeys": ["F13", "J"], "outputKeys": ["Left"]},
                {"inputKeys": ["Capital", "K"], "outputKeys": ["Right"]},
                {"inputKeys": ["F13", "K"], "outputKeys": ["Right"]},
                {"inputKeys": ["Capital", "U"], "outputKeys": ["Up"]},
                {"inputKeys": ["F13", "U"], "outputKeys": ["Up"]},
                {"inputKeys": ["Capital", "M"], "outputKeys": ["Down"]},
                {"inputKeys": ["F13", "M"], "outputKeys": ["Down"]},
                {"inputKeys": ["F13", "A"], "outputKeys": ["Down"]}
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