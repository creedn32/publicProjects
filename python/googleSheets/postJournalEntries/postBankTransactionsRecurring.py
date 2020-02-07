import sys, pathlib
sys.path.append(str(pathlib.Path.cwd().parents[1]))
from myPyLib import myPostBankTransactions


myPostBankTransactions.postTrans("Bank Transactions - Recurring")