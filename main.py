#need for this
#	qt4



import sys
from PyQt4.Qt import *
from PyQt4 import QtCore
import time

from Capture import Capturer
from AI import MyAI

class MainWindow(QMainWindow):

    def __init__(self, *args):
        
        QMainWindow.__init__(self, *args)
        self.setGeometry(QRect(0, 0, 400, 200))
        
        #making window transparent       
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
 
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Move this window up to the game screen, and select "start" in the capture menu')
 
        self.menubar = self.menuBar()

    	self.filemenu = self.menubar.addMenu('&File')
        self.capturemenu = self.menubar.addMenu('&Capture')
        
        entry = self.capturemenu.addAction("Start")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doCapture)

        entry = self.filemenu.addAction("Exit")
        self.connect(entry,QtCore.SIGNAL('triggered()'), self.doExit)

        self.capturer = Capturer()
        self.ai = MyAI()
        #TODO:
        #self.controller = Controller()

        self.ai.set_capturer(self.capturer)
        self.connect(self.capturer,QtCore.SIGNAL('needscreen'), self.capture_frame)
        #TODO:
        #self.ai.set_contoller(self.controller)

    def capture_frame(self,data):
        callback = data[0]
        rect = data[1]

        pmap = QPixmap.grabWindow(QApplication.desktop().winId(),rect.x(),rect.y(),rect.width(),rect.height()).toImage().rgbSwapped();
        callback(pmap);

    def doCapture(self):
    	win_rect = self.geometry()
    	
    	x = win_rect.x()
    	y = win_rect.y()
    	w = win_rect.width()
    	h = win_rect.height()

    	win_rect = self.menubar.geometry()

    	y = y + win_rect.height()
    	h = h - win_rect.height()

    	win_rect = self.statusbar.geometry()

    	h = h - win_rect.height()

    	time.sleep(0.2)
        
        self.capturer.start_capture(QRect(x,y,w,h))
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