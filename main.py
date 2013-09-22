import sys
from PyQt4.Qt import *
from PyQt4 import QtCore
import time

from Capture import Capturer
from AI import MyAI
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
        self.capturemenu = self.menubar.addMenu('&Capture')

        entry = self.capturemenu.addAction("Start")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doCapture)

        entry = self.capturemenu.addAction("Toogle image diff")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doToogleDiff)

        entry = self.filemenu.addAction("Exit")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doExit)

        self.capturer = Capturer()
        self.log("Capturer initialized!")
        
        self.controller = Controller()
        self.log("Contoller initialized!")
        
        self.ai = MyAI()
        self.log("AI initialized!")

        self.ai.set_capturer(self.capturer)
        self.ai.set_controller(self.controller)
        self.connect(self.ai,QtCore.SIGNAL('log'), self.log)
        self.connect(self.capturer,QtCore.SIGNAL('log'), self.log)

    def doToogleDiff(self):
        self.ai.toogle_diff_show();

    def doCapture(self):
        self.capturer.start_capture()
        r = self.capturer.get_rect();
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
