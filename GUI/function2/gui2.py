import sys
sys.path.append("..")

from PyQt5 import QtCore, QtGui, QtWidgets, uic
import app

qtCreatorFile1 = "function2/Near_res.ui"
qtCreatorFile2 = "function2/Direct_near_res.ui"
Ui_MainWindow1, QtBaseClass1 = uic.loadUiType(qtCreatorFile1)
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)

class Funct2(QtWidgets.QMainWindow, Ui_MainWindow1):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow1.__init__(self)
        self.setupUi(self)
        self.top.clicked.connect(self.top_res)
        self.back.clicked.connect(self.come_back)

    def come_back(self):
        self.main = app.Homepage()
        self.main.show()
        self.close()

    def top_res(self):
        self.main = Funct2_result()
        self.main.show()
        self.close()

class Funct2_result(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.back.clicked.connect(self.come_back)

    def come_back(self):
        self.main = Funct2()
        self.main.show()
        self.close()