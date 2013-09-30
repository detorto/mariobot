import sys
from PyQt4.Qt import *
from PyQt4 import QtCore
import time

from Capture import StreamCapturer
from Capture import FileCapturer
from AI import MyAI
from AI import VisualTrainer
from Controll import Controller
from AI import AIManager
from AI.NeuralNets import PlayerDetectionNet


class MainWindow(QMainWindow):

    def log(self,text):
        self.list.addItem(text)
        self.list.scrollToBottom()

    def __init__(self, *args):

        QMainWindow.__init__(self, *args)
        self.trainer = None;
        self.setGeometry(QRect(0, 0, 300, 300))
        self.list = QListWidget(self)
        self.list.setGeometry(QRect(0, 20, 300, 260))

        self.statusbar = self.statusBar()

        self.menubar = self.menuBar()

        self.filemenu = self.menubar.addMenu('&File')
        self.capturemenu = self.menubar.addMenu('&Simulator')
        self.diagmenu = self.menubar.addMenu('Diag window')

        entry = self.capturemenu.addAction("Start playing")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doPlay)

        entry = self.capturemenu.addAction("Start visual training")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doTraining)

        entry = self.diagmenu.addAction("Toogle AI info")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doToogleAIInfo)

        entry = self.diagmenu.addAction("Toogle image diff")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doToogleDiff)

        entry = self.diagmenu.addAction("Toogle saving to file")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doToogleSaving)

        entry = self.filemenu.addAction("Exit")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doExit)

        self.initEngines();


    def initEngines(self):
        CAPTURER_IMAGE_SIZE = (512, 448)
        self.capturer = StreamCapturer(CAPTURER_IMAGE_SIZE)

        self.log("Capturer initialized!")

        self.controller = Controller()
        self.log("Contoller initialized!")

        #here!
        self.ai = MyAI(player_detection_netclass =  PlayerDetectionNet )
        self.log("AI initialized!")

        self.manager = AIManager();

        self.manager.set_ai(self.ai)
        self.manager.set_capturer(self.capturer)
        self.manager.set_controller(self.controller)

        self.connect(self.manager,QtCore.SIGNAL('log'), self.log)
        self.connect(self.ai,QtCore.SIGNAL('log'), self.log)
        self.connect(self.capturer,QtCore.SIGNAL('log'), self.log)

    def doToogleAIInfo(self):
        if self.trainer:
            self.trainer.toogle_ai_info();
        self.manager.toogle_ai_info();

    def doTraining(self):

        self.trainer = VisualTrainer()

        self.trainer.set_ai(self.ai)

        self.trainer.set_raw_capturer(FileCapturer("./train_sets/raw_images/"))

        self.trainer.set_positive_dataset_capturer(FileCapturer("./train_sets/pos_data/"));
        self.trainer.set_negative_dataset_capturer(FileCapturer("./train_sets/neg_data/"));

        self.connect(self.trainer,QtCore.SIGNAL('log'), self.log)

        self.trainer.start_training()

    def doToogleDiff(self):
        self.manager.toogle_diff_show();

    def doToogleSaving(self):
        self.capturer.save_images_dir("./train_sets/raw_images/");
        self.capturer.save_images_parity(50)
        self.capturer.toogle_saving_images()

    def doPlay(self):
        self.capturer.start_capture()
        self.manager.start()

    def doExit(self):
        exit(0)

class App(QApplication):

    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow()
        self.connect(self, SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()

    def byebye( self ):
        self.exit(0)

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
