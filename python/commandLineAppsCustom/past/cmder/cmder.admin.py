import os

powershellCommand = "Start-Process \"cmder.exe\" -Verb RunAs"
os.system('Powershell -Command ' + powershellCommand)

