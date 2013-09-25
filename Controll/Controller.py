import sys

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
            return {    self.Action.ACTION_JUMP : uinput.KEY_UP, 
                        self.Action.ACTION_RIGHT_RUN : uinput.KEY_RIGHT,
                        self.Action.ACTION_RIGHT_RUN : uinput.KEY_LEFT,
                        self.Action.ACTION_SHOOT : uinput.KEY_SPACE}

if PLATFORM == "win32":
    import win32api
    def windows_keyboard_event(key, state = 0):
        win32api.keybd_event(event,0x0001,0);
else:
    import uinput
    def linux_keyboard_event(key, state = 1):
        device = uinput.Device(KeyboardLayout().get_default_key_map().values())
        device.emit_click(key)
        

def get_keyboard_event_func():
    if PLATFORM == "win32":
        return windows_keyboard_event;
    else:
        return linux_keyboard_event;

class Controller:

    def __init__(self):
        self.send_message = get_keyboard_event_func()
        self.keymap = KeyboardLayout().get_default_key_map();

    def jump(self):
            self.send_message(self.keymap[KeyboardLayout.Action.ACTION_JUMP])

    def left_run(self):
        self.send_message(self.keymap[KeyboardLayout.Action.ACTION_LEFT_RUN])
    
    def rigth_run(self):
        self.send_message(self.keymap[KeyboardLayout.Action.ACTION_RIGHT_RUN])
        
    def shoot(self):
        self.send_message(self.keymap[KeyboardLayout.Action.ACTION_SHOOT])
       
