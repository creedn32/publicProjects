import pyautogui
pyautogui.PAUSE = 1


# for i in range(1):
#    pyautogui.moveTo(100, 100, duration=0.25)
#    pyautogui.moveTo(200, 100, duration=0.25)
#    pyautogui.moveTo(200, 200, duration=0.25)
#    pyautogui.moveTo(100, 200, duration=0.25)

print(pyautogui.position())


for i in range(2):
    pyautogui.click(648, 347)
    pyautogui.dragRel(90, 0, duration=1)

