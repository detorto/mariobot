import copy
import time
import sys
#import PIL
#from PIL

from PyQt4.Qt import *
from PyQt4 import QtCore

import Image, ImageChops
from NeuralNets import PlayerDetectionNet

from Utils import pil_image, crop_rect
class MyAI(QObject):

    def __init__(self,player_detection_netclass = PlayerDetectionNet):
        QObject.__init__(self)
        self.player_detection_net = player_detection_netclass()

    def detect_player(self,frame):
        size = frame.size

        net_input_size = self.player_detection_net.input_image_size();
        maximum_answer = 0;
        mx,my = 0,0
        step = (net_input_size[0]/2,net_input_size[1]/2);

        for x in range(0,size[0]-net_input_size[0],step[0]):
            for y in range(0,size[1]-net_input_size[1],step[1]):

                rect = crop_rect((x,y),net_input_size)
                input_image = frame.crop(rect);

                a = self.player_detection_net.activate(input_image.tostring())
                if a > maximum_answer:
                   mx = x
                   my = y
                   maximum_answer = a;
                print x,y
        return (mx,my)+net_input_size;

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
       player_rect = self.detect_player(frame)
       return {"info":{"player_rect":player_rect}}
       #except:
        #   pass;





    def get_player_detection_net(self):
    	return self.player_detection_net



