import pathlib
__all__ = list()

for filePath in pathlib.Path(__file__).parent.iterdir():
    fileName = filePath.stem

    if fileName not in ["__init__", "__pycache__"]:
        __all__.append(fileName)

print(__all__)