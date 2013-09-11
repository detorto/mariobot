import sys

PLATFORM = sys.platform

class KeyboardLayout:
    class Action:
        ACTION_JUMP = "jump"
        ACTION_LEFT_RUN = "left"
        ACTION_RIGHT_RUN = "right"

    def get_default_key_map(self):
        if PLATFORM == "win32":
            return {self.Action.ACTION_JUMP:0x20, 
                        self.Action.ACTION_RIGHT_RUN:0x27,
                        self.Action.ACTION_RIGHT_RUN:0x25 }
        else:
            return {self.Action.ACTION_JUMP:0x20, 
                        self.Action.ACTION_RIGHT_RUN:0x27,
                        self.Action.ACTION_RIGHT_RUN:0x25 }

if PLATFORM == "win32":
    import win32api, win32con
    def windows_keyboard_event(event):
        win32api.keybd_event(event,0x0001,0);
else:
    import pyatspi
    def linux_keyboard_event(event):
        print "lin keyboard event %s" % event;

def getKeyboardEventFunc():
    if PLATFORM == "win32":
        return windows_keyboard_event;
    else:
        return linux_keyboard_event;

class Controller:

    def __init__(self):
        self.send_message = getKeyboardEventFunc()
        self.keymap = KeyboardLayout().get_default_key_map();

    def jump(self):
            self.send_message(self.keymap[KeyboardLayout.Action.ACTION_JUMP])

    def left_run(self):
        self.send_message(self.keymap[KeyboardLayout.Action.ACTION_LEFT_RUN])
    
    def rigth_run(self):
        self.send_message(self.keymap[KeyboardLayout.Action.ACTION_RIGHT_RUN])
       
