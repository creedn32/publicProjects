import sys
from pathlib import Path
from pprint import pprint as pp

thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[2]

sys.path.append(str(pathToPublicProjectsPython))

from myPyLib import myPostBankTransactions


myPostBankTransactions.postTrans("Bank Transactions - Recurring", pathToPublicProjectsPython)