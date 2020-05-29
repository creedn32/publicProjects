from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys

sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

from pprint import pprint as p




pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
pathToKeyFile = Path(pathToRepos, 'privateData', 'python', 'googleCredentials', 'keyForEncryption.key')
# _myPyFunc.generateKey(pathToKeyFile)

savedKey = _myPyFunc.openSavedKey(pathToKeyFile)
# savedKey = "asdfs"

pathOfFileToProcess = Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'jsonWithAPIKey.json')

_myPyFunc.encryptFile(pathOfFileToProcess, savedKey)

# _myPyFunc.decryptFile(pathOfFileToProcess, savedKey)




# encrypt a string

# unencryptedMessage = 'secret message'.encode()
# fernetObjUsingKey = Fernet(savedKey)
# encryptedMessage = fernetObjUsingKey.encrypt(unencryptedMessage)

# print(encryptedMessage)

# decryptedMessage = fernetObjUsingKey.decrypt(encryptedMessage)
# print(decryptedMessage)











