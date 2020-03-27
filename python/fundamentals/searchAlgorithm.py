#breadth-first search

from pathlib import Path
from pprint import pprint as pp
import os

thisPythonFilePath = Path(__file__).resolve()
pathToPublicProjectsPython = thisPythonFilePath.parents[1]

def listOfSubFolders(folderPath):
    subFolderArray = []
 
    for node in folderPath.iterdir():
        if not node.is_file():
            subFolderArray.append(node)

    return subFolderArray


folderArray = [pathToPublicProjectsPython]

while folderArray:
    currentFolder = folderArray.pop(0)
    folderArray.extend(listOfSubFolders(currentFolder))
    
    for node in currentFolder.iterdir():
        if node.is_file() and node.suffix == '.py':
            pp(node)






# depth-first search:

# list nodes_to_visit = {root};
# while( nodes_to_visit isn't empty ) {
#   currentnode = nodes_to_visit.take_first();
#   nodes_to_visit.prepend( currentnode.children );
#   //do something
# }




# breadth-first search:

# list nodes_to_visit = {root};
# while( nodes_to_visit isn't empty ) {
#   currentnode = nodes_to_visit.take_first();
#   nodes_to_visit.append( currentnode.children );
#   //do something
# }
