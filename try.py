from pynput.mouse import Listener

def on_click(x, y, button, pressed):
    print("Mouse clicked")
    print(x, y, button, pressed)
    print("Hello {0}".format("there"))
    Listener.stop()


with Listener(on_click=on_click) as Listener:
    Listener.join()


