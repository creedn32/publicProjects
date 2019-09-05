import pyWinhook, pythoncom, pyautogui, win32gui, time, pywinauto, psutil


import sys
sys.path.append("..")
from creed_modules import creedFunctions



def functionComboDetected(outputCombo):

    convertedOutputCombo = convCharMap(outputCombo, "pyHook", "pyAutoGui")
    # print(convertedOutputCombo)

    # print(outputCombo)
    # for outKey in outputCombo:
    #     print(outKey)



    for num, outKey in enumerate(outputCombo):
        # print(num)
        # print("outKey is " + outKey)
        # print(convCharMap(outputCombo, "pyHook", "pyAutoGui"))

        if convertedOutputCombo[num] == "shift" and num < len(convertedOutputCombo):
            appInfoObj.afterShift = convertedOutputCombo[num + 1:][0]


        appInfoObj.autoKeyDown.append(outKey)
        # print("outKey is " + outKey)
        pyautogui.keyDown(convertedOutputCombo[num])


    for num, outKey in enumerate(reversed(outputCombo)):
        # print(num)
        # print(outKey)
        pyautogui.keyUp(convertedOutputCombo[num])


def functionAdvComboDetected(outputString):

    if not win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":

        executorCombo = ["lmenu", "space"]

        convertedExecutorCombo = convCharMap(executorCombo, "pyHook", "pyAutoGui")

        for num, outKey in enumerate(executorCombo):
            appInfoObj.autoKeyDown.append(outKey)
            pyautogui.keyDown(convertedExecutorCombo[num])

        for num, outKey in enumerate(reversed(executorCombo)):
            pyautogui.keyUp(convertedExecutorCombo[num])


        for i in range(1, 20):

            if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":

                # print("Executor is now displayed and outputString is " + str(outputString))
                time.sleep(.01)

                for item in outputString:

                    for outKey in item["pyHook"]:
                        # print(outKey)
                        appInfoObj.autoKeyDown.append(outKey)

                    for outKey in item["pyAutoGui"]:
                        # print(outKey)
                        pyautogui.keyDown(outKey)

                    for outKey in reversed(item["pyAutoGui"]):
                        # print(outKey)
                        pyautogui.keyUp(outKey)


                break

            # print(i)
            time.sleep(.005)


    else:

        tmainformObj.wait('ready')
        teditObj = tmainformObj[u'3']
        currentText = teditObj.texts()
        print(currentText[0])


        executorCombo = ["lmenu", "space"]

        for num, outKey in enumerate(executorCombo):
            appInfoObj.autoKeyDown.append(outKey)
            pyautogui.keyDown(convCharMap(executorCombo, "pyHook", "pyAutoGui")[num])

        for num, outKey in enumerate(reversed(executorCombo)):
            pyautogui.keyUp(convCharMap(executorCombo, "pyHook", "pyAutoGui")[num])



def functionAutoKeyPress(event):

    if appInfoObj.printKeyActions:
        print("Key pressed down automatically: " + event.Key.lower() + " and it was sent to the OS.")
    return True



def functionKeyPress(event):

    toReturn = True

    if event.Key == "Tab":
        if win32gui.GetWindowText(win32gui.GetForegroundWindow()) == "Executor":
            print("tabbed")
            # pyautogui.press("right")
            # toReturn = False


    if not appInfoObj.autoKeyDown:

        for combo in comboList:

            if event.Key.lower() in combo["inputKeys"]:  # and event.Key.lower() not in currentPressedKeys:
                currentPressedKeys.add(event.Key.lower())



        for combo in comboList:

            if currentPressedKeys == combo["inputKeys"]:

                # print("A combo was detected")

                if "outputComboKeys" in combo.keys():
                    functionComboDetected(combo["outputComboKeys"])
                elif "outputString" in combo.keys():
                    functionAdvComboDetected(combo["outputString"])
                elif "printToScreen" in combo.keys():
                    print(combo["printToScreen"])


    if event.Key.lower() not in appInfoObj.autoKeyDown and "capital" in currentPressedKeys: # and event.Key.lower() != "lshift":
        toReturn = False


    if appInfoObj.printKeyActions:
        if toReturn:
            print("Key pressed: " + event.Key.lower() + " and it was sent to the OS.")
        else:
            print("Key pressed: " + event.Key.lower() + " and it was not sent to the OS.")


    return toReturn



