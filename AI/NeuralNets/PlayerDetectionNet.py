from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer,GaussianLayer
from pybrain.structure import FeedForwardNetwork, RecurrentNetwork
from pybrain.structure import FullConnection
import Image
from Utils import crop_rect
import time

import cv2
import numpy

def pil2cv(pilframe):
    open_cv_image = numpy.array(pilframe)
    return open_cv_image[:, :, ::-1].copy()

def cv2pil(cvframe):
    #cv2_im = cv2.cvtColor(cvframe,cv2.COLOR_BGR2RGB)
    return Image.fromarray(cvframe)

class PlayerDetectionNet:

        def input_image_size(self):
            return (64,64)

        def __init__(self):
            self.template = cv2.imread("./train_sets/tmach/template.png")
            self.template = self.template - cv2.erode(self.template, None)

        def detect_player(self,frame):
            cvimg = pil2cv(frame)
            cvimg = cvimg - cv2.erode(cvimg,None)

            match = cv2.matchTemplate(cvimg,self.template,cv2.TM_CCOEFF_NORMED)
            mn,mx,mnLoc,mxLoc = cv2.minMaxLoc(match)

            MaxPx,MaxPy = mxLoc

            trows,tcols = (32,32)
            return [(MaxPx,MaxPy,tcols,trows)]

        def find_player_template(self,diff):
            cvim = cv2.cvtColor(pil2cv(diff), cv2.COLOR_BGR2GRAY)
            cvim = cv2.adaptiveThreshold(cvim,256,1,1,11,2)

            mn,mx,mnLoc,mxLoc = cv2.minMaxLoc(cvim)
            cr = (mxLoc[0]-16,mxLoc[1]-16)+(32,32)
            self.template = pil2cv(diff.crop((mxLoc[0]-16,mxLoc[1]-16)+(32,32)))

            self.template = self.template - cv2.erode(self.template, None)
            cv2pil(self.template).show()

            return (mxLoc[0]-16,mxLoc[1]-16)+(32,32)


        def train_on_dataset(self, dataset, max_epochs = 12):
            #trainer = BackpropTrainer(self.net, dataset=dataset, learningrate=0.01, momentum=0.04, verbose=True, weightdecay=0.01)
            #trainer.trainUntilConvergence(maxEpochs=max_epochs, verbose=True)#, continueEpochs, validationProportion);
            #error = trainer.train()

            #NetworkWriter.writeToFile(self.net, ("./network_%d.xml")%(time.time()))
            pass
            return 0
