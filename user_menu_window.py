# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_dialoge_1.ui'
#
# Created: Tue Mar 14 17:06:08 2017
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
import config
import dialog_window
import serial
import user_threads
import init_window

msgs_all={}

num_winds=10
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

BAUD = 9600
BITSIZE=8
PARITY='N'
STOPBITS=1


class Ui_Dialog(QtWidgets.QWidget):
    def __init__(self, port_num1,port_num2,username, parent=None): # код метода init генерируется автоматически при конвертировании из .ui файла в .py файл
        self.centralwidget=QtWidgets.QWidget.__init__(self, parent)
        self.isOnline=True
        self.setWindowTitle(u""+str(username) +' port : '+ port_num1)#, encoding="UTF-8")
        self.resize(700, 250)
        self.lbl1 = QtWidgets.QLabel("User_menu")
        self.lbl1.setAlignment(QtCore.Qt.AlignCenter)
        self.portnum1=port_num1
        self.portnum2=port_num2
        self.username=username
        self.combo = QtWidgets.QComboBox()

        ############## код,добавленный  в конвертированный файл
        # пытаемся открыть входной порт с параметрами, указанными в начале файла
        self.ser1 = serial.Serial('COM'+port_num1,BAUD,BITSIZE,PARITY,STOPBITS)
        #except: # SerialException:
            #print("Cannot open port", port_num1,"BAUD",BAUD,'BITSIZE',BITSIZE,'PARITY',PARITY,'STOPBITS',STOPBITS)
            #exit(0)
        try: # пытаемся открыть выходной порт с параметрами, указанными в начале файла
            self.ser2 = serial.Serial('COM'+port_num2,BAUD,BITSIZE,PARITY,STOPBITS)
        except: # SerialException:
            print("Cannot open port", port_num2,"BAUD",BAUD,'BITSIZE',BITSIZE,'PARITY',PARITY,'STOPBITS',STOPBITS) # сообщаем о невозможности открыть порт.Эта ситуация возникает, когда порт уже открыт
            exit(0) # завершаем работу программы
        ##############

        self.threadIn=user_threads.ThreadIn(self.portnum1,self.portnum2,self.ser1,self.ser2,self.combo,self)
        self.threadIn.start()
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.lbl1)
        self.btnSend = QtWidgets.QPushButton("Create dialog")
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.btnSend)
        self.hbox.addWidget(self.combo)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)
        self.pushButton_2 = QtWidgets.QPushButton("enter/exit")
        self.pushButton_2.setGeometry(QtCore.QRect(360, 0, 75, 23))
        self.pushButton_3 = QtWidgets.QPushButton("disconnect")
        self.pushButton_3.setGeometry(QtCore.QRect(450, 0, 75, 23))
        self.hbox.addWidget(self.pushButton_2)
        self.hbox.addWidget(self.pushButton_3)
        #self.connect(self.btnSend, QtCore.SIGNAL("clicked()"), self._create)#(port_num1,username))
        self.btnSend.clicked.connect(self._create)
        self.pushButton_2.clicked.connect(self._unlink)
        self.pushButton_3.clicked.connect(self.disconnect_)
        #self.connect(self.threadIn, QtCore.SIGNAL("msgIn(QString)"), self.onRcvd, QtCore.Qt.QueuedConnection)
        #self.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self._unlink)
        #self.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.disconnect_)
        #self.connect(self.threadIn, QtCore.SIGNAL("ackIn(QString)"), self.ackRcvd, QtCore.Qt.QueuedConnection)

    def disconnect_(self): # функция разъединения пользователя
        self.ser2.isDtr=False # устанавливаем сигнал "не готов к приему" в выходной порт
        self.ser2.close() # закрываем выходной порт
        print('port is now disconnected')
        self.ser1.close() # закрываем входной порт


    def init_combo(self):
        self.combo.addItems(config.ports_all['real_enter'])

    def _unlink(self): # функция формирования кадра off
        msg=str(config.start_byte+init_window.bin_char(int(self.portnum1)+1)+config.get_code('off')+config.stop_byte)
        self.threadIn.send(msg)

    def _create(self): # функция создания окна диалога
        global num_winds
        if num_winds==10:
            global childwin10 # создаем глобальную переменную для инициализации окна диалога и его работы в бесконечном цикле
            self.port_num=config.ports_all['real_enter'][self.combo.currentIndex()] # получаем номер порта из переключателя
            childwin10 = dialog_window.Tetatet(self.portnum1,self.port_num,self.username,self.ser1,self.ser2,self.threadIn) # инициализируем глобальную переменную объектом диалога пользователей
            childwin10.show() # запускаем бесконечный цикл работы окна
            config.alpha.append(childwin10) # в конфигурационный файл записываем объект окна
            num_winds=num_winds+1 # инкрементируем счетчик количества диалогов
        else:
            if num_winds==11:
                global childwin11
                self.port_num=config.ports_all['real_enter'][self.combo.currentIndex()]
                childwin11 = dialog_window.Tetatet(self.portnum1,self.port_num,self.username,self.ser1,self.ser2,self.threadIn)
                childwin11.show()
                config.alpha.append(childwin11)
                num_winds=num_winds+1
            else:
                if num_winds==12:
                    global childwin12
                    self.port_num=config.ports_all['real_enter'][self.combo.currentIndex()]
                    childwin12 = dialog_window.Tetatet(self.portnum1,self.port_num,self.username,self.ser1,self.ser2,self.threadIn)
                    childwin12.show()
                    config.alpha.append(childwin12)
                    num_winds=num_winds+1
                else:
                    if num_winds==13:
                        global childwin13
                        self.port_num=config.ports_all['real_enter'][self.combo.currentIndex()]
                        childwin13 = dialog_window.Tetatet(self.portnum1,self.port_num,self.username,self.ser1,self.ser2,self.threadIn)
                        childwin13.show()
                        config.alpha.append(childwin13)
                        num_winds=num_winds+1
def reshifer(arr): # функция расшифровки сообщения
    text=str(arr[40:-10]) # получаем информационную часть сообщения
    #print(len(arr))
    i=int(len(text)/8) # получаем количество байт
    ans=''
    for k in range(i): # проходимся по байтам
        text_new=int(text[k*8:k*8+8],2) # получаем байт
        ans=ans+ str(chr(text_new)) # расшифровываем символ из байта и добавляем его в строку
    return ans # возвращаем расшифрованное слово




