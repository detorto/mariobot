import sys
from PyQt4.Qt import *
from PyQt4 import QtCore
import time

from Capture import StreamCapturer
from Capture import FileCapturer
from AI import MyAI
from AI import VisualTrainer
from Controll import Controller


class MainWindow(QMainWindow):

    def log(self,text):
        self.list.addItem(text)

    def __init__(self, *args):

        QMainWindow.__init__(self, *args)
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

        entry = self.diagmenu.addAction("Toogle image diff")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doToogleDiff)

        entry = self.filemenu.addAction("Exit")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doExit)

        self.initEngines();

    def initEngines(self):
        self.capturer = StreamCapturer()
        self.log("Capturer initialized!")
        
        self.controller = Controller()
        self.log("Contoller initialized!")
        
        self.ai = MyAI()
        self.log("AI initialized!")

        self.ai.set_capturer(self.capturer)
        self.ai.set_controller(self.controller)
        self.connect(self.ai,QtCore.SIGNAL('log'), self.log)
        self.connect(self.capturer,QtCore.SIGNAL('log'), self.log)

    def doTraining(self):
        self.trainer = VisualTrainer()
        self.trainer.set_ai(self.ai)
        self.trainer.set_capturer(FileCapturer())
        self.connect(self.trainer,QtCore.SIGNAL('log'), self.log)
        self.trainer.start_training()

    def doToogleDiff(self):
        self.ai.toogle_diff_show();

    def doPlay(self):
        self.capturer.start_capture()
        self.ai.start_ai()

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
