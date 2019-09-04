import pyWinhook, pythoncom, pyautogui, win32gui, time



def functionComboDetected(outputCombo, **otherArg):

    if otherArg:

        executorDisplayed = False

        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":
            executorDisplayed = True


    for num, outKey in enumerate(outputCombo):
        # print(num)
        # print(outKey
        keyDownInfoObj.autoKeyDown.append(outKey)
        pyautogui.keyDown(convCharMap(outputCombo, "pyHook", "pyAutoGui")[num])


    for num, outKey in enumerate(reversed(outputCombo)):
        # print(num)
        # print(outKey)
        pyautogui.keyUp(convCharMap(outputCombo, "pyHook", "pyAutoGui")[num])


    if otherArg:

        if not executorDisplayed:

            for i in range(1, 20):

                if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":

                    print("Executor is now displayed and outputString is " + str(otherArg["outputString"]))

                    time.sleep(.01)

                    for item in otherArg["outputString"]:

                        for outKey in item["pyHook"]:
                            # print(outKey)
                            keyDownInfoObj.autoKeyDown.append(outKey)

                        for outKey in item["pyAutoGui"]:
                            # print(outKey)
                            pyautogui.keyDown(outKey)

                        for outKey in reversed(item["pyAutoGui"]):
                            # print(outKey)
                            pyautogui.keyUp(outKey)


                    # keyDownInfoObj.autoKeyDown.append("9")
                    # pyautogui.press("9")
                    # keyDownInfoObj.autoKeyDown.append("back")
                    # pyautogui.press("backspace")


                    break

                print(i)
                time.sleep(.005)





def functionAutoKeyPress(event):

    print("Key pressed down automatically: " + event.Key.lower() + " and it was sent to the OS.")
    return True



def functionKeyPress(event):

    toReturn = True

    if event.Key == "Tab":
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":
            print("tabbed")
            # pyautogui.press("right")
            # toReturn = False


    if not keyDownInfoObj.autoKeyDown:

        for combo in comboList:

            if event.Key.lower() in combo["inputKeys"]:  # and event.Key.lower() not in currentPressedKeys:
                currentPressedKeys.add(event.Key.lower())



        for combo in comboList:

            if currentPressedKeys == combo["inputKeys"]:

                # print("A combo was detected")

                if "outputComboKeys" in combo.keys():
                    if "outputString" in combo.keys():
                        functionComboDetected(combo["outputComboKeys"], outputString=combo["outputString"])
                    else:
                        functionComboDetected(combo["outputComboKeys"])
                elif "printToScreen" in combo.keys():
                    print(combo["printToScreen"])


    if event.Key.lower() not in keyDownInfoObj.autoKeyDown and "capital" in currentPressedKeys:
            toReturn = False


    if toReturn:
        print("Key pressed: " + event.Key.lower() + " and it was sent to the OS.")
    else:
        print("Key pressed: " + event.Key.lower() + " and it was not sent to the OS.")


    return toReturn



def functionKeyRelease(event):

    toReturn = True


    if event.Key.lower() not in keyDownInfoObj.autoKeyDown and event.Key.lower() in currentPressedKeys:

        currentPressedKeys.remove(event.Key.lower())
        toReturn = False



    elif event.Key.lower() in keyDownInfoObj.autoKeyDown:
        keyDownInfoObj.autoKeyDown.remove(event.Key.lower())


    # print(str(currentPressedKeys))

    if toReturn:
        print("Key released: " + event.Key.lower() + " and it was sent to the OS.")
    else:
        print("Key released: " + event.Key.lower() + " and it was not sent to the OS.")


    # if event.Key.lower() == "capital" and not currentPressedKeys:
    #     print("here")
    #     keyDownInfoObj.autoKeyDown.append("back")
        # pyautogui.keyDown("backspace")
        # pyautogui.keyUp("backspace")




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



def convCharMap(action, fromFormat, toFormat):

    for item in characterMap:
        if fromFormat in item and item[fromFormat] == action:
            return item[toFormat]

    return action


def addKeyValue(dict, keyVal, val):

    dict[keyVal] = val
    return dict


def createNewDict(action, fromFormat, yesAsEntered):

    newDict = {}
    if yesAsEntered:
        addKeyValue(newDict, "asEntered", action)


    convertedToAutoGui = convCharMap(action, fromFormat, "pyAutoGui")
    convertedToHook = convCharMap(action, fromFormat, "pyHook")

    if not isinstance(convertedToAutoGui, list):
        convertedToAutoGui = [convertedToAutoGui]

    if not isinstance(convertedToHook, list):
        convertedToHook = [convertedToHook]

    addKeyValue(newDict, "pyAutoGui", convertedToAutoGui)
    addKeyValue(newDict, "pyHook", convertedToHook)

    return newDict






