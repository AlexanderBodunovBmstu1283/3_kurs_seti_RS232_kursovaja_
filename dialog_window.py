# -*- coding: cp1251 -*-
__author__ = 'Work'

import os,sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from PyQt5 import QtCore, QtGui
import init_window
import user_menu_window
import threading
import config
import code_decode1
from PyQt5 import QtWidgets

class Tetatet(QtWidgets.QWidget):
  def __init__(self,port_num1,port_num2,user_name,ser1,ser2,threadIn, parent=None): # код метода init генерируется автоматически при конвертировании из ui файла в py файл
    QtWidgets.QWidget.__init__(self, parent)

    self.lbl1 = QtGui.QLabel("Message_story")
    self.lbl1.setAlignment(QtCore.Qt.AlignCenter)

    self.txtHist = QtGui.QTextEdit()
    self.txtHist.setReadOnly(True)


    self.vbox = QtGui.QVBoxLayout()
    self.vbox.addWidget(self.lbl1)
    self.vbox.addWidget(self.txtHist)

    self.txtOut = QtGui.QLineEdit()
    self.btnSend = QtGui.QPushButton("Send")
    self.threadIn=threadIn

    self.hbox = QtGui.QHBoxLayout()
    self.hbox.addWidget(self.txtOut)
    self.hbox.addWidget(self.btnSend)

    self.vbox.addLayout(self.hbox)

    self.setLayout(self.vbox)

    ############# код,добавленный  в конвертированный файл
    self.ackCounter=0
    self.msgQuerry=[]
    self.portnum1=port_num1
    self.portnum2=port_num2
    self.reciever_true=init_window.bin_char(int(self.portnum1))
    try:

        for i in user_menu_window.msgs_all:
            if str(i) == self.portnum2:
                for j in user_menu_window.msgs_all[i]:
                    self.txtHist.append(j+'\n')
                if i[-10:-8]==self.portnum1:
                    self.txtHist.append(i+'\n')
    except:
        self.txtHist.append(self.portnum1)

    self.connect(self.btnSend, QtCore.SIGNAL("clicked()"), self.onSend)

    self.setWindowTitle(self.portnum1+' --> '+self.portnum2)
    self.resize(500, 250)
    #############
    #self.connect(self.threadIn, QtCore.SIGNAL("ackIn(QString)"), self.ackRcvd, QtCore.Qt.QueuedConnection)

  def hello(self): #функция, инициализирующая таймер
        if self.isAck==False: # если не получен кадр asc с момента посылки сообщения
            if self.ackCounter < 3: # если не было 3-х попыток отправки сообщения
                self.ackCounter=self.ackCounter+1 # инкрементируем счетчик количества попыток
                self.onSend() # посылаем то же сообщение снова
            else:
                QtGui.QMessageBox.critical( None,"failed",
                                            "Message is not delivered after 3 attempts!contact administrator ",
                                            buttons=QtGui.QMessageBox.Ok,
                                            defaultButton=QtGui.QMessageBox.Ok
                                            )
                self.msgQuerry.pop(0) #
                self.ackCounter=0
                self.isAck=True


  def ackRcv(self):
      global t
      self.isAck=True
      t.cancel()
      self.ackCounter=0
      if len(self.msgQuerry)>0:
          self.threadIn.send(self.msgQuerry[0]) # посылаем следующее сообщение из очереди
          self.msgQuerry.pop(0) # извлекаем только что отпраленное сообщение из очереди



  def onSend(self):
    self.isAck=False
    self.msg=''
    global t
    self.txtHist.append('   '+self.txtOut.text())
    try:
        user_menu_window.msgs_all[''+str(int(self.portnum2))].append('   '+self.txtOut.text())
    except:
        user_menu_window.msgs_all[''+str(int(self.portnum2))]=['   '+self.txtOut.text()]
    #if self.portnum1=='28': #or self.portnum1=='29':
    #    self.portnum1='22'
    if self.msg=='':
        bit_text=self.txtOut.text() # получаем сообщение из текстового поля
        cicle_coded_bit_text=code_decode1.Code(to_code(bit_text))
        print(cicle_coded_bit_text)
        print ("sender: "+self.portnum1+"-->"+self.portnum2)
        self.msg=str(config.start_byte+ # стартовый байт
                     init_window.bin_char(int(self.portnum2))+ # преобразуем адрес получателя из десятичного в двоичный вид для передачи в кадре
                     config.get_code('info')+ # получаем код кадра info из конфигурационного файла
                     init_window.bin_char(int(self.portnum1))+ # преобразуем адрес отправителя из десятичного в двоичный вид для передачи в кадре
                     str(init_window.bin_char(int(len(cicle_coded_bit_text)/7)))+ # длина сообщения из текстового поля
                     str(to_code(bit_text))+ # сообщение из текстового поля кодируем строкой байтов
                     config.stop_byte)  # стоповый байт
    self.threadIn.send(self.msg) # отправляем полученное сообщение в выходной порт
    self.msgQuerry.append(self.msg) # добавляем сообщение в очередь
    self.txtOut.clear() # очищаем текстовое поле
    t = threading.Timer(3.0, self.hello)
    t.start()


def to_code(_text): # функция преобразования сообщения в строку байтов
    a=''
    for i in _text:
        a=a+init_window.bin_char( # добавляем к строке новый байт,
            ord(str(i))) #  полученный путем преобразования в двоичный вид кода символа в таблице ascii
    return a # возвращаем полученную строку байт
