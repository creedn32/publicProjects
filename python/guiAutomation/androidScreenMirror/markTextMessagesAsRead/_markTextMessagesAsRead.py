import pyautogui
import time
pyautogui.PAUSE = 0


print(pyautogui.position())

pyautogui.click(840, 40)
time.sleep(1)

for i in range(500):
    pyautogui.moveTo(740, 200, duration=0)
    pyautogui.dragRel(160, 0, duration=1)
    time.sleep(1)

