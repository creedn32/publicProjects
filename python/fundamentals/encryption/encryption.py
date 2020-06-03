from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys

sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

from pprint import pprint as p




pathToRepos = _myPyFunc.getPathUpFolderTree(pathToThisPythonFile, 'repos')
pathToKeyFile = Path(pathToRepos, 'privateData', 'python', 'encryption', 'savedEncryptionKey.key')
# _myPyFunc.generateKey(pathToKeyFile)

savedKey = _myPyFunc.openSavedKey(pathToKeyFile)
# savedKey = "asdfs"

pathOfFileToProcess = Path(pathToThisPythonFile.parents[4], 'privateData', 'python', 'googleCredentials', 'usingOAuthGspread', 'authorizedUserFile.json')

_myPyFunc.encryptFile(pathOfFileToProcess, savedKey, pathToSaveEncryptedFile=Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'configData', 'encryptedAuthorizedUserFile.json'))

# _myPyFunc.decryptFile(pathOfFileToProcess, savedKey)




# encrypt a string

# unencryptedMessage = 'secret message'.encode()
# fernetObjUsingKey = Fernet(savedKey)
# encryptedMessage = fernetObjUsingKey.encrypt(unencryptedMessage)

# print(encryptedMessage)

# decryptedMessage = fernetObjUsingKey.decrypt(encryptedMessage)
# print(decryptedMessage)











