

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



def printPythonInfo(var):
    from pprint import pprint

    pprint("Printing the variable as a string: " + str(var))
    pprint(var)

    pprint("Printing help() of the variable: " + str(var))
    pprint(help(var))

    pprint("Printing dir() of the variable: " + str(var))
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





def columnToLetter(columnNumber):
    letter = ""

    while columnNumber > 0:
        columnNumber, remainder = divmod(columnNumber - 1, 26)
        letter = chr(65 + remainder) + letter

    return letter






    #
    # while column > 0:
    #     temp = (column - 1) % 26
    #     print(temp + 65)
    #     letter = ''.join(map(chr, temp + 65))
    #     # letter = String.fromCharCode(temp + 65) + letter
    #     column = (column - temp - 1) / 26
    #
    # # return letter
    # return column



# function letterToColumn(letter)
# {
#   var column = 0, length = letter.length;
#   for (var i = 0; i < length; i++)
#   {
#     column += (letter.charCodeAt(i) - 64) * Math.pow(26, length - i - 1);
#   }
#   return column;
# }









# def pynputPressRel(controllerObj, keyToPress):
#     controllerObj.press(keyToPress)
#     controllerObj.release(keyToPress)

#
# def emptyCell(f):
#     if f:
#         return float(f)
#     else:
#         return 0




# def returnCellValue(row, column, array):
#     value = array[row - 1][column - 1]
#     return value



