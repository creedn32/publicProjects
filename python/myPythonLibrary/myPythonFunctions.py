from pprint import pprint as pp


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




def saveFile(dataObj, path):

    from pprint import pprint as pp

    with open(path, "w") as out:
        pp(dataObj, stream=out)




def filterListOfLists(list, filterObj):

    listToReturn = []

    for item in list:

        for dictionary in filterObj:

            filterCount = 0

            for key, value in dictionary.items():
                if item[key] == value:
                    filterCount = filterCount + 1

            if filterCount == len(dictionary):
                listToReturn.append(item)

    # pp(listToReturn)

    return listToReturn



def sumListOfLists(list, index):

    runningSum = 0

    for item in list:
        runningSum = runningSum + float(item[index] or 0)

    return runningSum


def sumFormulasListOfLists(list, index):

    runningFormula = "="

    for item in list:

        if isinstance(item[index], str):
            runningFormula = runningFormula + "+" + item[index].strip("=")
        else:
            runningFormula = runningFormula + "+" + str(item[index])



    return runningFormula



def convertTwoColumnListToDict(listObj, startingRow):

    dictToReturn = {}

    for item in listObj[1:]:
        dictToReturn[item[0]] = item[1]

    return dictToReturn




def convertSerialDateToDateWithoutDashes(serialDate):

    from datetime import date

    dateObj = date.fromordinal(date(1900, 1, 1).toordinal() + serialDate - 2)
    dateStr = str(dateObj.year) + str(dateObj.month).zfill(2) + str(dateObj.day).zfill(2)

    return dateStr



def convertSerialDateToMySQLDate(serialDate):

    from datetime import date

    dateObj = date.fromordinal(date(1900, 1, 1).toordinal() + serialDate - 2)
    dateStr = str(dateObj.year) + "-" + str(dateObj.month).zfill(2) + "-" + str(dateObj.day).zfill(2)

    return dateStr


def convertSerialDateToYear(serialDate):
    from datetime import date

    dateObj = date.fromordinal(date(1900, 1, 1).toordinal() + serialDate - 2)

    return str(dateObj.year)



def convertDateToSerialDate(dateObj):

    import datetime

    temp = datetime.datetime(1899, 12, 30)    # Note, not 31st Dec but 30th!
    delta = dateObj - temp

    return float(delta.days) + (float(delta.seconds) / 86400)



def executeSQLStatements(sqlList, sqlCursor):

    for cmd in sqlList:
        sqlCursor.execute(cmd)





def createDatabase(databaseName, dbPath, tblName, columnsObj):

    import sqlite3

    dbPath = dbPath + "\\" + databaseName
    sqlObj = {"sqlConnection": sqlite3.connect(dbPath)}
    sqlObj["sqlCursor"] = sqlObj["sqlConnection"].cursor()

    createTable(tblName, columnsObj, sqlObj["sqlCursor"])

    return sqlObj


def closeDatabase(sqlConnection):

    sqlConnection.commit()
    sqlConnection.close()


def createTable(tblName, columnsObj, sqlCursor):

    sqlList = []

    sqlList.append("drop table if exists " + tblName + ";")
    sqlCommand = "create table " + tblName + " ("

    for key, value in columnsObj.items():
        sqlCommand = sqlCommand + key + " " + value

        if key != next(reversed(columnsObj)):
            sqlCommand = sqlCommand + ", "

    sqlCommand = sqlCommand + ");"


    sqlList.append(sqlCommand)

    # sqlList.append(
    #     "create table " + tblName + " (tranDate date, account varchar(255), accountType varchar(255), accountCategory varchar(255), amount float, tranType varchar(255), stockName varchar(255), broker varchar(255), lot varchar(255), shares float);")


    executeSQLStatements(sqlList, sqlCursor)



def createTableAs(tblName, sqlCursor, sqlCommand):

    sqlList = ["drop table if exists " + tblName, "create table " + tblName + " as " + sqlCommand]
    executeSQLStatements(sqlList, sqlCursor)




