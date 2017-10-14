import pyxhook
import time
import actions
import public

PressedKeys = list()
running = True


class KeyBind:
    keys = tuple()
    action = ...

    def __init__(self, keys, action):
        self.keys = keys
        self.action = action


Actions = actions.Actions()
Mappings = (KeyBind(('Alt', 'x'), Actions.kill),
            KeyBind(('Control', 'Return'), Actions.bullet))


def filterKey(key):
    return key.replace('_L', '').replace('_R', '')


def KeyDown(event):
    PressedKeys.append(filterKey(event.Key))
    for mapping in Mappings:
        if all([key in PressedKeys for key in mapping.keys]):
            mapping.action()


def KeyUp(event):
    try:
        PressedKeys.remove(filterKey(event.Key))
    except ValueError:
        pass


def start():
    hookman = pyxhook.HookManager()
    hookman.KeyDown = KeyDown
    hookman.KeyUp = KeyUp
    hookman.HookKeyboard()
    hookman.start()

    while Actions.running:
        time.sleep(0.1)

    hookman.cancel()

    if not public.documentModified:
        public.LatexDoc.undoChanges()
