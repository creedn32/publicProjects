import webbrowser, pyautogui, time




def setSystemVolume():

    for i in range(0, 50):
        pyautogui.press('volumedown')

    for i in range(0, 25):
        pyautogui.press('volumeup')

    time.sleep(3)


def playYouTubeMovies():
    webbrowser.open('https://www.youtube.com/embed/NvZtkt9973A?start=1&fs=1&autoplay=1')
    time.sleep(4)
    webbrowser.open('https://www.youtube.com/embed/Xf5QTs2NLRc?start=1&fs=1&autoplay=1')


def moveMouse():

    time.sleep(10)

    while True:
        pyautogui.moveRel(500, 500, 1)
        pyautogui.moveRel(-500, -500, 1)



def pressKey():

    pyautogui.FAILSAFE = False

    time.sleep(20)

    for i in range(0, 3):
        pyautogui.press('0')

    pyautogui.FAILSAFE = True





# setSystemVolume()
# playYouTubeMovies()
pressKey()





# https://developers.google.com/youtube/iframe_api_reference#setVolume
# player.setVolume(volume:Number):Void
# Sets the volume. Accepts an integer between 0 and 100.

# document.getElementsByClassName('video-stream html5-main-video')[0].volume = 0


# import scheduler, time

# # Set up scheduler
# s = sched.scheduler(time.localtime, time.sleep)
# # Schedule when you want the action to occur
# s.enterabs(time.strptime('Tue May 01 11:05:17 2018'), 0, action)
# # Block until the action has been run
# s.run()

