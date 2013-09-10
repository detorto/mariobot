import threading
import copy
from PyQt4.Qt import *
from PyQt4 import QtCore
import time
import pygame
import sys
class MyAI(QtCore.QThread):

	def __init__(self):
		QtCore.QThread.__init__(self)
		self.lock = threading.Lock();

	def init_test_screen(self):
		pygame.init()
		self.size = (self.capturer.rect.width(),self.capturer.rect.height())
 		self.winscreen = pygame.display.set_mode(self.size)

	def process_test_screen(self):
		surf = pygame.image.frombuffer(self.frame,self.size,"RGBX")
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()


			#self.winscreen.fill(0)
		self.winscreen.blit(surf,(0,0))
		pygame.display.flip()
		
	def set_capturer(self, capturer):
		self.capturer = capturer

	def set_controler(self, controller):
		pass

	def start_ai(self):
		self.start()
	
	def stop_ai(self):
		pass

	def do_analize(self):
		#here must be conwersion of image and calls to analise it.
		#image is QImage instanse, with inverted RGB.
		pass

	def run(self):

		self.init_test_screen()
		
		while(True):
			self.frame = self.capturer.get_last_frame_bytestring()
			
			self.do_analize()

			self.process_test_screen()
			
			#time.sleep(0.1)
