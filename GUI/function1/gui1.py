import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app

qtCreatorFile = "function1/Direct.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Funct1(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.back.clicked.connect(self.come_back)

    def come_back(self):
        self.main = app.Homepage()
        self.main.show()
        self.close()
