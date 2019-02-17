# -*- coding: cp1251 -*-
__author__ = 'Work'
import initial
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import config
import sys
import admin_manage

# создает окно для ввода номеров используемых COM портов
class InitialWindow(QMainWindow, initial.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familiar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
        self.pushButton.clicked.connect(self.add_coms)  #эта кнопка добавляет введенные COM порты в список используемых
        self.pushButton_2.clicked.connect(self.link_window_appear)  #эта кнопка вызывает функцию создания  окна администратора

    def add_coms(self):
        try:
            port=self.txtOut.text()
            #создаем фильтр для ввода, игнорирующий недопустимые символы
            ports_=[x for x in port if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']]
            ports=''.join(map(str, ports_)) #формируем массив из номеров портов
            if "-" not in ports: # если добавлен 1 порт
                self.listWidget.addItem(ports) #добавляем его имя в текстовое поле
            else:  #введен диапазон
                i = int(ports[0:2]) #начальное значение диапазона введенных COM портов
                j= int(ports[3:5]) #конечное значение диапазона
                while i <=j: # идем по значениям из диапазона
                    self.listWidget.addItem(str(i)) #добавляем  имя порта в текстовое поле
                    config.ports_all['pairs'].append(str(i)) #добавляем номер порта пары в конфигурационный файл (config.py) в массив пар портов
                    config.ports_all['suposed_enter'].append('COM'+str(i)) #в массив предполагаемых входных портов добавляем номер порта в конфигурационный файл (config.py)
                    config.ports_all['suposed_exit'].append('COM'+str(i)) #в массив предполагаемых выходных портов добавляем номер порта в конфигурационный файл (config.py)
                    i=i+1
                # print(config.ports_all['suposed_exit'])
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)

    def link_window_appear(self): #создание окна администратора
        try:
            global form1
            form1 = admin_manage.ExampleApp()  # We set the form to be our ExampleApp (design)
            form1.show()  # Show the form
        except:
            (type, value, traceback) = sys.exc_info()
            sys.excepthook(type, value, traceback)