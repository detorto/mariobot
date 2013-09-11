import sys, time

class controll:
    send_message = 0
    os_version = 0
    
    def __init__(self):
        self.send_message = self.getSendMessageFunc()
        
    def getSendMessageFunc(self):
        self.os_version = sys.platform
        if self.os_version == "win32":
            import win32api, win32con
            return win32api.keybd_event
        else:
            import pyatspi
            return pyatspi.Registry.generateKeyboardEvent #I'm not sure 
        
    def jump(self):
        if self.os_version == "win32":
            self.send_message(0x20,0,0x0001,0)
        else:
            pass
        
    def left_run(self):
        if self.os_version == "win32":
            self.send_message(0x25,0,0x0001,0)
        else:
            pass
        
    def left_run(self):
        if self.os_version == "win32":
            self.send_message(0x27,0,0x0001,0)
        else:
            pass
       
