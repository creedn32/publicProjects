import sys, pathlib
from pprint import pprint as pp

sys.path.append(str(pathlib.Path.cwd()/"publicProjects/python"))

from myPyLib import myPostBankTransactions

myPostBankTransactions.postTrans("Bank Transactions")