import sys, pathlib
from pprint import pprint as pp

# sys.path.append(str(pathlib.Path.cwd().parents[1]))
sys.path.append(str(pathlib.Path.cwd()/"publicProjects/python"))
# pp(sys.path)

from myPyLib import myPostBankTransactions

myPostBankTransactions.postTrans("Bank Transactions")

#




