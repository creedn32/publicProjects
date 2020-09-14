import pynput.mouse, time

print("a")

def functionOnClick(x, y, button, pressed):
    print("Mouse clicked at {0}, {1} with {2} and pressed is {3}".format(x, y, button, pressed))
    listenerObj.stop()

with pynput.mouse.Listener(on_click=functionOnClick) as listenerObj:
    print("b")
    listenerObj.join()


print("c")
time.sleep(3)

with pynput.mouse.Listener(on_click=functionOnClick) as listenerObj:
    print("d")
    listenerObj.join()

print("e")