def createPathList(path):

    pathList = []

    for char in path:
        pathList.append(createNewDict(char.lower(), "asEntered", True))



    if pathList[-1]["asEntered"] !=  "\\":
        pathList.append(createNewDict("\\", "pyAutoGui", False))



    # pathList.append(createNewDict("9", "pyAutoGui", False))
    # pathList.append(createNewDict("back", "pyHook", False))

    for i in range(1, 2):
        pathList.insert(0, createNewDict("back", "pyHook", False))
    pathList.insert(0, createNewDict(["lcontrol", "a"], "pyHook", False))

    print(str(pathList).replace("'", "\""))



    return pathList






class keyDownInfo():
    def __init__(self, autoKeyDown):
        self.autoKeyDown = autoKeyDown




#
# pyHookToAutoGui = [
#     ["lmenu", "alt"],
#     ["lshift", "shift"],
#     ["lcontrol", "ctrl"]
# ]
#



characterMap = [
    {"pyHook": "space", "pyAutoGui": "space", "asEntered": " "},
    {"pyHook": "oem_5", "pyAutoGui": "\\", "asEntered": "\\"},
    {"pyHook": "back", "pyAutoGui": "backspace"},
    {"pyHook": ["lcontrol", "a"], "pyAutoGui": ["ctrl", "a"]},
    {"pyHook": ["lshift", "oem_1", "lshift"], "pyAutoGui": ":", "asEntered": ":"},
    {"pyHook": ["lshift", "oem_minus", "lshift"], "pyAutoGui": "_", "asEntered": "_"},
    {"pyHook": ["lmenu", "space"], "pyAutoGui": ["alt", "space"]}
]



comboList = [
                {"inputKeys": {"capital", "j"}, "outputComboKeys": ["left"]},
                {"inputKeys": {"capital", "k"}, "outputComboKeys": ["right"]},
                {"inputKeys": {"capital", "u"}, "outputComboKeys": ["up"]},
                {"inputKeys": {"capital", "m"}, "outputComboKeys": ["down"]},
                # {"inputKeys": {"capital", "d"}, "outputComboKeys": ["lmenu", "space"], "outputString": createPathList(r"C:\Users\cnaylor\Desktop")},
                # {"inputKeys": {"capital", "a"}, "outputComboKeys": ["lmenu", "space"], "outputString": createPathList(r"Y:\Accounting")},
                # {"inputKeys": {"capital", "c"}, "outputComboKeys": ["lmenu", "space"], "outputString": createPathList(r"Y:\Accounting\12_Creed")},
                {"inputKeys": {"capital", "a"}, "outputComboKeys": ["lmenu", "space"], "outputString": createPathList(r"C:\users\creed")},
                {"inputKeys": {"capital", "s"}, "outputComboKeys": ["lmenu", "space"], "outputString": createPathList(r"c:\users\creed\nas\synologydrive\computer\setup files")},
                {"inputKeys": {"capital", "h"}, "printToScreen": "hi"}
            ]



keyDownInfoObj = keyDownInfo([])
currentPressedKeys = set()
pyautogui.PAUSE = 0



hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
print("ready")


# for key in ["alt", "space"]:
#     pyautogui.keyDown(key)
#
# for key in reversed["alt", "space"]:
#     pyautogui.keyUp(key)


pythoncom.PumpMessages()




#
# Key pressed: lshift and it was sent to the OS.
# Key pressed: oem_minus and it was sent to the OS.
# Key released: lshift and it was sent to the OS.
# Key pressed: lshift and it was sent to the OS.
# Key released: oem_minus and it was sent to the OS.
# Key released: lshift and it was sent to the OS.
#



#
# Key pressed: lshift and it was sent to the OS.
# Key pressed: oem_1 and it was sent to the OS.
# Key released: lshift and it was sent to the OS.
# Key pressed: lshift and it was sent to the OS.
# Key released: oem_1 and it was sent to the OS.
# Key released: lshift and it was sent to the OS.




# win32guiObj = win32gui
#     win32guiObj.GetWindowText(win32guiObj.GetForegroundWindow())
#     processID = win32process.GetWindowThreadProcessId(win32guiObj.GetForegroundWindow())
#     # print(psutil.Process(processID[-1]))
#
#     if psutil.Process(processID[-1]).name() == "Executor.exe":
#         keyDownInfoObj.notAllowedToRelease = "Tab"
#         pyautogui.press("right")
#         toReturn = False


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