def functionKeyRelease(event):

    toReturn = True

    # if event.Key.lower() == "lshift":
    #     print(convCharMap(event.Key.lower(), "pyHook", "pyAutoGui"))

    if event.Key.lower() == "lshift" and appInfoObj.afterShift:
        # print(1)
        toReturn = False
    elif event.Key.lower() in appInfoObj.autoKeyDown and not appInfoObj.afterShift:
        # print(2)
        appInfoObj.autoKeyDown.remove(event.Key.lower())
    elif event.Key.lower() not in appInfoObj.autoKeyDown and event.Key.lower() in currentPressedKeys:
        # print(3)
        currentPressedKeys.remove(event.Key.lower())
        toReturn = False
    elif event.Key.lower() in appInfoObj.autoKeyDown and event.Key.lower() == appInfoObj.afterShift:
        # print(4)
        # print(event.Key.lower())
        appInfoObj.afterShift = None
        appInfoObj.autoKeyDown.remove(event.Key.lower())
        pyautogui.keyUp("shift")
        pyautogui.keyUp("shift")

        # appInfoObj.autoKeyDown.remove("lshift")
        # print("autoKeydown " + str(appInfoObj.autoKeyDown))
        # print("afterShift " + str(appInfoObj.afterShift))



    # print(str(currentPressedKeys))

    if appInfoObj.printKeyActions:
        if toReturn:
            print("Key released: " + event.Key.lower() + " and it was sent to the OS.")
        else:
            print("Key released: " + event.Key.lower() + " and it was not sent to the OS.")


    return toReturn




def OnKeyboardEvent(event):
    # print("afterShift is " + str(appInfoObj.afterShift))

    if event.MessageName in ["key sys down", "key down"]:

        if event.Key.lower() in appInfoObj.autoKeyDown:
            # print("event.Key: " + event.Key)
            # print("appInfoObj.autoKeyDown: " + str(appInfoObj.autoKeyDown))
            return functionAutoKeyPress(event)
        else:
            return functionKeyPress(event)

    elif event.MessageName in ["key up", "key sys up"]:
        return functionKeyRelease(event)



def convCharMap(action, fromFormat, toFormat):

    toReturn = None

    for item in characterMap:
        if fromFormat in item and item[fromFormat] == action:

            if not isinstance(item[toFormat], list):
                toReturn = [item[toFormat]]
            else:
                toReturn = item[toFormat]



    if not toReturn and isinstance(action, list):
        toReturn = []

        for char in action:
            convertedChar = char

            for item in characterMap:

                if fromFormat in item and item[fromFormat] == char:
                    convertedChar = item[toFormat]

            toReturn.append(convertedChar)



    if not toReturn:
        toReturn = [action]


    return toReturn



def addKeyValue(dict, keyVal, val):

    dict[keyVal] = val
    return dict


def createNewDict(action, fromFormat, yesAsEntered):

    newDict = {}
    if yesAsEntered:
        addKeyValue(newDict, "asEntered", [action])


    convertedToAutoGui = convCharMap(action, fromFormat, "pyAutoGui")
    convertedToHook = convCharMap(action, fromFormat, "pyHook")

    addKeyValue(newDict, "pyAutoGui", convertedToAutoGui)
    addKeyValue(newDict, "pyHook", convertedToHook)

    return newDict





def createPathList(path):

    pathList = []

    for char in path:
        pathList.append(createNewDict(char.lower(), "asEntered", True))



    if pathList[-1]["asEntered"] !=  "\\":
        pathList.append(createNewDict("\\", "pyAutoGui", False))



    # pathList.insert(0, createNewDict("back", "pyHook", False))
    # pathList.insert(0, createNewDict(["lcontrol", "a"], "pyHook", False))

    # print(str(pathList).replace("'", "\""))

    return pathList










