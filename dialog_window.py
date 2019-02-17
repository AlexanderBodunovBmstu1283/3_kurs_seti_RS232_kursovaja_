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
  def __init__(self,port_num1,port_num2,user_name,ser1,ser2,threadIn, parent=None): # ��� ������ init ������������ ������������� ��� ��������������� �� ui ����� � py ����
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

    ############# ���,�����������  � ���������������� ����
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

  def hello(self): #�������, ���������������� ������
        if self.isAck==False: # ���� �� ������� ���� asc � ������� ������� ���������
            if self.ackCounter < 3: # ���� �� ���� 3-� ������� �������� ���������
                self.ackCounter=self.ackCounter+1 # �������������� ������� ���������� �������
                self.onSend() # �������� �� �� ��������� �����
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
          self.threadIn.send(self.msgQuerry[0]) # �������� ��������� ��������� �� �������
          self.msgQuerry.pop(0) # ��������� ������ ��� ����������� ��������� �� �������



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
        bit_text=self.txtOut.text() # �������� ��������� �� ���������� ����
        cicle_coded_bit_text=code_decode1.Code(to_code(bit_text))
        print(cicle_coded_bit_text)
        print ("sender: "+self.portnum1+"-->"+self.portnum2)
        self.msg=str(config.start_byte+ # ��������� ����
                     init_window.bin_char(int(self.portnum2))+ # ����������� ����� ���������� �� ����������� � �������� ��� ��� �������� � �����
                     config.get_code('info')+ # �������� ��� ����� info �� ����������������� �����
                     init_window.bin_char(int(self.portnum1))+ # ����������� ����� ����������� �� ����������� � �������� ��� ��� �������� � �����
                     str(init_window.bin_char(int(len(cicle_coded_bit_text)/7)))+ # ����� ��������� �� ���������� ����
                     str(to_code(bit_text))+ # ��������� �� ���������� ���� �������� ������� ������
                     config.stop_byte)  # �������� ����
    self.threadIn.send(self.msg) # ���������� ���������� ��������� � �������� ����
    self.msgQuerry.append(self.msg) # ��������� ��������� � �������
    self.txtOut.clear() # ������� ��������� ����
    t = threading.Timer(3.0, self.hello)
    t.start()


def to_code(_text): # ������� �������������� ��������� � ������ ������
    a=''
    for i in _text:
        a=a+init_window.bin_char( # ��������� � ������ ����� ����,
            ord(str(i))) #  ���������� ����� �������������� � �������� ��� ���� ������� � ������� ascii
    return a # ���������� ���������� ������ ����
