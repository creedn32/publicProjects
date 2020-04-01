from pynput.keyboard import Key, Listener

def onPressFunction(pressedKey):
    print('{0} pressed'.format(
        pressedKey))

def onReleaseFunction(releasedKey):
    print('{0} release'.format(
        releasedKey))
    if releasedKey == Key.esc:
        # Stop listener
        return False

# Collect events until released
with Listener(on_press=onPressFunction, on_release=onReleaseFunction) as listenerObj:
    listenerObj.join()