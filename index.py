# -*- coding: cp1251 -*-
__author__ = 'Work'
import initial
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import config
import sys
import admin_manage

# ������� ���� ��� ����� ������� ������������ COM ������
class InitialWindow(QMainWindow, initial.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familiar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        self.pushButton.clicked.connect(self.add_coms)  #��� ������ ��������� ��������� COM ����� � ������ ������������
        self.pushButton_2.clicked.connect(self.link_window_appear)  #��� ������ �������� ������� ��������  ���� ��������������

    def add_coms(self):
        try:
            port=self.txtOut.text()
            #������� ������ ��� �����, ������������ ������������ �������
            ports_=[x for x in port if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']]
            ports=''.join(map(str, ports_)) #��������� ������ �� ������� ������
            if "-" not in ports: # ���� �������� 1 ����
                self.listWidget.addItem(ports) #��������� ��� ��� � ��������� ����
            else:  #������ ��������
                i = int(ports[0:2]) #��������� �������� ��������� ��������� COM ������
                j= int(ports[3:5]) #�������� �������� ���������
                while i <=j: # ���� �� ��������� �� ���������
                    self.listWidget.addItem(str(i)) #���������  ��� ����� � ��������� ����
                    config.ports_all['pairs'].append(str(i)) #��������� ����� ����� ���� � ���������������� ���� (config.py) � ������ ��� ������
                    config.ports_all['suposed_enter'].append('COM'+str(i)) #� ������ �������������� ������� ������ ��������� ����� ����� � ���������������� ���� (config.py)
                    config.ports_all['suposed_exit'].append('COM'+str(i)) #� ������ �������������� �������� ������ ��������� ����� ����� � ���������������� ���� (config.py)
                    i=i+1
                # print(config.ports_all['suposed_exit'])
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

    def link_window_appear(self): #�������� ���� ��������������
        try:
            global form1
            form1 = admin_manage.ExampleApp()  # We set the form to be our ExampleApp (design)
            form1.show()  # Show the form
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)