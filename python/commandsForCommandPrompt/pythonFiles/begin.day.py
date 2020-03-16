from pprint import pprint as pp
from pathlib import Path
import json, subprocess, sys


pc = sys.argv[1]
pathToCurrentFile = Path(__file__).resolve()
currentFileName = pathToCurrentFile.stem
pathToJSON = str(pathToCurrentFile).replace("publicProjects", "privateData").replace("pythonFiles\\" + pathToCurrentFile.name, currentFileName + "." + pc + ".json")


with open(pathToJSON, "r") as filePathObj:
    fileObj = json.load(filePathObj)

for process in fileObj:
    # pass
    subprocess.call(process)