from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys
sys.path.append(str(Path(pathToThisPythonFile.parents[2], 'myPythonLibrary')))
import _myPyFunc
sys.path.append(str(Path(pathToThisPythonFile.parents[1], 'myGoogleSheetsLibrary')))
import _myGoogleSheetsFunc


 googleSheetsAPIObj = _myGoogleSheetsFunc.getGoogleSheetsAPIObj(['privateData', 'python', 'googleCredentials'])

 