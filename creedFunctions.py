

def convertNothingToEmptyStr(s):
    if s:
        return str(s)
    else:
        return ""


def convertSingleSpaceToZero(s):
    if s == " ":
        return 0
    else:
        return s

def repetitiveKeyPress(numberOfTabs, keyToPress):
    import pyautogui

    for i in range(0, numberOfTabs):
        pyautogui.press(keyToPress)


def functionOnClick(x, y, button, pressed):
    if not pressed:
        print("Mouse {2} was {0} at {1}.".format("pressed" if pressed else "released", (x, y), button))
        return False


def pynputPressRel(controllerObj, keyToPress):
    controllerObj.press(keyToPress)
    controllerObj.release(keyToPress)


def printPythonInfo(var):
    from pprint import pprint

    pprint("Printed: " + str(var))
    pprint(var)

    pprint("Printed help: " + str(var))
    pprint(help(var))

    pprint("Printed dir: " + str(var))
    pprint(dir(var))



def convertKey(key):
    if key == "lmenu":
        return "alt"
    elif key == "oem_1":
        return ":"
    elif key == "oem_5":
        return "\\"
    else:
        return key



#
# def emptyCell(f):
#     if f:
#         return float(f)
#     else:
#         return 0




# def returnCellValue(row, column, array):
#     value = array[row - 1][column - 1]
#     return value



