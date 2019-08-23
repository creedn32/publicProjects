import pyWinhook
import pythoncom


def OnKeyboardEvent(event):

  print(pyWinhook.GetKeyState(0x20))
  
  if pyWinhook.GetKeyState(0x41) > 0 and pyWinhook.HookConstants.IDToName(event.KeyID) == "S":
    print("Combo detected")


  return True




  # print('MessageName: %s' % event.MessageName)
  # print('Message: %s' % event.Message)
  # print('Time: %s' % event.Time)
  # print('Window: %s' % event.Window)
  # print('WindowName: %s' % event.WindowName)
  # print('Ascii: %s' %  event.Ascii, chr(event.Ascii))
  # print('Key: %s' %  event.Key)
  # print('KeyID: %s' %  event.KeyID)
  # print('ScanCode: %s' %  event.ScanCode)
  # print('Extended: %s' %  event.Extended)
  # print('Injected: %s' %  event.Injected)
  # print('Alt %s' %  event.Alt)
  # print('Transition %s' %  event.Transition)
  # print('---')

  # return True to pass the event to other handlers
  # return False to stop the event from propagating




hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.HookKeyboard()
pythoncom.PumpMessages()


