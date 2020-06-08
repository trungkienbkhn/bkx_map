import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from function1 import gui1
from function2 import gui2
from function3 import gui3

qtCreatorFile = "Main.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Homepage(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.center()
        self.funct1.clicked.connect(self.switch_to_funct1)
        self.funct2.clicked.connect(self.switch_to_funct2)
        self.funct3.clicked.connect(self.switch_to_funct3)
        self.show()

    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def switch_to_funct1(self):
        self.main = gui1.Funct1()
        self.main.show()
        self.close()

    def switch_to_funct2(self):
        self.main = gui2.Funct2()
        self.main.show()
        self.close()

    def switch_to_funct3(self):
        self.main = gui3.Funct3()
        self.main.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Homepage()
    sys.exit(app.exec_())
