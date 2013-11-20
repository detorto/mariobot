from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer,GaussianLayer
from pybrain.structure import FeedForwardNetwork, RecurrentNetwork
from pybrain.structure import FullConnection
import Image
import sys
from Utils import crop_rect
import time

import ImageDraw


import cv2
import numpy
import numpy as np
import itertools
def pil2cv(pilframe):
    open_cv_image = numpy.array(pilframe)
    try:
        return open_cv_image[:, :, :].copy()
    except:
           return open_cv_image[:, :].copy()


def cv2pil(cvframe):
    #cv2_im = cv2.cvtColor(cvframe,cv2.COLOR_BGR2RGB)
    return Image.fromarray(cvframe)

class PlayerDetectionNet:

        lk_params = dict( winSize  = (10, 10),
                              maxLevel = 5,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        feature_params = dict( maxCorners = 1000,
                                   qualityLevel = 0.3,
                                   minDistance = 3,
                                   blockSize = 2)

        def input_image_size(self):
            return (64,64)

        def __init__(self):
            #self.template = cv2.imread("./train_sets/tmach/template.png")
            #self.template = self.template - cv2.erode(self.template, None)
            self.new_pts = None
            self.def_pts = None
            self.prev_frame = None
            self.bb = None
            self.old_pts = None
            pass

        def detect_player(self,frame):

            #cvimg = pil2cv(frame)
            #cvimg = cv2.cvtColor(cvimg,cv2.COLOR_BGR2GRAY)
            #cvimg = cvimg - cv2.erode(cvimg,None)

            #match = cv2.matchTemplate(cvimg,self.template,cv2.TM_CCOEFF_NORMED)
            #mn,mx,mnLoc,mxLoc = cv2.minMaxLoc(match)

            #MaxPx,MaxPy = mxLoc

            #trows,tcols = (32,32)
            #return [(MaxPx,MaxPy,tcols,trows)]
            bb = self.bb
            f = frame.crop((bb[0],bb[1],bb[0]+bb[2],bb[1]+bb[3]))
            #ff.show()
            #sys.exit()
            img1 = pil2cv(f)#cv2pil(rcv1).crop((mxLoc[0]-32,mxLoc[1]-32,mxLoc[0]+32,mxLoc[1]+32)))
            g = cv2.cvtColor(img1, cv2.cv.CV_BGR2GRAY) # get grayscale image
            g = g - cv2.erode(g,None);
            pt = cv2.goodFeaturesToTrack(g, **self.feature_params)
            # pt is for cropped image. add x, y in each point.
            try:
                len(pt)
            except:

                self.prev_frame = frame

                self.bb = self.predictBB(bb,self.old_pts, self.new_pts,frame)
                self.old_pts = self.new_pts

                return None
            for i in xrange(len(pt)):
                pt[i][0][0] = pt[i][0][0]+bb[0]
                pt[i][0][1] = pt[i][0][1]+bb[1]

            self.p0 = np.float32(pt).reshape(-1, 1, 2)

            cf = frame;
            if self.prev_frame:
                pf = self.prev_frame
            else:
                pf = cf

            newg = pil2cv(cf)
            oldg =  pil2cv(pf)

            newg = cv2.cvtColor(newg, cv2.cv.CV_BGR2GRAY)
            oldg = cv2.cvtColor(oldg, cv2.cv.CV_BGR2GRAY)

            newg = newg - cv2.erode(newg,None);
            oldg = oldg - cv2.erode(oldg,None);

            #p0 = np.float32(pt).reshape(-1, 1, 2)

            # For Forward-Backward Error method
            # using calcOpticalFlowPyrLK on both image frames
            # with corresponding tracking points

            p1, st, err = cv2.calcOpticalFlowPyrLK(oldg, newg, self.p0,
                                                   None, **self.lk_params)
            p0r, st, err = cv2.calcOpticalFlowPyrLK(newg, oldg, p1,
                                                   None, **self.lk_params)
            d = abs(self.p0-p0r).reshape(-1, 2).max(-1)
            good = d
            self.new_pts = []
            #self.old_pts = self.def_pts
            #print self.old_pts
            for pts, val in itertools.izip(p1, good):
                if val:
                    # points using forward-backward error
                    self.new_pts.append([pts[0][0], pts[0][1]])

            self.prev_frame = frame

            self.bb = self.predictBB(bb,self.old_pts, self.new_pts,frame)
            self.old_pts = self.new_pts


            return (self.bb[0],self.bb[1],self.bb[2],self.bb[3])
        def show_t(self):
            pass#self.template.show()

        def predictBB(self,bb0, pt0, pt1,frame):
            try:
                if not pt0:
                    pt0 = pt1

                cvimg = pil2cv(frame)
                cvimg = cv2.cvtColor(cvimg,cv2.COLOR_BGR2GRAY)
                self.template = cv2.cvtColor(self.template,cv2.COLOR_BGR2GRAY)
                cvimg = cvimg - cv2.erode(cvimg,None)
                self.template = self.template - cv2.erode(self.template,None)

                match = cv2.matchTemplate(cvimg,self.template,cv2.TM_CCOEFF_NORMED)
                mn,mx,mnLoc,mxLoc = cv2.minMaxLoc(match)

                cv2pil(match).show()
                sys.exit()

                dx=[]
                dy=[]
                for p1, p2 in itertools.izip(pt0, pt1):
                    dx.append(p2[0]-p1[0])
                    dy.append(p2[1]-p1[1])
                if not dx or not dy:
                    return bb0
                cen_dx = round(sum(dx)/len(dx))
                cen_dy = round(sum(dy)/len(dy))
                print cen_dx, cen_dy,
                print "shift"
                bb = [int(bb0[0]+cen_dx), int(bb0[1]+cen_dy), int(bb0[2]), int(bb0[3])]
                if bb[0] <= 0:
                    bb[0] = 1
                if bb[1] <= 0:
                    bb[1] = 1
                return bb
            except:
                print "Ololo err"
                return bb0


        def find_player_template(self, left_frames, right_frames):


            lcv1 = pil2cv(left_frames[0])
            rcv1 = pil2cv(right_frames[0])

            lcv2 = pil2cv(left_frames[1])
            rcv2 = pil2cv(right_frames[1])

            lcv1 = lcv1 - cv2.erode(lcv1,None);
            rcv1 = rcv1 - cv2.erode(rcv1,None);

            lcv2 = lcv2 - cv2.erode(lcv2,None);
            rcv2 = rcv2 - cv2.erode(rcv2,None);

            diff1 = lcv1-lcv2
            diff2 = rcv1-rcv2

            mdiff = diff1-diff2

            #mdiff = cv2.blur(mdiff,(5,5),cv2.BORDER_WRAP)
            mdiff = cv2.cvtColor(mdiff,cv2.COLOR_BGR2GRAY)

            median_blur = cv2.medianBlur(mdiff,15)
            #mdiff = cv.adaptiveThreshold(mdiff,255,1,1,11,2)
            #cv2pil(diff1).show()
            #cv2pimedian_blur = cv2.medianBlur(img,i)l(diff2).show()
            #cv2pil(mdiff).show()

            #mdiff = cv2.blur(mdiff,(5,5),0);

            #cv2pil(median_blur).show()

            mn,mx,mnLoc,mxLoc = cv2.minMaxLoc(median_blur)
            print "MnLock: ", mxLoc
            #for size in xrange(2,32,2):
            #    print pil2cv(cv2pil(mdiff).crop((mxLoc[0]-size,mxLoc[1]-size,mxLoc[0]+size,mxLoc[1]+size))).mean()


            self.template = pil2cv(left_frames[0].crop((mxLoc[0]-32,mxLoc[1]-16,mxLoc[0]+32,mxLoc[1]+32)))#cv2pil(rcv1).crop((mxLoc[0]-32,mxLoc[1]-32,mxLoc[0]+32,mxLoc[1]+32)))
            cv2pil(self.template).show()

            self.bb = (mxLoc[0]-32,mxLoc[1]-16,32,32)

            return 1


        def train_on_dataset(self, dataset, max_epochs = 12):
            #trainer = BackpropTrainer(self.net, dataset=dataset, learningrate=0.01, momentum=0.04, verbose=True, weightdecay=0.01)
            #trainer.trainUntilConvergence(maxEpochs=max_epochs, verbose=True)#, continueEpochs, validationProportion);
            #error = trainer.train()

            #NetworkWriter.writeToFile(self.net, ("./network_%d.xml")%(time.time()))
            pass
            return 0
