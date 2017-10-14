import pyxhook
import time

PressedKeys = list()


def KeyDown(event):
    PressedKeys.append(event.Key)
    print(PressedKeys)


def KeyUp(event):
    try:
        PressedKeys.remove(event.Key)
    except ValueError:
        pass


def start():
    hookman = pyxhook.HookManager()
    hookman.KeyDown = KeyDown
    hookman.KeyUp = KeyUp
    hookman.HookKeyboard()
    hookman.start()

    running = True
    while running:
        time.sleep(0.1)

    hookman.cancel()
