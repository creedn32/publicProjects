# import subprocess

# if subprocess.check_output('xset q | grep LED', shell=True)[65] == 50 :
#     capslock = False
# if subprocess.check_output('xset q | grep LED', shell=True)[65] == 51 :
#     capslock = True

# print( "capslock ON is : ", capslock )

VK_NUMLOCK = 0x90
VK_CAPITAL = 0x14

def getKeyState(keyCode):

    import ctypes
    obj = ctypes.WinDLL("User32.dll")

    if (obj.GetKeyState(keyCode) & 0xffff) != 0:
        return True
    return False

print(getKeyState(VK_NUMLOCK))

    