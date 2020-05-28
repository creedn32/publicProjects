from cryptography.fernet import Fernet

def writeKey():
    """
    Generates a key and save it into a file
    """
    generatedKey = Fernet.generate_key()

    with open('keyFile.key', 'wb') as keyFileObj:
        keyFileObj.write(generatedKey)


def openSavedKey():
    """
    Loads the key from the current directory named `keyFile.key`
    """

    return open('keyFile.key', 'rb').read()


def encryptFile(fileName, savedKey):
    """
    Given a fileName (str) and key (bytes), it encrypts the file and write it
    """

    fernetObjUsingKey = Fernet(savedKey)

    with open(fileName, "rb") as fileObj:
        # read all file data
        fileData = fileObj.read()


    # encrypt data
    encryptedFileData = fernetObjUsingKey.encrypt(fileData)

    # write the encrypted file
    with open(fileName, "wb") as fileObj:
        fileObj.write(encryptedFileData)


def decryptFile(fileName, savedKey):
    """
    Given a fileName (str) and key (bytes), it decrypts the file and write it
    """

    fernetObjUsingKey = Fernet(savedKey)

    with open(fileName, "rb") as fileObj:
        # read the encrypted data
        encryptedFileData = fileObj.read()

    # decrypt data
    decryptedFileData = fernetObjUsingKey.decrypt(encryptedFileData)

    # write the original file
    with open(fileName, "wb") as fileObj:
        fileObj.write(decryptedFileData)





# writeKey()
savedKey = openSavedKey()

fileName = "textFile.txt"

# encryptFile(fileName, savedKey)
decryptFile(fileName, savedKey)






# unencryptedMessage = 'secret message'.encode()
# fernetObjUsingKey = Fernet(savedKey)
# encryptedMessage = fernetObjUsingKey.encrypt(unencryptedMessage)

# print(encryptedMessage)

# decryptedMessage = fernetObjUsingKey.decrypt(encryptedMessage)
# print(decryptedMessage)











