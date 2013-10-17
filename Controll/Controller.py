import sys
import time
PLATFORM = sys.platform

class KeyboardLayout:
    class Action:
        ACTION_JUMP = "jump"
        ACTION_LEFT_RUN = "left"
        ACTION_RIGHT_RUN = "right"
        ACTION_SHOOT = "shoot"

    def get_default_key_map(self):
        if PLATFORM == "win32":
            return {    self.Action.ACTION_JUMP:0x20,
                        self.Action.ACTION_RIGHT_RUN:0x27,
                        self.Action.ACTION_RIGHT_RUN:0x25,
                        self.Action.ACTION_SHOOT:0x0D}
        else:
            import uinput
            return {    self.Action.ACTION_JUMP : "t",
                        self.Action.ACTION_RIGHT_RUN : "d",
                        self.Action.ACTION_LEFT_RUN : "a",
                        self.Action.ACTION_SHOOT : ""}

if PLATFORM == "win32":
    import win32api
    def windows_keyboard_event(key, state = 0):
        win32api.keybd_event(event,0x0001,0);
else:
    import uinput
    from subprocess import *
    #device = uinput.Device(KeyboardLayout().get_default_key_map().values())
    def linux_keyboard_event(key, state = 1):
        #time.sleep(1)
        pass
       # device.write(ecodes.EV_KEY,key,1)

    prevkey = None
    def lkeypress(key, state = 1):
        global prevkey

        if prevkey:
            p = Popen(['xte'], stdin=PIPE)
            p.communicate(input="keyup %s\n"%prevkey)

        p = Popen(['xte'], stdin=PIPE)
        if state == 1:
            p.communicate(input="keydown %s\n"%key)
        else:
            p.communicate(input="keyup %s\n"%key)
        prevkey = key


def get_keyboard_event_func():
    if PLATFORM == "win32":
        return windows_keyboard_event;
    else:
        return lkeypress;

send_message = get_keyboard_event_func()
keymap = KeyboardLayout().get_default_key_map();

def jump():
        send_message(keymap[KeyboardLayout.Action.ACTION_JUMP])

def left_run():
        send_message(keymap[KeyboardLayout.Action.ACTION_LEFT_RUN])

def rigth_run():
        send_message(keymap[KeyboardLayout.Action.ACTION_RIGHT_RUN])

def shoot():
        send_message(keymap[KeyboardLayout.Action.ACTION_SHOOT])

