"""Входная точка."""
import sys
from PyQt5 import QtWidgets
from main_window import MainWindow

if __name__ == "__main__":
    sys.setrecursionlimit(4000)
    application = QtWidgets.QApplication(sys.argv)
    application_window = MainWindow()
    application_window.setFixedSize(800, 600)
    application_window.show()
    application.exec_()
