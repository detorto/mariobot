import threading
import copy
from PyQt4.Qt import *
from PyQt4 import QtCore
import time
class Capturer(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.lock = threading.Lock()
        self.frame = None

    def set_frame(self,frame):
        self.lock.acquire()
        self.frame = frame
        self.lock.release()

    def run(self):
        while(True):
            #asking main window for screenshot, becouse of QT (grab screen must be called from same thread as GUI)
            self.emit(SIGNAL("needscreen"),[self.set_frame, self.rect])
            time.sleep(0.01)

    def __del__(self):
        self.wait()

    def start_capture(self, rect):
        self.rect = rect
        self.start()

    def stop_capture(self):
        pass

    def get_last_frame_pil(self):
        self.lock.acquire()
        f = copy.copy(self.frame)
        self.lock.release()
        return f

    def get_last_frame_bytestring(self):
        self.lock.acquire()
        f = self.frame.bits().asstring(self.frame.numBytes())
        self.lock.release()
        return f