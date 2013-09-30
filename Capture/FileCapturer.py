import time
import sys
from PyQt4.Qt import *
from PyQt4 import QtCore
import Image #PIL
from .Capturer import Capturer

import os#

class FileCapturer(Capturer):

    def __init__(self,filepath):
        self.filepath = filepath

    def get_count(self):
        return self.count

    def get_folder(self):
        return self.filepath

    def start_capture(self,filepath = None):
        #ask here for files folder
        self.files = [self.filepath+f for f in os.listdir(self.filepath) if f.endswith('.png') or  f.endswith('.jpg')]
        self.image_size = Image.open(self.files[0]).size
        self.count = len(self.files)

    def log(self,string):
        self.emit(SIGNAL("log"),string)

    def get_last_frame_pil(self):
        if not self.files:
            return None
        return Image.open(self.files.pop(0))

    def get_last_frame_bytestring(self):
        if not self.files:
            return None
        im = Image.open(self.files.pop(0))
        return im.convert("RGB").tostring()

    def get_image_size(self):
        return self.image_size
