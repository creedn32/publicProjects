import sys

if 'win32com' not in sys.modules:
    import win32com.client

if 'pyautogui' not in sys.modules:
    import pyautogui

if 'pywinauto' not in sys.modules:
    import pywinauto



#os.chdir(os.path.dirname(sys.argv[0]))
#wb = openpyxl.load_workbook('JE\'s To Post.xlsx')
#sheet = wb.get_sheet_by_name('Bank Transactions')



#xl = win32com.client.Dispatch('excel.application')
#xl.Workbooks.Open('')
xl = win32com.client.GetObject(Class='Excel.Application')


selectedCells = xl.Selection.Value
caption = 'Bank Transaction Entry  -  GPPRD (CNAYLOR)'
pyautogui.PAUSE = .5



appGPBank = pywinauto.application.Application()
appGPBank.connect(title=caption)
windowGPBank = appGPBank[caption]
pywinauto.win32functions.SetForegroundWindow(pywinauto.findwindows.find_window(title=caption))
boxTransactionDateGPBank = windowGPBank[u'0']
boxTransactionDateGPBank.click()


pyautogui.press(['home', 'tab', 'home', 'tab'])
pyautogui.typewrite(str(int(selectedCells[0][2])))
pyautogui.press('tab')
pyautogui.typewrite(str(selectedCells[0][3]))
pyautogui.press(['tab', 'tab'])
pyautogui.typewrite(str(selectedCells[0][4]))
pyautogui.press('tab')
pyautogui.typewrite(str(selectedCells[0][5]))
pyautogui.press('tab')
pyautogui.typewrite(str(selectedCells[0][6]))
pyautogui.press('tab')




#appWinExplorer.start(cmd_line=u'C:\\Windows\\Explorer.EXE')

#appExcel = pywinauto.application.Application()
#appExcel.connect(title='Book1 - Excel')
#windowExcel = appExcel['Book1 - Excel']
#boxFormulaExcel = windowExcel[u'EXCEL<']



##
##for rowOfCellObjects in sheet['A506':'I506']:
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[0].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[1].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[2].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[3].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[4].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[5].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[6].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[7].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys(rowOfCellObjects[8].value, with_spaces = True)
##        boxFormulaExcel.TypeKeys('^+{HOME}')
##        boxFormulaExcel.TypeKeys('{BACKSPACE}')
##        print('end of row')
##        

        


##
##appNotepad = pywinauto.application.Application()
##appNotepad.start('C:\\Windows\\System32\\notepad.exe')
##windowNotepad = appNotepad['Untitled - Notepad']
##type(windowNotepad)
#Playing with list/combobox
#mainWindow.MenuItem(u'F&ormat->&Font...').click()
#formatWindow = app['Font'] 
#fontComboBox = formatWindow['Font:ComboBox']
#fontComboBoxProps  = fontComboBox.GetProperties()
#print(fontComboBox)
#print(fontComboBoxProps['texts']) #Prints all items in the combobox
#formatWindow['Ok'].click()