characterMap = [
    {"pyHook": "space", "pyAutoGui": "space", "asEntered": " "},
    {"pyHook": "oem_5", "pyAutoGui": "\\", "asEntered": "\\"},
    {"pyHook": "back", "pyAutoGui": "backspace"},
    {"pyHook": ["lcontrol", "a"], "pyAutoGui": ["ctrl", "a"]},
    {"pyHook": ["lshift", "oem_1", "lshift"], "pyAutoGui": ":", "asEntered": ":"},
    {"pyHook": ["lshift", "oem_minus", "lshift"], "pyAutoGui": "_", "asEntered": "_"},
    {"pyHook": ["lmenu", "space"], "pyAutoGui": ["alt", "space"]},
    {"pyHook": "lshift", "pyAutoGui": "shift"}
]



comboList = [
                {"inputKeys": {"capital", "j"}, "outputComboKeys": ["left"]},
                {"inputKeys": {"capital", "k"}, "outputComboKeys": ["right"]},
                {"inputKeys": {"capital", "u"}, "outputComboKeys": ["up"]},
                {"inputKeys": {"capital", "m"}, "outputComboKeys": ["down"]},
                {"inputKeys": {"lshift", "capital", "m"}, "outputComboKeys": ["lshift", "down"]},
                {"inputKeys": {"capital", "d"}, "outputString": createPathList(r"C:\Users\cnaylor\Desktop")},
                {"inputKeys": {"capital", "a"}, "outputString": createPathList(r"Y:\Accounting")},
                {"inputKeys": {"capital", "c"}, "outputString": createPathList(r"Y:\Accounting\12_Creed")},
                # {"inputKeys": {"capital", "a"}, "outputString": ["lmenu", "space"], "outputString": createPathList(r"C:\users\creed")},
                # {"inputKeys": {"capital", "s"}, "outputString": ["lmenu", "space"], "outputString": createPathList(r"c:\users\creed\nas\synologydrive\computer\setup files")},
            ]



class appInfo():
    def __init__(self, autoKeyDown, printKeyActions, afterShift):
        self.autoKeyDown = autoKeyDown
        self.printKeyActions = printKeyActions
        self.afterShift = afterShift



appInfoObj = appInfo([], True, None)
currentPressedKeys = set()
pyautogui.PAUSE = 0



for process in psutil.process_iter():
    if process.name().lower() == "executor.exe":
        executorRunning = True

if executorRunning:
    executorApp = pywinauto.Application().connect(path="C:\\Users\\cnaylor\\Desktop\\Portable Applications\\Other\\Executor64bit\\Executor64bit\\Executor.exe")
else:
    executorApp = pywinauto.Application().start(cmd_line=u'"C:\\Users\\cnaylor\\Desktop\\Portable Applications\\Other\\Executor64bit\\Executor64bit\\Executor.exe"')


tmainformObj = executorApp.Executor
tcmdformObj = executorApp.TCmdForm




hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
print("ready")
pythoncom.PumpMessages()


















#
# pyHookToAutoGui = [
#     ["lmenu", "alt"],
#     ["lshift", "shift"],
#     ["lcontrol", "ctrl"]
# ]
#





# win32gui.ShowWindow(executorHwnd, win32con.SW_MINIMIZE)

# executorHwnd = win32gui.FindWindow(None, "Executor")
# win32gui.SetForegroundWindow(executorHwnd)

#     win32gui.ShowWindow(executorHwnd, 9)
#     tmainformObj.wait('ready')
#     teditObj = tmainformObj[u'3']
#     currentText = teditObj.texts()
#     # teditObj.set_focus()
#










# for key in ["alt", "space"]:
#     pyautogui.keyDown(key)
#
# for key in reversed["alt", "space"]:
#     pyautogui.keyUp(key)







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
#         appInfoObj.notAllowedToRelease = "Tab"
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

