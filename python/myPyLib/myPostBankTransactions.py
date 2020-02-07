

def postTrans(sheetName):


    import sys, pathlib
    sys.path.append(str(pathlib.Path.cwd().parents[1]))
    from myPyLib import myPyFunc, myGoogleSheetsFunc

    splitTime = myPyFunc.printElapsedTime(False, "Starting code")

    import datetime, pynput.mouse, win32api, win32con, pyautogui
    from pprint import pprint as pp

    # class moduleNameClass:
    #     pass
    #
    # moduleName = "myGoogleSheetsPythonLibrary"
    # moduleNameObj = moduleNameClass()
    #
    #
    #
    #
    # for filePath in pathlib.Path(pathlib.Path.cwd().parents[0]/moduleName).iterdir():
    #     if filePath.stem not in ["__init__", "__pycache__"]:
    #         importedModuleObj = importlib.import_module(moduleName + "." + filePath.stem)
    #         setattr(moduleNameObj, filePath.stem, importedModuleObj)
    # myGoogleSheetsPythonLibrary = moduleNameObj


    # spreadsheetIDStr = "1uQezYVWkLZEvXzbprJPLRyDdyn04MdO-k6yaiyZPOx8"   #ID of public Google Sheet
    spreadsheetIDStr = "1nR8wJISZjeJh6DCBf1OTpiG6rdY5DyyUtDI763axGhg"  # ID of private Google Sheet
    # spreadsheetIDStr = "1kCI36ash9JI2AO0mCjbIUndRo93oiWgx2KWgeeJeP28"  #ID of simple Google Sheet

    changeCellColor = False
    numLockChanged = False
    pyautogui.PAUSE = 0
    activateKeyboard = True



    googleSheetsAPIObj = myGoogleSheetsFunc.authFunc()
    googleSheetsData = googleSheetsAPIObj.get(spreadsheetId=spreadsheetIDStr, includeGridData=True).execute()




    for dict in googleSheetsData["sheets"]:
        if dict["properties"]["title"] == sheetName:
            currentSheetIDStr = dict["properties"]["sheetId"]
            currentSheetData = dict["data"][0]["rowData"]



    requestDictionary = {}
    requestDictionary["requests"] = []
    requestDictionary["requests"].append({})
    requestDictionary["requests"][0]["repeatCell"] = {}
    requestDictionary["requests"][0]["repeatCell"]["range"] = {}
    requestDictionary["requests"][0]["repeatCell"]["range"]["sheetId"] = currentSheetIDStr
    requestDictionary["requests"][0]["repeatCell"]["range"]["startRowIndex"] = 0
    requestDictionary["requests"][0]["repeatCell"]["range"]["endRowIndex"] = 0
    requestDictionary["requests"][0]["repeatCell"]["cell"] = {}
    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"] = {}
    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"] = {}
    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["red"] = 208 /255
    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["green"] = 224 /255
    requestDictionary["requests"][0]["repeatCell"]["cell"]["userEnteredFormat"]["backgroundColor"]["blue"] = 227 /255
    requestDictionary["requests"][0]["repeatCell"]["fields"] = "userEnteredFormat(backgroundColor)"



    splitTime = myPyFunc.printElapsedTime(splitTime, "Finished importing modules and intializing variables")


    if activateKeyboard:

        with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
            print("Click on 'Clear' to begin posting...")
            listenerObj.join()




    for row in currentSheetData[1:]:


        if myGoogleSheetsFunc.isWhite(row["values"][0]) and myGoogleSheetsFunc.hasFormattedValue(row["values"][0]):


            if row["values"][0]["formattedValue"] != "Enter/Edit" and activateKeyboard:

                # pprint(row)
                print("Row " + str("") + " will be populated into the Great Plains entry window.")

                if win32api.GetKeyState(win32con.VK_NUMLOCK) == 1:
                    pyautogui.press("numlock")


                for col in range(0, 9):

                    numberTabs = 1

                    try:
                        string = str(row["values"][col]["formattedValue"])
                    except:
                        string = ""


                    if col == 0:

                        pyautogui.press(["down", "up", "up", "up"])

                        if string == "Enter Receipt":
                            pyautogui.press("down")


                    elif col == 1:

                        pyautogui.press(["down", "up", "up", "up"])

                        if string == "Cash":
                            pyautogui.press("down")
                        elif string == "Increase Adjustment":
                            myPyFunc.repetitiveKeyPress(2, "down")
                        elif string == "Decrease Adjustment":
                            myPyFunc.repetitiveKeyPress(3, "down")


                    elif col == 2:

                        # string = row["values"][col]["formattedValue"]
                        dateObj = datetime.datetime.strptime(string, "%m/%d/%Y")
                        # print(datetime.ParseExact(string, "yyMMdd", CultureInfo.InvariantCulture))
                        string = dateObj.strftime("%m%d%Y")


                    elif col == 3:
                        numberTabs = 2

                    elif col == 6:
                        numberTabs = 6


                    elif col == 7:
                        string = string.replace("-", "")

                        if row["values"][0]["formattedValue"] != "Enter Transaction" or \
                                (row["values"][0]["formattedValue"] == "Enter Transaction" and row["values"][1][
                            "formattedValue"] not in ["Check", "Decrease Adjustment"]):
                            numberTabs = 2

                    if col in [6, 8]:
                        # if len(string.split(".")) == 1:
                        # string = string + "00"
                        string = string.lstrip("$").replace(".", "").replace(",", "")

                    if col not in [0, 1]:

                        for letter in string:

                            if ord(letter) in (
                                    list(range(123, 127)) + list(range(94, 96)) + list(range(62, 91)) + [60, 58] + list(
                                    range(40, 44)) + list(range(33, 39))):

                                pyautogui.PAUSE = .0000000000001
                                pyautogui.keyDown("shift")
                                pyautogui.press(letter)
                                pyautogui.keyUp("shift")
                                pyautogui.PAUSE = 0

                            else:
                                pyautogui.press(letter)

                    myPyFunc.repetitiveKeyPress(numberTabs, "tab")

                if win32api.GetKeyState(win32con.VK_NUMLOCK) == 0:
                    pyautogui.press("numlock")

                with pynput.mouse.Listener(on_click=myPyFunc.functionOnClick) as listenerObj:
                    print("Click on 'Post' or 'Clear' to continue with this entry...")
                    listenerObj.join()