def populateTable(totalRows, totalColumns, tblName, sheetDataList, sqlCursor, listOfDateColumns):

    sqlCommand = "insert into " + tblName + " values "

    for indexOfRow in range(1, totalRows):

        sqlCommand = sqlCommand + "("

        for indexOfColumn in range(0, totalColumns):

            sqlCommand = sqlCommand + "\""

            if indexOfColumn in listOfDateColumns:
                sqlCommand = sqlCommand + convertSerialDateToMySQLDate(
                    sheetDataList[indexOfRow][indexOfColumn])
            else:
                sqlCommand = sqlCommand + str(sheetDataList[indexOfRow][indexOfColumn])

            sqlCommand = sqlCommand + "\""

            if indexOfColumn != totalColumns - 1:
                sqlCommand = sqlCommand + ", "

        sqlCommand = sqlCommand + ")"

        if indexOfRow != totalRows - 1:
            sqlCommand = sqlCommand + ", "

    sqlCommand = sqlCommand + ";"

    executeSQLStatements([sqlCommand], sqlCursor)
     



def getQueryResult(sqlCommand, tblName, sqlCursor, includeColumnNames):

    sqlCursor.execute(sqlCommand)
    queryResult = sqlCursor.fetchall()

    if includeColumnNames:

        colNames = []

        for column in sqlCursor.description:
            colNames.append(column[0])

        # colNames = getSQLColNamesList(sqlCursor, tblName, False)

        for i in range(0, len(colNames)):
            if colNames[i].startswith("'"):
                # pp(1)
                colNames[i] = colNames[i][1:]

            if colNames[i].endswith("'"):
                # pp(2)
                colNames[i] = colNames[i][:-1]


        queryResult.insert(0, colNames)

    # pp(queryResult)

    return queryResult


def createPivotColDict(fieldToPivot, fieldColIndex, fieldToSum, rowStartIndex,  dataList):

    colData = []

    for row in dataList[rowStartIndex:]:
        colData.append(row[fieldColIndex])

    colData = list(set((colData)))
    colData.sort()

    colDict = {"colList": colData}
    pivotColStr = ""

    for colItem in colData:
        pivotColStr = pivotColStr + "sum(case when " + fieldToPivot + " = '" + str(colItem) + "' then " + fieldToSum + " end) as '" + str(colItem) + "'"

        if colItem != colData[len(colData) - 1]:
            pivotColStr = pivotColStr + ", "

    colDict["pivotColStr"] = pivotColStr

    return colDict




def getAllColumns(colDict, sqlCursor):

    colList = []

    for i in range(0, len(colDict)):

        tableColNamesList = getSQLColNamesList(sqlCursor, colDict[i]["table"], True)

        tableColNamesWithoutExcl = []

        for col in tableColNamesList:

            excluded = False

            for excludedField in colDict[i]["excludedFields"]:
                if ".'" + excludedField + "'" in col:
                    excluded = True

            if not excluded:
                # if "additionalColumnText" in colDict[i]:
                #     tableColNamesWithoutExcl.append(col + " as '" + col.split("'")[1] + " " + colDict[i]["additionalColumnText"] + "'")
                # else:
                tableColNamesWithoutExcl.append(col)

        colList.extend(tableColNamesWithoutExcl)

    return listToStr(colList)





def getSQLColNamesList(sqlCursor, tblName, addTableName):

    colNames = []

    # for tblName in tblNames:

    sqlCursor.execute("pragma table_info(" + tblName + ");")
    fetchedList = sqlCursor.fetchall()

    addedTableName = ""

    if addTableName:
        addedTableName = tblName + "."

    colNames.extend([addedTableName + "'" + item[1] + "'" for item in fetchedList])

    return colNames




def fieldsDictToStr(dict, fieldBool, aliasBool):

    strToReturn = ""

    for i in range(0, len(dict)):

        if fieldBool:

            strToReturn = strToReturn + dict[i]["field"]

        if fieldBool and aliasBool:

            strToReturn = strToReturn + " as "

        if aliasBool:

            strToReturn = strToReturn + dict[i]["alias"]

        if i != len(dict) - 1:
            strToReturn = strToReturn + ", "


        # strToReturn = strToReturn + item

    return strToReturn




def listToStr(list):
    return ", ".join(list)



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



