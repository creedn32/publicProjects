import pyWinhook
import pythoncom



def OnKeyboardEvent(event):
  # print(event.KeyID)

  # ctrl_pressed = pyHook.GetKeyState(pyHook.HookConstants.VKeyToID('VK_CONTROL') >> 15)

  # print(pyWinhook.GetKeyState(pyWinhook.HookConstants.VKeyToID('VK_CONTROL')))

  print(pyWinhook.GetKeyState(pyWinhook.HookConstants.VKeyToID('VK_CONTROL')))

  if pyWinhook.HookConstants.IDToName(event.KeyID) == 'C':
    print("c pressed")



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
  return True


hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.HookKeyboard()

pythoncom.PumpMessages()



