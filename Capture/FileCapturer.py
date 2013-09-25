import time
import sys
from PyQt4.Qt import *
from PyQt4 import QtCore
import Image #PIL

import os

class FileCapturer:

    def __init__(self):        
        self.a = 0;
        pass

    def start_capture(self):
        #ask here for files folder
        print ""
        path = "./train_sets/default/"#raw_input("Dataset dir: ")
        self.files = [path+f for f in os.listdir(path) if f.endswith('.png') or  f.endswith('.jpg')]
        print self.files
        self.size = Image.open(self.files[0]).size

    
    def log(self,string):
        self.emit(SIGNAL("log"),string)

    def get_last_frame_pil(self):
        #firstand next
        return Image.open(self.files.pop(0))

    def get_last_frame_bytestring(self):
    	if not self.files:
    		return None
    	im = Image.open(self.files.pop(0))
        return im.convert("RGB").tostring()
    
    def get_rect(self):
        return QRect(0,0,self.size[0],self.size[1])