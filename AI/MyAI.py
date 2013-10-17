import copy
import time
import sys
#import PIL
#from PIL
import ImageChops
from Controll import Controller

from PyQt4.Qt import *
from PyQt4 import QtCore

import Image, ImageChops
from NeuralNets import PlayerDetectionNet

from Utils import pil_image, crop_rect

class MyAI(QObject):

    player_detected = False;

    def __init__(self,player_detection_netclass = PlayerDetectionNet):
        QObject.__init__(self)
        self.player_detection_net = player_detection_netclass()
        self.analize_proc = self.state_select_proc

        self.frames = {"left_run": None, "right_run": None, "jump":None}
        self.iters = 0

    def player_detection_proc(self,frame):

      if self.iters % 3 == 0:
        Controller.rigth_run();
        print "RR"
        self.frames["jump"] = frame;

      elif self.iters % 3 == 1:
        Controller.left_run();
        print "LR"
        self.frames["right_run"] = frame;
      else:
        #Controller.jump();
        print "JP"
        self.frames["left_run"] = frame;

      self.iters+=1

      if not self.frames["left_run"] or not self.frames["right_run"] or not self.frames["jump"]:
        return

      self.diff1  = ImageChops.difference(self.frames["left_run"],self.frames["right_run"])
      r = (0,0,0,0)
      r =  self.player_detection_net.find_player_template(self.diff1)
      self.player_detected = True;
      self.analize_proc = self.state_select_proc

      return {"player_rect":[r],"diag":self.diff1}

    def main_proc(self,frame):
      r = self.player_detection_net.detect_player(frame)
      return {"player_rect":r}



    def state_select_proc(self,frame):
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
       print "frame got"
       r = None
       try:
          r = self.analize_proc(frame)
       except:
          pass

       return {"info":r}
       #except:
        #   pass;


    def get_player_detection_net(self):
    	return self.player_detection_net



