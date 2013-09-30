import pybrain


import sys
sys.path.append('../')

from Capture import FileCapturer
from pybrain.tools.shortcuts import buildNetwork
import pygame
from PyQt4.Qt import *
from PyQt4 import QtCore
import copy
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.structure import LinearLayer, SigmoidLayer, SoftmaxLayer
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import FullConnection
import ImageFilter
import ImageEnhance
net = buildNetwork(2,4,1)


class PlayerNet:
	pass

class test:


	def init_test_screen(self):
		pygame.init()
		self.size = (512,448)
		self.winscreen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF, 32)
		
	def draw_rect(self,surf,rect,tpe):
		color = (0,255,02,255)
		w=1
		if tpe == "AI":
			color = (255,0,0,255)
			w = 0;
		if tpe == "USR_F":
			w = 0;

		pygame.draw.rect(surf,color,(rect.x(),rect.y(),rect.width(),rect.height()),w)
	t = 0;
	f = 0;
	def detection(self,net,img):
		arr = [ord(x) for x in list(img.tostring())]
		#print arr
		a = net.activate(arr);
		print "corNet: "
		print (id(net))
		print a
		
		if a > 0.5:
			self.t+=1;
			return True;
		else:
			self.f+=1;#return False;
			return False;

	ds = SupervisedDataSet(64*64*3, 1)

	def correction(self,img, answ):
		#self.ds = SupervisedDataSet(64*64*3, 1)
		
		arr = [ord(x) for x in (list(img.tostring()))]
		#if answ == 1:
		#	img.show()
		
		self.ds.addSample(arr, (answ,))


	def run(self):

 		fc = FileCapturer();
		fc.start_capture("../train_sets/points/");
		cellingsize = 64;
		cellingtile = cellingsize/2
	
		
		print "building network...."

		image = fc.get_last_frame_pil();

		#detection here:
		size = image.size
		print size
		ix = size[0]/cellingtile
		iy = size[1]/cellingtile

		self.init_test_screen();
		imcount = 0;
		while imcount >=0:
			image = fc.get_last_frame_pil();
			corrected = False;
			was_lb_pressed = False;
			mx,my = 0,0
			sx,sy = 0,0
			while not corrected:
			
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						corrected = True;
					if event.type == pygame.QUIT: 
						imcount = -1
						corrected = True;

					if event.type == pygame.MOUSEBUTTONDOWN:
							was_lb_pressed = True;
							sx,sy = pygame.mouse.get_pos()
					if event.type == pygame.MOUSEBUTTONUP:
							corrected = True;
							imcount+=1
							pygame.display.set_caption('Image %d from 150'%(imcount))

							was_lb_pressed = False;
							for i in xrange(ix-1):
								for j in xrange(iy-1):
									crp = image.crop((i*cellingtile,j*cellingtile,i*cellingtile+cellingsize,j*cellingtile+cellingsize))
									#crp.show();

									#if self.detection(net,crp):
									#self.draw_rect(surf,QRect((i)*cellingtile,(j)*cellingtile,2*cellingtile,2*cellingtile),"AI");
									print "[%d of %d] [%d of %d]"%(i,ix,j,iy)
									if mx > i*cellingtile and mx < (i+1)*cellingtile and my > (j)*cellingtile and my < (j+1)*cellingtile:
										self.correction(crp,1)
										i=i+2;
										j=j+1;
										crp = image.crop((i*cellingtile,j*cellingtile,i*cellingtile+cellingsize,j*cellingtile+cellingsize))
										self.correction(crp,0)
										#crp.show();
										
									#else:
									#	print "zero corection"
									#	self.correction(crp,0)
										
									#if mx > i*cellingtile and mx < (i+2)*cellingtile and my > (j)*cellingtile and my < (j+2)*cellingtile:
										#this is correct cell
							#for inpt, target in self.ds:
							#	print inpt, target
							#trainer = BackpropTrainer(net, self.ds)
							#print trainer.train()

				if was_lb_pressed:
					mx,my = pygame.mouse.get_pos()

					#wait correction input


				surf = copy.copy(pygame.image.frombuffer(image.tostring(),self.size,"RGB"))
				#self.draw_rect(surf,ai_player_rect,"AI");
				for i in xrange(ix):
					for j in xrange(iy):
						self.draw_rect(surf,QRect(i*cellingtile,j*cellingtile,(i+1)*cellingtile,(j+1)*cellingtile),"USR");
					
						if mx > i*cellingtile and mx < (i+1)*cellingtile and my > (j)*cellingtile and my < (j+1)*cellingtile:
							self.draw_rect(surf,QRect((i)*cellingtile,(j)*cellingtile,2*cellingtile,2*cellingtile),"USR_F");
						

				self.winscreen.fill(0)
				self.winscreen.blit(surf,(0,0))
				pygame.display.flip()
		pygame.quit()
		
		

		print "building network"
		net = FeedForwardNetwork()
		inLayer = LinearLayer(64*64*3)
		hiddenLayer1 = SigmoidLayer(100)
		hiddenLayer2 = SigmoidLayer(50)
		outLayer = LinearLayer(1)

		net.addInputModule(inLayer)
		net.addModule(hiddenLayer1)
		net.addModule(hiddenLayer2)
		net.addOutputModule(outLayer)

		in_to_hidden = FullConnection(inLayer, hiddenLayer1)
		hth = FullConnection(hiddenLayer1, hiddenLayer2)
		hidden_to_out = FullConnection(hiddenLayer2, outLayer)
		
		net.addConnection(in_to_hidden)
		net.addConnection(hth)
		net.addConnection(hidden_to_out)
		
		net.sortModules()
		
		print "making trainer..."
		trainer = BackpropTrainer(net, dataset=self.ds, learningrate=0.01, momentum=0.04, verbose=True, weightdecay=0.01)

		nf  = 0;
		#while True:
		print trainer.trainUntilConvergence(maxEpochs=10, verbose=True)#, continueEpochs, validationProportion);
		print "Writing netwokt to file"
		NetworkWriter.writeToFile(net, ("./network_OOOK!.xml"))
		nf+=1;
		while True:
			image = fc.get_last_frame_pil();
			image.show();
			a = raw_input("somes");
			for i in xrange(ix-1):
				for j in xrange(iy-1):
						crp = image.crop((i*cellingtile,j*cellingtile,i*cellingtile+cellingsize,j*cellingtile+cellingsize))
						if self.detection(net,crp):
							crp.show();
			print self.t," true"
			print self.f," false"
if __name__ == "__main__":
	test().run()