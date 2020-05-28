from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys

sys.path.append(str(Path(pathToThisPythonFile.parents[3], 'herokuGorilla', 'backend', 'python', 'myPythonLibrary')))
import _myPyFunc

from cryptography.fernet import Fernet
from pprint import pprint as p

def generateKey():
    """
    Generates a key and save it into a file
    """
    generatedKey = Fernet.generate_key()

    with open('keyFile.key', 'wb') as keyFileObj:
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







# generateKey()

pathToKeyFileDirectory = _myPyFunc.replacePartOfPath(pathToThisPythonFile.parents[0], 'publicProjects', 'privateData')
savedKey = openSavedKey(Path(pathToKeyFileDirectory, 'keyForEncryption.key'))
# savedKey = "asdfs"
pathOfFileToProcess = Path(pathToThisPythonFile.parents[0], 'textFile.txt')

# encryptFile(pathOfFileToProcess, savedKey)

decryptFile(pathOfFileToProcess, savedKey)






# unencryptedMessage = 'secret message'.encode()
# fernetObjUsingKey = Fernet(savedKey)
# encryptedMessage = fernetObjUsingKey.encrypt(unencryptedMessage)

# print(encryptedMessage)

# decryptedMessage = fernetObjUsingKey.decrypt(encryptedMessage)
# print(decryptedMessage)











