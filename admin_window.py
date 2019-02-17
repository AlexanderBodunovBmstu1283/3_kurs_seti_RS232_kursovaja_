# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'my_design.ui'
#
# Created: Wed Apr 05 17:31:45 2017
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore
from PyQt5 import QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 50, 151, 111))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 220, 751, 301))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 20, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(230, 50, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(230, 80, 71, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(230, 110, 61, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(230, 140, 46, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.comboPortNumber = QtWidgets.QComboBox(self.centralwidget)
        self.comboPortNumber.setGeometry(QtCore.QRect(312, 20, 171, 22))
        self.comboPortNumber.setObjectName(_fromUtf8("comboPortNumber"))
        self.comboBaudRate = QtWidgets.QComboBox(self.centralwidget)
        self.comboBaudRate.setGeometry(QtCore.QRect(310, 50, 171, 22))
        self.comboBaudRate.setObjectName(_fromUtf8("comboBaudRate"))
        self.comboDataBits = QtWidgets.QComboBox(self.centralwidget)
        self.comboDataBits.setGeometry(QtCore.QRect(310, 80, 171, 22))
        self.comboDataBits.setObjectName(_fromUtf8("comboDataBits"))
        self.comboStopBits = QtWidgets.QComboBox(self.centralwidget)
        self.comboStopBits.setGeometry(QtCore.QRect(310, 110, 171, 22))
        self.comboStopBits.setObjectName(_fromUtf8("comboStopBits"))
        self.comboParity = QtWidgets.QComboBox(self.centralwidget)
        self.comboParity.setGeometry(QtCore.QRect(310, 140, 171, 22))
        self.comboParity.setObjectName(_fromUtf8("comboParity"))
        self.comboPortNumber2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboPortNumber2.setGeometry(QtCore.QRect(510, 20, 161, 22))
        self.comboPortNumber2.setObjectName(_fromUtf8("comboPortNumber2"))
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(680, 20, 71, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(560, 70, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(510, 70, 46, 13))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 100, 141, 61))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 180, 151, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(540, 180, 141, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(300, 180, 180, 23))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")#(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText("Подключиться к COM")#(QtGui.QApplication.translate("MainWindow", "Подключиться к COM", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText("Номер порта1")#(QtGui.QApplication.translate("MainWindow", "№ порта1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText("скорость")#(QtGui.QApplication.translate("MainWindow", "скорость", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText("биты данных")#(QtGui.QApplication.translate("MainWindow", "биты данных", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText("стоп биты")#(QtGui.QApplication.translate("MainWindow", "стоп биты", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText("четность")#(QtGui.QApplication.translate("MainWindow", "четность", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText("номер порта2")#(QtGui.QApplication.translate("MainWindow", "номер порта2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText("имя")#(QtGui.QApplication.translate("MainWindow", "имя", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText("проверка соединения")#(QtGui.QApplication.translate("MainWindow", "проверка соединения", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText("по умолчанию")#(QtGui.QApplication.translate("MainWindow", "по умолчанию", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText("разорвать соединение")#(QtGui.QApplication.translate("MainWindow", "разорвать соединение", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText("получить список пользователей")#(QtGui.QApplication.translate("MainWindow", "получить список пользователей", None, QtGui.QApplication.UnicodeUTF8))

