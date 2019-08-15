

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


#
# def emptyCell(f):
#     if f:
#         return float(f)
#     else:
#         return 0




# def returnCellValue(row, column, array):
#     value = array[row - 1][column - 1]
#     return value



