from PyQt4.Qt import *
from PyQt4 import QtCore

import pygame
import copy
import Image
import time

from Utils import pil_image

from pybrain.datasets import SupervisedDataSet



def crop_rect(xy,wh):
    return xy+(xy[0]+wh[0],xy[1]+wh[1])

class VisualTrainer(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.process_ai = False;

    def set_ai(self, ai):
        self.net = ai.get_player_detection_net()
        self.ai = ai

    def log(self,string):
        self.emit(SIGNAL("log"),string)

    def init_test_screen(self):
        pygame.init()
        self.raw_size = self.raw_capturer.get_image_size()

        self.winscreen = pygame.display.set_mode(self.raw_size)

        self.log("Diag screen inited (%d, %d)" % self.raw_size)

    def draw_rect(self,surf,rect,tpe):
        if tpe == "POS":
            color = (0,255,0)
        if tpe == "NEG":
            color = (255,0,0)
        if tpe == "AI":
            color = (255,255,255)
        pygame.draw.rect(surf,color,rect,1)

    def toogle_ai_info(self):
        self.process_ai = not self.process_ai
        self.log("Ai processing is %s" % (str(self.process_ai)))

    def run(self):

        self.init_test_screen();
        self.net_input_size = self.net.input_image_size()

        training = True
        saved_count = 0

        while training:

            pygame.display.set_caption("Images processed: %d"%(saved_count))
            frame = self.raw_capturer.get_last_frame_bytestring()
            if self.process_ai:
                ai_answer = self.ai.analize_state({"current_frame_pil":pil_image(frame,self.raw_size)})

                try:
                    ai_answer["info"]["player_rect"];
                except:
                    self.log("No player rect in AI answer!");

            if not frame:
                self.log("No raw images left!")
                break;

            selected = {"NEG": False, "POS" : False}
            position = {"NEG":(0,0),"POS":(0,0)}

            skipped = False
            mx,my = 0,0

            while not selected["NEG"]:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        training = False
                        skipped = True
                        selected["NEG"] = True
                        selected["POS"] = True
                        break

                    if event.type == pygame.KEYDOWN:
                        selected["NEG"] = True
                        selected["POS"] = True
                        skipped = True

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        was_lb_pressed = True;
                        if selected["POS"]:
                            selected["NEG"] = True
                            position["NEG"] = (mx,my)#save negative here
                        else:
                            selected["POS"] = True
                            position["POS"] = (mx,my)

                mx,my = pygame.mouse.get_pos()
                surf = copy.copy( pygame.image.frombuffer(frame, self.raw_size, "RGB") )

                if not selected["POS"]:
                    self.draw_rect(surf, (mx,my)+self.net_input_size, "POS")
                else:
                    self.draw_rect(surf, (mx,my)+self.net_input_size, "NEG")
                    self.draw_rect(surf, position["POS"]+self.net_input_size, "POS")

                try:
                    self.draw_rect(surf,   ai_answer["info"]["player_rect"] , "AI")
                except:
                    pass

                self.winscreen.fill(0)
                self.winscreen.blit(surf,(0,0))
                pygame.display.flip()

            if skipped:
                continue

            positive_rect = crop_rect(position["POS"], self.net_input_size)
            negative_rect = crop_rect(position["NEG"], self.net_input_size)

            pos_image = pil_image(frame, self.raw_size).crop(positive_rect)
            neg_image = pil_image(frame, self.raw_size).crop(negative_rect)

            pos_data_folder = self.positive_capturer.get_folder();
            neg_data_folder = self.negative_capturer.get_folder();

            pos_image.save("%s/%d_%d.png"%(pos_data_folder, saved_count,time.time()))
            neg_image.save("%s/%d_%d.png"%(neg_data_folder, saved_count,time.time()))

            saved_count += 1
            self.log("Images processed: %d"%(saved_count))

        pygame.display.quit()
        self.log("Generating dataset....")
        dataset = self.generate_dataset();
        self.log("Training....")
        self.log("Error on last train is: %f"%(self.net.train_on_dataset(dataset)))
        self.log("Done training!")

    def set_raw_capturer(self, capturer):
        self.raw_capturer = capturer

    def set_positive_dataset_capturer(self,capturer):
        self.positive_capturer = capturer;

    def set_negative_dataset_capturer(self,capturer):
        self.negative_capturer = capturer;

    def start_training(self):
        self.raw_capturer.start_capture();
        self.start();


    def generate_dataset(self):
        self.positive_capturer.start_capture();
        self.negative_capturer.start_capture();
        pos_image = self.positive_capturer.get_last_frame_pil();
        neg_image = self.negative_capturer.get_last_frame_pil();

        neg_count = self.negative_capturer.get_count()
        pos_count = self.positive_capturer.get_count()

        self.log("There is %d positive images and"%(pos_count))
        self.log("%d negative images."%(neg_count))
        self.log("Generating %d sets!"%(min(neg_count, pos_count)))
        dataset = SupervisedDataSet(self.net.input_image_size()[0]*self.net.input_image_size()[1]*3, 1)

        while pos_image and neg_image:
            arr1 = [ord(x) for x in (list(pos_image.tostring()))]
            dataset.addSample(arr1, (1,))

            arr2 = [ord(x) for x in (list(neg_image.tostring()))]
            dataset.addSample(arr1, (0,))

            pos_image = self.positive_capturer.get_last_frame_pil();
            neg_image = self.negative_capturer.get_last_frame_pil();

        return dataset

