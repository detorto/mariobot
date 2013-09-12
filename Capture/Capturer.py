import threading
import copy
from PyQt4.Qt import *
from PyQt4 import QtCore
import time

class CapturerThread(QtCore.QThread):
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

    def dict(self):
        return self.__dict__;

import sys
from PyQt4.Qt import *
from PyQt4 import QtCore
import time

class CapturerWindow(QMainWindow):
  
    def __init__(self, *args):

        QMainWindow.__init__(self, *args)
        self.setGeometry(QRect(0, 0, 300, 300))
        #making window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        self.capturer_thread = CapturerThread()
        self.connect(self.capturer_thread,QtCore.SIGNAL('needscreen'), self.capture_frame)

        #self.statusbar = self.statusBar()
        #self.statusbar.showMessage('Move this window up to the game screen, and close it!')

    def closeEvent(self, event):
        
        
        win_rect = self.geometry()

        x = win_rect.x()
        y = win_rect.y()
        w = win_rect.width()
        h = win_rect.height()

        #win_rect = self.statusbar.geometry()

       # h = h - win_rect.height()
#
        time.sleep(0.2)
        self.capturer_thread.start_capture(QRect(x,y,h,w));
        self.emit(SIGNAL("can_run_ai"))
        #event.accept()
        event.ignore()
        

    def capture_frame(self,data):
        callback = data[0]
        rect = data[1]
        pmap = QPixmap.grabWindow(QApplication.desktop().winId(),rect.x(),rect.y(),rect.width(),rect.height()).toImage().rgbSwapped();
        callback(pmap);

   

class Capturer(QObject):

    def __init__(self):        
        QObject.__init__(self)
        self.win = CapturerWindow()
        self.connect(self.win, SIGNAL("can_run_ai"), self.run_capture )
    def run_capture(self):
        self.emit(SIGNAL("can_run_ai"))
        #self.__dict__ = self.win.capturer_thread.dict()

    def start_capture(self):
        self.thr = QThread();
        self.win.moveToThread(self.thr)
        self.thr.start()
        self.win.show()
       # while(True):
        #    pass

    def set_frame(self,frame):
        return self.win.capturer_thread.set_frame(frame)

    def get_last_frame_pil(self):
        return self.win.capturer_thread.get_last_frame_pil();

    def get_last_frame_bytestring(self):
        return self.win.capturer_thread.get_last_frame_bytestring();
    def get_rect(self):
        return self.win.capturer_thread.rect