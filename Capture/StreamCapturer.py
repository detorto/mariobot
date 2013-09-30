import threading
import copy

from PyQt4.Qt import *
from PyQt4 import QtCore

import time
import sys
import gtk
from .Capturer import Capturer
import Image

DEFAULT_IMAGE_SIZE = (512, 448)

PLATFORM = sys.platform

def make_screenshot_linux(capture_rect,image_size):
        w = gtk.gdk.get_default_root_window()
        sz = (capture_rect[2]+(capture_rect[2] % 2),capture_rect[3])
        #only even alloved
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),capture_rect[0],capture_rect[1],0,0,sz[0],sz[1])
        if (pb == None):
            return False
        else:
            width,height = sz[0],sz[1]

            #filename = "/home/torto/projects/mariobot/train_sets/default/%d.png"%(count);

            #da+=1
            #if da == 10:
            #    Image.fromstring("RGB",(width,height),pb.get_pixels()).resize(DEFAULT_IMAGE_SIZE).save(filename);
            #    count+=1;
            #    da=0
            #    print "SavedScreenshot"

            return Image.fromstring("RGB",(width,height),pb.get_pixels()).resize(image_size)

def make_screen_shot(capture_rect,image_size):
    if PLATFORM == "win32":
        return make_screenshot_windows(capture_rect, image_size)
    else:
        return make_screenshot_linux(capture_rect, image_size)

class CapturerThread(QtCore.QThread):
    def __init__(self,image_size):
        QtCore.QThread.__init__(self)
        self.lock = threading.Lock()
        self.frame = None
        self.image_size = image_size
        self.saving_on =  False;
        self.save_parity = 100;

    def set_save_dir(self, path):
        self.save_path  = path;

    def set_save_parity(self, parity):
        self.save_parity  = parity;

    def toogle_saving(self):
        self.saving_on = not self.saving_on;
        self.log("Frame saving is %s" % (str(self.saving_on)))

    def set_logger_callback(self,callback):
        self.log = callback

    def set_frame(self,frame):
        self.lock.acquire()
        self.frame = frame
        self.lock.release()

    def run(self):
        frames_count = 0;
        frames_saved = 0;
        while(True):
            gtk.threads_enter()
            frame = make_screen_shot(self.capture_rect, self.image_size)
            gtk.threads_leave()

            self.set_frame(frame)

            frames_count += 1;

            if frames_count % self.save_parity == 0 and self.saving_on:
                self.get_last_frame_pil().save(self.save_path+"%d.png"%(time.time()))
                frames_saved +=1;
                self.log("Frames saved: %d"%(frames_saved))

    def __del__(self):
        self.wait()

    def start_capture(self, capture_rect):
        self.capture_rect = capture_rect
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
            f = self.frame.tostring()
        self.lock.release()
        return f

    def get_image_size(self):
        return self.image_size#self.rect


class CapturerWindow(QDialog):

    def __init__(self, image_size):

        QDialog.__init__(self)
        self.setGeometry(QRect(0, 0,image_size[0],image_size[1]))

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

        self.rect = (x,y,w,h)

    def get_capture_rect(self):
        return self.rect

class StreamCapturer(QObject,Capturer):

    def __init__(self, image_size):
        QObject.__init__(self)
        gtk.gdk.threads_init()

        self.image_size = image_size

        self.capturer_window = CapturerWindow(self.image_size)
        self.capturer_thread = CapturerThread(self.image_size)
        self.capturer_thread.set_logger_callback(self.log)
    def toogle_saving_images(self):
        self.capturer_thread.toogle_saving()

    def save_images_dir(self,path):
        self.capturer_thread.set_save_dir(path)

    def save_images_parity(self,parity):
        self.capturer_thread.set_save_parity(parity)

    def start_capture(self):

        self.capturer_window.exec_()

        self.capturer_thread.start_capture(self.capturer_window.get_capture_rect())

        r = self.capturer_window.get_capture_rect()
        log_msg =  "Capturer ready, rect: (%d,%d,%d,%d)"%(r)
        self.log(log_msg)

    def log(self,string):
        self.emit(SIGNAL("log"),string)

    def get_last_frame_pil(self):
        return self.capturer_thread.get_last_frame_pil();

    def get_last_frame_bytestring(self):
        return self.capturer_thread.get_last_frame_bytestring();

    def get_capture_rect(self):
        self.capturer_window.get_capture_rect()

    def get_image_size(self):
        return self.capturer_thread.get_image_size()