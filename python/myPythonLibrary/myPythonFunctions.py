
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


def convertEmptyStrToZero(s):
    if s == "":
        return 0
    else:
        return s



def convertOutOfRangeToZero(array, index):
    if len(array) <= index:
        return 0
    else:
        return array[index]



def removeCommaFromStr(s):

    if isinstance(s, str):
        return s.replace(",", "")
    return s


def repetitiveKeyPress(numberOfTabs, keyToPress):
    import pyautogui

    for i in range(0, numberOfTabs):
        pyautogui.press(keyToPress)


def functionOnClick(x, y, button, pressed):
    if not pressed:
        print("Mouse {2} was {0} at {1}.".format("pressed" if pressed else "released", (x, y), button))
        return False



def printPythonInfo(var, length):
    from pprint import pprint

    pprint("1. Printing string of the variable: " + str(var)[0:length])
    pprint(var)

    pprint("2. Printing help() of the variable: " + str(var)[0:length])
    pprint(help(var))

    pprint("3. Printing dir() of the variable: " + str(var)[0:length])
    pprint(dir(var))



    pprint("4. Printing vars() of the variable: " + str(var)[0:length])
    try:
        pprint(vars(var))
    except:
        pprint("An exception occurred printing vars() of the variable")




    pprint("5. Printing and loopting through the variable: " + str(var)[0:length])
    try:
        for attr in dir(var):
            pprint("obj.%s = %r" % (attr, getattr(var, attr)))
    except:
        pprint("An exception occurred printing and loopting through the variable")



    pprint("6. Printing the .__dict__ of the variable: " + str(var)[0:length])
    try:
        pprint(var.__dict__)
    except:
        pprint("An exception occurred printing the .__dict__ of the variable")



    pprint("7. Printing the repr() of the variable: " + str(var)[0:length])
    try:
        pprint(repr(var))
    except:
        pprint("An exception occurred printing the repr() of the variable")








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



def startCode():

    global time
    import time

    print("Comment: Importing modules and setting up variables...")
    return time.time()



def getFromDict(dictObj, key):
    return dictObj[key]

def getFromList(listObj, position):
    return listObj[position]




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



