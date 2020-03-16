from pprint import pprint as pp
from pathlib import Path
import json, subprocess


pathToCurrentFile = Path(__file__).resolve()
currentFileName = pathToCurrentFile.stem
pathToJSON = str(pathToCurrentFile).replace("publicProjects", "privateData").replace("pythonFiles\\" + pathToCurrentFile.name, currentFileName + ".json")


with open(pathToJSON, "r") as filePathObj:
    fileObj = json.load(filePathObj)

for process in fileObj:
    subprocess.call(process)