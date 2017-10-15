import pyxhook
import time
import actions
import public as pub

PressedKeys = set()
pub.running = True


class KeyBind:
    def __init__(self, keys, action):
        self.keys = keys
        self.action = action


pub.Actions = actions.Actions()
Mappings = (KeyBind(('Control', 'x'), pub.Actions.kill),
            KeyBind(('Control', 'Return'), pub.Actions.bullet_factory(major=True)),
            KeyBind(('Shift', 'Return'), pub.Actions.bullet_factory(major=False)),
            KeyBind(('Alt', 'd'), pub.Actions.delete_factory(major=False)),
            KeyBind(('Alt', 'D'), pub.Actions.delete_factory(major=True)),
            KeyBind(('Alt', 'S'), pub.Actions.toggleDateCheck))


def filterKey(key):
    return key.replace('_L', '').replace('_R', '')


def KeyDown(event):
    PressedKeys.add(filterKey(event.Key))
    for mapping in Mappings:
        if all([key in PressedKeys for key in mapping.keys]):
            mapping.action()


def KeyUp(event):
    try:
        PressedKeys.remove(filterKey(event.Key))
    except KeyError:
        pass


def start():
    hookman = pyxhook.HookManager()
    hookman.KeyDown = KeyDown
    hookman.KeyUp = KeyUp
    hookman.HookKeyboard()
    hookman.start()

    pub.running = True
    while pub.running:
        time.sleep(0.1)

    hookman.cancel()
