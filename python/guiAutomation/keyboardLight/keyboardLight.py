import pyautogui


# print(pyautogui.KEYBOARD_KEYS)
# pyautogui.press('help')
# pyautogui.hotkey('fn', 'f10')

pyautogui.keyDown('fn')
pyautogui.keyDown('f10')
pyautogui.keyUp('f10')
pyautogui.keyUp('fn')