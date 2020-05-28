from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys

sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

from cryptography.fernet import Fernet
from pprint import pprint as p



def generateKey(pathToStoreKeyFile):
    """
    Generates a key and save it into a file
    """
    generatedKey = Fernet.generate_key()

    with open(pathToStoreKeyFile, 'wb') as keyFileObj:
        keyFileObj.write(generatedKey)



def openSavedKey(pathToKeyFile):
    """
    Loads the key from the current directory named `keyFile.key`
    """

    return open(pathToKeyFile, 'rb').read()



def encryptFile(pathOfFileToProcess, savedKey):
    """
    Given a pathOfFileToProcess (str) and key (bytes), it encrypts the file and write it
    """

    fernetObjUsingKey = Fernet(savedKey)

    with open(pathOfFileToProcess, "rb") as fileObj:
        # read all file data
        fileData = fileObj.read()


    # encrypt data
    encryptedFileData = fernetObjUsingKey.encrypt(fileData)

    # write the encrypted file
    with open(pathOfFileToProcess, "wb") as fileObj:
        fileObj.write(encryptedFileData)



def decryptFile(pathOfFileToProcess, savedKey):
    """
    Given a pathOfFileToProcess (str) and key (bytes), it decrypts the file and write it
    """

    fernetObjUsingKey = Fernet(savedKey)

    with open(pathOfFileToProcess, "rb") as fileObj:
        # read the encrypted data
        encryptedFileData = fileObj.read()

    # decrypt data
    decryptedFileData = fernetObjUsingKey.decrypt(encryptedFileData)

    # write the original file
    with open(pathOfFileToProcess, "wb") as fileObj:
        fileObj.write(decryptedFileData)





pathToKeyFileDirectory = _myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')
keyFileName = 'keyForEncryption.key'
pathToStoreKeyFile = Path(pathToKeyFileDirectory, keyFileName)
# generateKey(pathToStoreKeyFile)

savedKey = openSavedKey(Path(pathToKeyFileDirectory, keyFileName))
# savedKey = "asdfs"

pathOfFileToProcess = Path(pathToThisPythonFile.parents[0], 'fileToProcess.txt')

# encryptFile(pathOfFileToProcess, savedKey)

# decryptFile(pathOfFileToProcess, savedKey)




# encrypt a string

# unencryptedMessage = 'secret message'.encode()
# fernetObjUsingKey = Fernet(savedKey)
# encryptedMessage = fernetObjUsingKey.encrypt(unencryptedMessage)

# print(encryptedMessage)

# decryptedMessage = fernetObjUsingKey.decrypt(encryptedMessage)
# print(decryptedMessage)











