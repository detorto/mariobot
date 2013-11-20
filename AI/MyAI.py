import copy
import time
import sys
import numpy
#import PIL
#from PIL
import ImageChops
from Controll import Controller

from PyQt4.Qt import *
from PyQt4 import QtCore

import Image, ImageChops
from NeuralNets import PlayerDetectionNet

from Utils import pil_image, crop_rect

def pil2cv(pilframe):
    open_cv_image = numpy.array(pilframe)
    return open_cv_image[:, :, ::-1].copy()
class MyAI(QObject):

    player_detected = False;

    def __init__(self,player_detection_netclass = PlayerDetectionNet):
        QObject.__init__(self)
        self.player_detection_net = player_detection_netclass()
        self.analize_proc = self.state_select_proc

        self.frames = {"left_run": [], "right_run": [], "jump":None}
        self.iters = 0

    def player_detection_proc(self,frame):

      self.r = None
      if self.iters == 0:
        Controller.rigth_run();

      if self.iters == 1:
          Controller.rigth_run();
          self.frames["right_run"].append(frame);

      if self.iters == 2:
          Controller.left_run();
          self.frames["right_run"].append(frame);

      if self.iters == 3:
          Controller.left_run();
          self.frames["left_run"].append(frame);

      if self.iters == 4:
          self.frames["left_run"].append(frame);

      self.iters+=1
      time.sleep(0.1)

      if not self.frames["left_run"] or not self.frames["right_run"]:
        return {"anus":2}

      if not self.player_detected and self.iters > 4:
        self.r =  self.player_detection_net.find_player_template( self.frames["left_run"], self.frames["right_run"] )

      if self.r:
           self.player_detected = True;
           self.player_detection_net.show_t();

           self.analize_proc = self.state_select_proc
      print "returning pr: ",self.r
      return {"player_rect":[self.r]}

    def main_proc(self,frame):
      Controller.rigth_run();

      r = self.player_detection_net.detect_player(frame)
      if not r:
        Controller.jump()
      print "returning pr2: ",r
      return {"player_rect":[r,]}

    def state_select_proc(self,frame):
      print self.player_detected
      if not self.player_detected:
        self.analize_proc = self.player_detection_proc;
        return self.analize_proc(frame)
      else:
        self.analize_proc = self.main_proc
        return self.analize_proc(frame)

    def analize_state(self,state):
       frame = None;
       try:
           frame = state["current_frame_pil"];
       except:
           pass

       if not frame:
           print "No frame on input!"
           return None
      # print "frame got"
       r = None
       #try:
       r = self.analize_proc(frame)
       #except:
        #  pass

       return {"info":r}
       #except:
        #   pass;


    def get_player_detection_net(self):
    	return self.player_detection_net



