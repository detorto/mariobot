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

import cv2
import numpy as np
import numpy
import itertools

def pil2cv(pilframe):
    open_cv_image = numpy.array(pilframe)
    try:
        return open_cv_image[:, :, ::-1].copy()
    except:
           return open_cv_image[:, :].copy()


def cv2pil(cvframe):
    #cv2_im = cv2.cvtColor(cvframe,cv2.COLOR_BGR2RGB)
    return Image.fromarray(cvframe)

class AIManager(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.lock = threading.Lock();
        self.diff_show = False;
        self.current_frame = None;
        self.prev_frame = None;
        self.working = True
        self.ai_process = True

    def log(self,string):
        self.emit(SIGNAL("log"),string)

    def draw_rect(self,surf,rect,tpe):
        if tpe == "POS":
            color = (0,255,0)
        if tpe == "NEG":
            color = (255,0,0)
        if tpe == "AI":
            color = (255,255,255)
        pygame.draw.rect(surf,color,rect,1)

    def init_test_screen(self):
        pygame.init()
        self.size = self.capturer.get_image_size()
        self.winscreen = pygame.display.set_mode(self.size)
        self.log("Diag screen inited (%d, %d)" % self.size)

    def process_diag_screen(self):
        fr = pygame.image.frombuffer(self.diag_frame,self.size,"RGB")
       # print self.ai_answer
        try:
            fr = pygame.image.frombuffer(self.ai_answer["info"]["diag"].tostring(),self.size,"RGB")
        except:
            pass

        surf = fr;

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.working = False;
        try:
            self.draw_rect(surf, self.ai_answer["info"]["player_rect"][0] , "POS")
            self.draw_rect(surf, self.ai_answer["info"]["player_rect"][1] , "NEG")
        except:
            pass

        #if self.ai.player_detection_net.new_pts != None:
         #   for p in self.ai.player_detection_net.new_pts:
          #      pygame.draw.circle(surf,(255,0,255),tuple(p),4);

        #if self.ai.player_detection_net.bb:
         #   pygame.draw.rect(surf,(255,0,255),self.ai.player_detection_net.bb,2)



        self.winscreen.blit(surf,(0,0))
        pygame.display.flip()

    def set_capturer(self, capturer):
        self.capturer = capturer

    def set_controller(self, controller):
        self.controller = controller

    def set_ai(self, ai):
        self.ai = ai

    def toogle_diff_show(self):
        self.diff_show = not self.diff_show;
        self.log("Diff show toogled, state %s"%self.diff_show)

    def toogle_ai_info(self):
        self.ai_process = not self.ai_process

    def run(self):
        time.sleep(5)
        self.init_test_screen()

        while(self.working):
            self.current_frame = self.capturer.get_last_frame_bytestring()

            if not self.current_frame:
                continue;

            if self.ai_process:
                self.do_analize()
                self.do_actions()


            self.diag_frame = Image.fromstring("RGB", self.size, self.current_frame);

            if self.diff_show:
                #self.diag_frame  = ImageChops.difference(Image.fromstring("RGB", self.size, self.current_frame),
                cvimg = pil2cv(self.diag_frame)
                cvimg = cv2.cvtColor(cvimg,cv2.COLOR_BGR2GRAY)
                cvimg = cvimg - cv2.erode(cvimg,None)
                cvimg = cv2.cvtColor(cvimg,cv2.COLOR_GRAY2BGR)
                self.diag_frame = cv2pil(cvimg)                        #Image.fromstring("RGB", self.size, self.prev_frame))

            #do somthing with diag_image
            self.diag_frame = self.diag_frame.tostring();

            self.prev_frame=self.current_frame;

            self.process_diag_screen()

        pygame.display.quit()

    def do_analize(self):
        state = {"current_frame_pil":Image.fromstring("RGB", self.size, self.current_frame)}

        self.ai_answer = self.ai.analize_state(state)

    def do_actions(self):
        pass
        if self.ai_answer:
            pass


