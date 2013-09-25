import threading
import copy
from PyQt4.Qt import *
from PyQt4 import QtCore
import time
import pygame
import sys
#import PIL
#from PIL 
import Image, ImageChops
class MyAI(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.lock = threading.Lock();
        self.diff_show = False;
    def log(self,string):
        self.emit(SIGNAL("log"),string)
    
    def init_test_screen(self):
        pygame.init()
        self.size = (self.capturer.get_rect().width(),self.capturer.get_rect().height())
        self.winscreen = pygame.display.set_mode(self.size)
        self.log("Diag screen inited (%d, %d)" % self.size)

    def process_diag_screen(self):
        surf = pygame.image.frombuffer(self.diag_frame,self.size,"RGB")

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            #self.winscreen.fill(0)
        self.winscreen.blit(surf,(0,0))
        pygame.display.flip()

    def set_capturer(self, capturer):
        self.capturer = capturer

    def set_controller(self, controller):
        self.controller = controller

    def start_ai(self):
        self.start()

    def stop_ai(self):
        pass

    def toogle_diff_show(self):
        self.diff_show = not self.diff_show;
        self.log("Diff show toogled, state %s"%self.diff_show)
        


    def run(self):
        self.init_test_screen()

        while(True):
            self.current_frame = self.capturer.get_last_frame_bytestring()

            if not self.current_frame:
                continue;

            self.do_analize()

            self.diag_frame = Image.fromstring("RGB", self.size, self.current_frame);
            
            if self.diff_show:
                self.diag_frame  = ImageChops.difference(Image.fromstring("RGB", self.size, self.current_frame),  
                                                        Image.fromstring("RGB", self.size, self.prew_frame))
            
            #do somthing with diag_image
            self.diag_frame = self.diag_frame.tostring();
            
            self.prew_frame=self.current_frame;
            self.process_diag_screen()

    def do_analize(self):
        #here must be conwersion of image and calls to analise it.
        #image is QImage instanse, with inverted RGB.
        pass

    def detect_player(self, frame):
        self.current_frame = frame;
        #here must be player detection
        return QRect(30,20,30+50,20+50)
    
    def player_correct(self,correctRect):
        #this called in training mode, 
        #correctRect are the rea coordinates on current frame
        pass

    def save_state(self):
        #in training mode, save trained state to file
        pass

