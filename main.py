from Application import Application

import sys
from PyQt5 import QtWidgets, QtCore, QtGui

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Application()
    win.show()
    sys.exit(app.exec_())


main()