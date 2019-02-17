# -*- coding: cp1251 -*-
__author__ = 'Work'
from config import b,ports,std_speeds,data_bits,paritys,stop_bits


import init_window
from PyQt5 import QtGui,QtCore
import serial
from PyQt5.QtWidgets import QMainWindow
import sys

import user_threads
import admin_window
import dialog_window
import config
import threading
import user_menu_window

class ExampleApp(QMainWindow, admin_window.Ui_MainWindow,QtCore.QThread):# this is class for administrator window
    def __init__(self):
            # Explaining super is out of the scope of this article
            # So please google it if you're not familar with it
            # Simple reason why we use it here is that it allows us to
            # access variables, methods etc in the design.py file
            super(self.__class__, self).__init__()
            self.setupUi(self)  # This is defined in design.py file automatically

            # It sets up layout and widgets that are defined
            self.init_combos() # �������������� ��������� �������� �������������� � ����
            self.pushButton.clicked.connect(self.browse_port)  #������ ����������� 1 ������������
            self.pushButton_2.clicked.connect(self._check) #������ �������� ����������� ���������� � ������
            self.pushButton_3.clicked.connect(self.connect_default) #������  ����������� 4-� ������������� � ����������� �� ���������
            self.pushButton_4.clicked.connect(self._disconnect) # ������ ������������ ���� �������������
            self.listWidget.addItem('No link:(')
            self.pushButton_5.clicked.connect(self._identify_users) # ������ ���������� ������������� � ������ �������������


    def hello(self): # timer that ticks every 10 seconds to check link
        config.isLink=False # ���������� ���� ������� ����� link �������
        try:
            config.admin_port2.write(# ������� ��������� ���� link
                config.start_byte+ # ��������� ����
                init_window.bin_char(config.admin_port_num)+ # ����������� ����� ���������� �� ����������� � �������� ��� ��� �������� � �����
                config.get_code('link')+ #�������� ��� ����� link �� ����������������� �����
                config.stop_byte) # �������� ����
        except: # ����������� ��������� �� ����������(������� ������ � �������� COM ����)
            pass

        t=threading.Timer(10.0, self.hello) # �������������� ������, ������� �������� ������� hello ����� 10 ������
        t.start()
        self.check_() # ��.����

    def check_(self): # ������� �������� ����� ������� ����� link
        if config.isLink==False:
            self.listWidget.addItem('No link:(')

    def _identify_users(self): #������� ���������� ������������� � ������� � ������ ������ �������������
        msg=""
        j=0 # ������� �����
        for i in config.ports_all['real_enter']:
            # print(len(config.ports_all['real_enter'])) # ��������� � ���� ������ ����� ����� �������� ����� ������������
            msg=msg+i
            try:
                user=dialog_window.to_code(config.ports_all['real_user_name'][j]) #��������� � �������������� ���� ����� ��� ������������
            except:
                pass
            j=j+1
            for i in range(10-len(user)): #����� ����� � ����� 10 ��������,������� ��������� ��� ��������� �� 10-�� ��������
                user=user+' '
                msg=msg+user
        try: #��������� ���� set � �������� ��� ��������� �� �������� ����
            config.admin_port2.write(config.start_byte+ # ��������� ����
                                    init_window.bin_char(config.admin_port_num)+ # ����������� ����� ���������� �� ����������� � �������� ��� ��� �������� � �����
                                    config.get_code('set')+ #�������� ��� ����� set �� ����������������� �����
                                    msg+ # ��������� , ���������� ������ ������ � ����� �������������
                                    config.stop_byte) # �������� ����
        except:
            pass

    def browse_port(self): # ������� ����������� ������������
        try:
            a=[config.ports_all['suposed_enter'][self.comboPortNumber.currentIndex()],
               std_speeds[self.comboBaudRate.currentIndex()],
               data_bits[self.comboDataBits.currentIndex()],
               stop_bits[self.comboStopBits.currentIndex()],
               paritys[self.comboParity.currentIndex()],
               config.ports_all['suposed_exit'][self.comboPortNumber2.currentIndex()],
                ]
            user_name=self.lineEdit.text()

            user_menu_window.PORT=a[0]
            user_menu_window.BAUD=int(a[1])
            user_menu_window.BITSIZE=int(a[2])
            user_menu_window.PARITY=a[4]

            if a[0]!=a[5]:
                init_window.create_dialog(a[0][3:],a[5][3:],self,user_name,self) # �������� ������� �������� ������� � �����������, ���������� ��������������� � ��������������
            else: #������������ ������ ���������� ������ COM ������
                QtGui.QMessageBox.critical( None,"error",
                                            "enter and exit COM ports must be different!",
                                            buttons=QtGui.QMessageBox.Ok,
                                            defaultButton=QtGui.QMessageBox.Ok)
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)


    def link_check(self,msg):
        self.listWidget.addItem(msg)

    def _check(self): #������ �������� ����������� ���������� � ������
        config.isLink=False
        try:
            config.admin_port2.write(
                config.start_byte+ # ��������� ����
                init_window.bin_char(config.admin_port_num)+ # ����������� ����� ���������� �� ����������� � �������� ��� ��� �������� � �����
                config.get_code('link')+ # �������� ��� ����� link �� ����������������� �����
                config.stop_byte) # �������� ����
            #gtet_a_tet.bin_char(data_.admin_port_num)
        except: # ���� ��� �� ��������������� �� ���� ������������
            self.listWidget.addItem('No ports connected yet')

    def connect_default(self): # ������� ����������� ������ �� ���������
        a=[
           std_speeds[self.comboBaudRate.currentIndex()],
           data_bits[self.comboDataBits.currentIndex()],
           stop_bits[self.comboStopBits.currentIndex()],
           paritys[self.comboParity.currentIndex()],
            ]
        user_threads.BAUD=int(a[0])
        user_threads.BITSIZE=int(a[1])
        user_threads.STOPBITS=int(a[2])
        user_threads.PARITY=a[3]
        init_window.create_dialog('22','23',self,'1',self)
        init_window.create_dialog('24','25',self,'2',self)
        init_window.create_dialog('26','27',self,'3',self)
        init_window.create_dialog('28','21',self,'4',self)
        config.DTRs.append({"port_num1":"23","port_num2":"24","is_DTR":True,"data":[]})
        config.DTRs.append({"port_num1":"25","port_num2":"26","is_DTR":True,"data":[]})
        config.DTRs.append({"port_num1":"27","port_num2":"28","is_DTR":True,"data":[]})
        config.DTRs.append({"port_num1":"28","port_num2":"21","is_DTR":True,"data":[]})
        self.hello()

    def _succeed(self,link_checker=None):
        config.isLink=True
        #data_.timers['is_link']=True
        self.listWidget.addItem('Link:)')
        #data_.timers['link']=time.time()
        # print ('signal link recieved ')

    def init_combos(self): # ������� ������������� ��������������
        self.comboPortNumber.clear()  # ������� �������������, ���������� ������ ��������� ������� ������.��� ����������� ������������� �� ����� ��������� ������ ����� ��������
        self.comboPortNumber2.clear() # ������� �������������, ���������� ������ ��������� �������� ������
        self.comboPortNumber.addItems(config.ports_all['suposed_enter'])  # ������������� ������� ������� COM ������ �������������� �������� �� ����������������� �����
        self.comboPortNumber2.addItems(config.ports_all['suposed_exit']) # ������������� ������� �������� COM ������ �������������� �������� �� ����������������� �����
        self.comboBaudRate.addItems(std_speeds) # ������������� ��������� COM ������ �������������� �������� ��������� �� ������ ����� �����
        self.comboDataBits.addItems(data_bits) # ������������� ��� ������ COM ������ �������������� �������� ��� ������ �� ������ ����� �����
        self.comboStopBits.addItems(paritys) # ������������� ���������� ��� �������� COM ������ �������������� �������� ��������� �� ������ ����� �����
        self.comboParity.addItems(stop_bits) # ������������� �������� COM ������ �������������� �������� ��������� �� ������ ����� �����

    def _disconnect(self): # ������� ��������� ���� uplink
        config.admin_port2.write(config.start_byte+ # ��������� ����
                                init_window.bin_char(config.admin_port_num)+ # ����������� ����� ���������� �� ����������� � �������� ��� ��� �������� � �����
                                config.get_code('uplink')+ # �������� ��� ����� uplink �� ����������������� �����
                                config.stop_byte) # �������� ����


def get_all_comports(): # get all real ports
    return list(serial.tools.list_ports_windows.comports())


