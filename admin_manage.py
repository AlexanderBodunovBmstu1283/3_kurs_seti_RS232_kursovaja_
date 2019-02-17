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
            self.init_combos() # инициализируем начальные значения переключателей в окне
            self.pushButton.clicked.connect(self.browse_port)  #кнопка подключения 1 пользователя
            self.pushButton_2.clicked.connect(self._check) #кнопка проверки целостность соединения в кольце
            self.pushButton_3.clicked.connect(self.connect_default) #кнопка  подключения 4-х пользователей с параметрами по умолчанию
            self.pushButton_4.clicked.connect(self._disconnect) # кнопка отсоединения всех пользователей
            self.listWidget.addItem('No link:(')
            self.pushButton_5.clicked.connect(self._identify_users) # кнопка оповещения пользователей о других пользователях


    def hello(self): # timer that ticks every 10 seconds to check link
        config.isLink=False # сбрасываем флаг прихода кадра link обратно
        try:
            config.admin_port2.write(# функция формирует кадр link
                config.start_byte+ # стартовый байт
                init_window.bin_char(config.admin_port_num)+ # преобразуем адрес получателя из десятичного в двоичный вид для передачи в кадре
                config.get_code('link')+ #получаем код кадра link из конфигурационного файла
                config.stop_byte) # стоповый байт
        except: # предохраням программу от исключений(попытка записи в закрытый COM порт)
            pass

        t=threading.Timer(10.0, self.hello) # инициализируем таймер, который вызывает функцию hello через 10 секунд
        t.start()
        self.check_() # см.ниже

    def check_(self): # функция проверки факта прихода кадра link
        if config.isLink==False:
            self.listWidget.addItem('No link:(')

    def _identify_users(self): #функция оповещения пользователей о наличии и именах других пользователей
        msg=""
        j=0 # счетчик цикла
        for i in config.ports_all['real_enter']:
            # print(len(config.ports_all['real_enter'])) # добавляем в поле данных кадра номер входного порта пользователя
            msg=msg+i
            try:
                user=dialog_window.to_code(config.ports_all['real_user_name'][j]) #добавляем в информационное поле кадра имя пользователя
            except:
                pass
            j=j+1
            for i in range(10-len(user)): #длина имени в кадре 10 символов,поэтому дополняем имя пробелами до 10-ти символов
                user=user+' '
                msg=msg+user
        try: #формируем кадр set и пытаемся его отправить на выходной порт
            config.admin_port2.write(config.start_byte+ # стартовый байт
                                    init_window.bin_char(config.admin_port_num)+ # преобразуем адрес получателя из десятичного в двоичный вид для передачи в кадре
                                    config.get_code('set')+ #получаем код кадра set из конфигурационного файла
                                    msg+ # сообщение , содержащее номера портов и имена пользователей
                                    config.stop_byte) # стоповый байт
        except:
            pass

    def browse_port(self): # функция полключения пользователя
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
                init_window.create_dialog(a[0][3:],a[5][3:],self,user_name,self) # вызываем функцию создания диалога с параметрами, выбранными администратором в переключателях
            else: #пользователь выбрал одинаковые номера COM портов
                QtGui.QMessageBox.critical( None,"error",
                                            "enter and exit COM ports must be different!",
                                            buttons=QtGui.QMessageBox.Ok,
                                            defaultButton=QtGui.QMessageBox.Ok)
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)


    def link_check(self,msg):
        self.listWidget.addItem(msg)

    def _check(self): #кнопка проверки целостность соединения в кольце
        config.isLink=False
        try:
            config.admin_port2.write(
                config.start_byte+ # стартовый байт
                init_window.bin_char(config.admin_port_num)+ # преобразуем адрес получателя из десятичного в двоичный вид для передачи в кадре
                config.get_code('link')+ # получаем код кадра link из конфигурационного файла
                config.stop_byte) # стоповый байт
            #gtet_a_tet.bin_char(data_.admin_port_num)
        except: # если еще не зарегистрирован ни один пользователь
            self.listWidget.addItem('No ports connected yet')

    def connect_default(self): # функция подключения портов по умолчанию
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

    def init_combos(self): # функция инициализации переключателей
        self.comboPortNumber.clear()  # очищаем переключатель, содержащий номера доступных входных портов.При подключении пользователей он будет уменьшать список своих значений
        self.comboPortNumber2.clear() # очищаем переключатель, содержащий номера доступных выходных портов
        self.comboPortNumber.addItems(config.ports_all['suposed_enter'])  # переключатель номеров входных COM портов инициальзируем массивом из конфигурационного файла
        self.comboPortNumber2.addItems(config.ports_all['suposed_exit']) # переключатель номеров выходных COM портов инициальзируем массивом из конфигурационного файла
        self.comboBaudRate.addItems(std_speeds) # переключатель скоростей COM портов инициальзируем массивом скоростей из начала этого файла
        self.comboDataBits.addItems(data_bits) # переключатель бит данных COM портов инициальзируем массивом бит данных из начала этого файла
        self.comboStopBits.addItems(paritys) # переключатель количества бит четности COM портов инициальзируем массивом четностей из начала этого файла
        self.comboParity.addItems(stop_bits) # переключатель четности COM портов инициальзируем массивом четностей из начала этого файла

    def _disconnect(self): # функция формирует кадр uplink
        config.admin_port2.write(config.start_byte+ # стартовый байт
                                init_window.bin_char(config.admin_port_num)+ # преобразуем адрес получателя из десятичного в двоичный вид для передачи в кадре
                                config.get_code('uplink')+ # получаем код кадра uplink из конфигурационного файла
                                config.stop_byte) # стоповый байт


def get_all_comports(): # get all real ports
    return list(serial.tools.list_ports_windows.comports())


