import copy
import time
import sys
#import PIL
#from PIL

from PyQt4.Qt import *
from PyQt4 import QtCore

import Image, ImageChops
from NeuralNets import PlayerDetectionNet


class MyAI(QObject):

    def __init__(self,player_detection_netclass = PlayerDetectionNet):
    	QObject.__init__(self)
        self.player_detection_net = player_detection_netclass()

    def analize_state(self,state):
        return {"info":{"player_rect":(0,0,100,100)}}

    def get_player_detection_net(self):
    	return self.player_detection_net



