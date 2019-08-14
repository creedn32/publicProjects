import pyautogui

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
    for i in range(0, numberOfTabs):
        pyautogui.press(keyToPress)





##def emptyCell(f):
##    if f:
##        return float(f)
##    else:
##        return 0
