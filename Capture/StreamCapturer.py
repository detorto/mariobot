import threading
import copy

from PyQt4.Qt import *
from PyQt4 import QtCore

import time
import sys
import gtk

import Image #PIL

PLATFORM = sys.platform

def make_screenshot_linux(rect):
        w = gtk.gdk.get_default_root_window()
        sz = (rect.width(),rect.height())
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),rect.x(),rect.y(),0,0,sz[0],sz[1])
        if (pb == None):
            return False
        else:
            width,height = rect.width(),rect.height()
            return Image.fromstring("RGB",(width,height),pb.get_pixels())

def make_screen_shot(rect):
    if PLATFORM == "win32":
        return make_screenshot_windows(rect)
    else:
        return make_screenshot_linux(rect)

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
            gtk.threads_enter()
            frame = make_screen_shot(self.rect)
            gtk.threads_leave()

            self.set_frame(frame)
    
    def __del__(self):
        self.wait()

    def start_capture(self, rect):
        self.rect = rect
        #print rect
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
        f = None
        if self.frame:
            #print self.frame
            f = self.frame.tostring()
        self.lock.release()
        return f

    def get_capturer_rect(self):
        return self.rect


class CapturerWindow(QDialog):
  
    def __init__(self, *args):

        QDialog.__init__(self, *args)
        self.setGeometry(QRect(0, 0, 300, 300))

        #making window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
    def closeEvent(self, event):
        win_rect = self.geometry()

        x = win_rect.x()
        y = win_rect.y()
        w = win_rect.width()
        h = win_rect.height()

        self.rect = QRect(x,y,w,h);   

class StreamCapturer(QObject):

    def __init__(self):        
        QObject.__init__(self)
        self.capturer_window = CapturerWindow()
        self.capturer_thread = CapturerThread()
        gtk.gdk.threads_init()
    
    def start_capture(self):
        #do modal dialog to pick up capturer rect
        self.capturer_window.exec_()
        self.capturer_thread.start_capture(self.capturer_window.rect)
        r = self.get_rect()
        log_msg =  "Capturer ready, rect: (%d,%d,%d,%d)"%(r.x(),r.y(),r.width(),r.height())
        self.log(log_msg)
    
    def log(self,string):
        self.emit(SIGNAL("log"),string)

    def get_last_frame_pil(self):
        return self.capturer_thread.get_last_frame_pil();

    def get_last_frame_bytestring(self):
        return self.capturer_thread.get_last_frame_bytestring();
    
    def get_rect(self):
        return self.capturer_thread.get_capturer_rect()