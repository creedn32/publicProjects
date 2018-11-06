print("Cmt: Importing modules...")

import win32api    


       while True:
	if win32api.GetKeyState(0x01) == -127:
		print("left button clicked")
		break
