import pyxhook
import time
import actions
import public

PressedKeys = list()
public.running = True
public.modified = False


class KeyBind:
    keys = tuple()
    action = ...

    def __init__(self, keys, action):
        self.keys = keys
        self.action = action


Mappings = (KeyBind(('Alt', 'x'), actions.kill),
            KeyBind(('Control', 'Return'), actions.bullet_factory(primary=True)),
            KeyBind(('Shift', 'Return'), actions.bullet_factory(primary=False)))


def filterKey(key):
    return key.replace('_L', '').replace('_R', '')


def KeyDown(event):
    PressedKeys.append(filterKey(event.Key))
    for mapping in Mappings:
        if all([key in PressedKeys for key in mapping.keys]):
            mapping.action()
            if mapping.action != actions.kill:
                public.modified = True


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

    public.running = True
    while public.running:
        time.sleep(0.1)

    hookman.cancel()

    if not public.modified:
        public.LatexDoc.undoChanges()
