import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app

qtCreatorFile1 = "function3/Filter.ui"
qtCreatorFile2 = "function3/Direct.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)

class Funct3(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.filter.clicked.connect(self.res)
        self.back.clicked.connect(self.come_back)

    def come_back(self):
        self.main = app.Homepage()
        self.main.show()
        self.close()

    def res(self):
        self.main = Funct3_result()
        self.main.show()
        self.close()

class Funct3_result(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back.clicked.connect(self.come_back)

    def come_back(self):
        self.main = Funct3()
        self.main.show()
        self.close()