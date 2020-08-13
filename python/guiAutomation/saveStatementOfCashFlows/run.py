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

if len(sys.argv) > 2:
    startingYear = int(sys.argv[2])
else:
    startingYear = 1969 

for year in range(startingYear, 2021):

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

        g.hotkey('alt', 't')
        g.press(['p', 'enter'])

        while not g.locateOnScreen('quickbooksSave.png'):
            pass

        g.write(str(Path(pathToSaveFile, 'Cash Flow - ' + sys.argv[1] + ' - ' + str(year) + ' - ' + date.today().strftime('%Y%m%d'))))
    
        g.press('enter')

        
        # excelObj = getExcelObj()
        # excelWb = None
        
        # while not excelWb:

        #     try:
        #         for workbook in excelObj.Workbooks:
        #             if workbook.Name[0:4] == 'Book':
        #                 excelWb = workbook

        #     except:
        #         pass


        # excelSheet1 = None
        
        # while not excelSheet1:

        #     try:
        #         excelSheet1 = excelWb.Worksheets('Sheet1')
        #     except:
        #         pass


        # # excelSheet1.Activate()

        # usedRows = 0
        
        # while usedRows < 10:
        #     try:
        #         usedRange = excelSheet1.Range(excelSheet1.usedRange.Address)
        #         usedRows = usedRange.Rows.Count
        #         p(usedRows)
        #     except:
        #         pass

        # # excelObj.WindowState = -4137 # set this number meaning full size
        # # excelObj.Visible = 1

        # # while 10 > excelSheet1.UsedRange.Rows.Count:
        # #     p('Used range is ' + str(excelSheet1.UsedRange.Rows.Count) + ' rows.')

        # excelObj.DisplayAlerts = False
        # excelWb.SaveAs(Filename=str(Path(pathToSaveFile, 'Cash Flow - ' + sys.argv[1] + ' - ' + str(year) + ' - ' + date.today().strftime('%Y%m%d') + '.xlsx')))
        # # excelObj.WindowState = -4140
        # excelWb.Close()
        # excelObj.DisplayAlerts = True
        # excelObj.Quit()

    # break