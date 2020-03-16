from pprint import pprint as pp
from pathlib import Path
import json, subprocess, sys, psutil


pc = sys.argv[1]
thisPythonFilePath = Path(__file__).resolve()
thisPythonFileName = thisPythonFilePath.stem
jsonPath = str(thisPythonFilePath).replace("publicProjects", "privateData").replace("pythonFiles\\" + thisPythonFilePath.name, thisPythonFileName + "." + pc + ".json")


with open(jsonPath, "r") as filePathObj:
    fileObj = json.load(filePathObj)


for process in fileObj["processesToStart"]:
    # pass
    subprocess.Popen(process)


for process in psutil.process_iter():
    pass
    # pp(process.name())
    # pp(process.exe())
    # pp(process.cmdline())