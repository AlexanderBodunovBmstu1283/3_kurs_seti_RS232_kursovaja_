# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'initial.ui'
#
# Created: Sat Apr 01 22:40:01 2017
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(325, 277)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(219, 10, 91, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.txtOut = QtWidgets.QLineEdit(self.centralwidget)
        self.txtOut.setGeometry(QtCore.QRect(75, 10, 131, 21))
        self.txtOut.setObjectName(_fromUtf8("textEdit"))
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 40, 75, 191))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 211, 192))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 20))
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 325, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")#(QApplication.translate("MainWindow", "MainWindow", None, QApplication.UnicodeUTF8))
        self.pushButton.setText("добавить")#(QApplication.translate("MainWindow", "добавить", None, QApplication.UnicodeUTF8))
        self.pushButton_2.setText("ок")#(QApplication.translate("MainWindow", "ок", None, QApplication.UnicodeUTF8))
        self.label.setText("номер COM")#(QApplication.translate("MainWindow", "номер COM", None, QApplication.UnicodeUTF8))

