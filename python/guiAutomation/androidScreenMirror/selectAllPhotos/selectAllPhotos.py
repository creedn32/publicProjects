import pyautogui
import time
pyautogui.PAUSE = 0


# print(pyautogui.position())

# pyautogui.click(840, 40)
# time.sleep(1)

pyautogui.mouseDown()
pyautogui.move(450, 40, 2)
pyautogui.move(0, 700, 2)
time.sleep(3)
pyautogui.mouseUp()
# pyautogui.drag(450, 450, 2, button='left')
# pyautogui.drag(0, 450, 2, button='left')


# for i in range(500):
#     pyautogui.moveTo(740, 200, duration=0)
#     pyautogui.dragRel(160, 0, duration=1)
#     time.sleep(1)

