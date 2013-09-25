from PyQt4.Qt import *
from PyQt4 import QtCore

import pygame
import copy

class VisualTrainer(QtCore.QThread):
    def set_ai(self, ai):
        QtCore.QThread.__init__(self)
        self.ai = ai

    def log(self,string):
        self.emit(SIGNAL("log"),string)    
    
    def init_test_screen(self):
        pygame.init()
        self.size = (self.capturer.get_rect().width(),self.capturer.get_rect().height())
        self.winscreen = pygame.display.set_mode(self.size)
        self.log("Diag screen inited (%d, %d)" % self.size)

    def draw_rect(self,surf,rect,tpe):
    	color = (0,255,0)
    	if tpe == "AI":
    		color = (255,0,0)

        pygame.draw.rect(surf,color,(rect.x(),rect.y(),rect.width(),rect.height()),1)

    def run(self):

        self.init_test_screen();

        while True:
            
            frame = self.capturer.get_last_frame_bytestring()
            if not frame:
            	break;
           
            ai_player_rect = self.ai.detect_player(frame);

            corrected = False;
            was_lb_pressed = False;
            mx,my = 0,0
            sx,sy = 0,0
            while not corrected:
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: corrected = True;
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        was_lb_pressed = True;
                        sx,sy = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONUP:
                        was_lb_pressed = False;

                if was_lb_pressed:
                    mx,my = pygame.mouse.get_pos()


                #wait correction input
                surf = copy.copy(pygame.image.frombuffer(frame,self.size,"RGB"))
                self.draw_rect(surf,ai_player_rect,"AI");
                self.draw_rect(surf,QRect(sx,sy,mx-sx,my-sy),"USR");
                

                self.winscreen.fill(0)
                self.winscreen.blit(surf,(0,0))
                pygame.display.flip()

            self.ai.player_correct(QRect(sx,sy,mx-sx,my-sy))
        pygame.display.quit()
        self.ai.save_state();

    def set_capturer(self, capturer):
    	self.capturer = capturer
    
    def start_training(self):
    	self.capturer.start_capture();
    	self.start();
    	
    	

