from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
# sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
# import _myPyFunc

import pyautogui as g
from pprint import pprint as p
import time
import win32com.client
from datetime import date




def getExcelObj():

    excelObj = None

    while not excelObj:

        try: 
            excelObj = win32com.client.GetActiveObject("Excel.Application")
            # print("Running Excel instance found, returning object")

        except:
            pass

    #     excel = new_Excel(visible=visible)
    #     print("No running Excel instances, returning new instance")

    # else:
    #     if not excel.Workbooks.Count:
    #         excel.Workbooks.Add(1)
    #     excel.Visible = visible

    return excelObj



pathToTxtFile = Path(pathToThisPythonFile.parents[4], 'privateData', 'python', 'guiAutomation', 'saveStatementOfCashFlows', 'pathToSaveFile.txt')

with open(pathToTxtFile, 'rt') as pathToSaveFileTxt: 
    pathToSaveFile = Path(pathToSaveFileTxt.read())



# for year in range(1969, 2021):
for year in range(2016, 2021):

    quickbooksFromCoordinates = None

    while not quickbooksFromCoordinates:
        quickbooksFromCoordinates = g.locateOnScreen('quickBooksFrom.png')

    g.click(quickbooksFromCoordinates[0] + 45, quickbooksFromCoordinates[1] + 10)

    g.press(['backspace']*10)
    g.press(['delete']*10)
    g.write('01/01/' + str(year))
    g.press('tab')
    g.write('12/31/' + str(year))
    g.press('tab')

    while not g.locateOnScreen('quickBooksStatementOfCashFlowsTitle.png', grayscale=True):
        pass

    locatedBoxNetCashFlow = g.locateOnScreen('quickBooksNoCashFlow.png')

    if locatedBoxNetCashFlow:

        p('There are no cash flows in ' + str(year))
    
    else:

        p('There are cash flows in ' + str(year))

        g.hotkey('alt', 'x')
        g.press(['n', 'enter'])
    
        excelObj = getExcelObj()
        excelWb = None
        
        while not excelWb:

            try:
                for workbook in excelObj.Workbooks:
                    if workbook.Name[0:4] == 'Book':
                        excelWb = workbook

            except:
                pass

        excelSheet1 = excelWb.Worksheets('Sheet1')

        while 10 > excelSheet1.UsedRange.Rows.Count:
            pass

        excelObj.DisplayAlerts = False
        excelWb.SaveAs(Filename=str(Path(pathToSaveFile, 'Cash Flow - 1 - ' + str(year) + ' - ' + date.today().strftime('%Y%m%d') + '.xlsx')))
        excelWb.Close()
        excelObj.DisplayAlerts = True
        excelObj.Quit()

    break