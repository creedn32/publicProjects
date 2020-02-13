import sys, pathlib
from pprint import pprint as pp

# pp(pathlib.Path.cwd().parents[1])
sys.path.append(str(pathlib.Path.cwd().parents[1]))
# pp(sys.path)

from myPyLib import myPostBankTransactions

import datetime, pynput.mouse #, win32api, win32con, pyautogui

# myPostBankTransactions.postTrans("Bank Transactions")