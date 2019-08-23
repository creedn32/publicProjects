import pyWinhook
import pythoncom


def functionComboDetected():
    print("Combo detected")


def OnKeyboardEvent(event):

  if event.MessageName == "key down":
    if event.Key in comboList:
      currentPressedKeys.append(event.Key)

    if list(dict.fromkeys(currentPressedKeys)) == comboList and keyDownInfoObj.comboReleased:
        keyDownInfoObj.comboReleased = False
        functionComboDetected()

    if comboList[0] in currentPressedKeys:
      keyDownInfoObj.turnOffKeys = True


  if event.MessageName == "key up":
    if event.Key in comboList:
      currentPressedKeys[:] = [x for x in currentPressedKeys if x != event.Key]

    if len(currentPressedKeys) == 0:
      keyDownInfoObj.comboReleased = True

  if pyWinhook.GetKeyState(pyWinhook.HookConstants.VKeyToID('VK_CONTROL')) > 0 and pyWinhook.HookConstants.IDToName(event.KeyID) == "S":
    print("Combo detected")

  if comboList[0] not in currentPressedKeys:
    keyDownInfoObj.turnOffKeys = False



  print(currentPressedKeys)



  # print('MessageName: %s' % event.MessageName)
  # print('Message: %s' % event.Message)
  # print('Time: %s' % event.Time)
  # print('Window: %s' % event.Window)
  # print('WindowName: %s' % event.WindowName)
  # print('Ascii: %s' % event.Ascii, chr(event.Ascii))
  # print('Key: %s' % event.Key)
  # print('KeyID: %s' % event.KeyID)
  # print('ScanCode: %s' % event.ScanCode)
  # print('Extended: %s' % event.Extended)
  # print('Injected: %s' % event.Injected)
  # print('Alt %s' % event.Alt)
  # print('Transition %s' % event.Transition)
  # print('---')


  # return True to pass the event to other handlers
  # return False to stop the event from propagating

  if keyDownInfoObj.turnOffKeys:
    return False
  else:
    return True




class keyDownInfo():
  def __init__(self, comboReleased, turnOffKeys):
    self.comboReleased = comboReleased
    self.turnOffKeys = turnOffKeys

keyDownInfoObj = keyDownInfo(True, False)


comboList = ["A", "S"]
currentPressedKeys = []


hookManagerObj = pyWinhook.HookManager()
hookManagerObj.KeyDown = OnKeyboardEvent
hookManagerObj.KeyUp = OnKeyboardEvent
hookManagerObj.HookKeyboard()
pythoncom.PumpMessages()




