# -*- coding: cp1251 -*-
# __author__ = 'Work'
from PyQt5 import QtCore,QtGui
from PyQt5.QtGui import *
import serial
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import config
import dialog_window
import admin_window
from time import sleep
import time
import threading
import init_window
import user_menu_window
import code_decode1

PORT = "COM17"
BAUD = 9600
BITSIZE=8
PARITY='N'
STOPBITS=1

msgs_all={}


'''
класс для создания пользователя
'''
class ThreadIn(QtCore.QThread):
  # функция задания начальных параметров для пользователя
  def __init__(self,port_num1,port_num2,ser1,ser2,combo, parent=None):
    self.thread=QtCore.QThread.__init__(self, parent) # выносим в отдельный поток
    self.ser1=ser1
    self.ser2=ser2
    self.parent=parent # родительское окно
    self.combo=combo # выпадающий список с номерами портов
    self.port_num1=port_num1
    self.port_num2=port_num2
    self.timer=0
    self.isDTR=True
    self.isLink=True
    self.ports=[] # список допустимых портов-адресатов для данного пользователя
    self.users=[] # список допустимых имен пользователей, с которыми может общаться создаваемый пользователь
    #self.connect(self.parent, QtCore.SIGNAL("msgOut(QString)"), self.send, QtCore.Qt.QueuedConnection)

    #self.readThread.readthread.connect(self.change_state)

  def timer_30_sec(self): # таймер, реагирующий на отсутствие кадра link свыше 30-ти секунд
        t = threading.Timer(30.0, self.timer_30_sec)
        t.start()
        self.check_() # посылает кадр err
        self.isLink=False # сброс флага

  def check_(self):
      if self.isLink==False:
          self.send(config.start_byte+ # стартовый байт
                    init_window.bin_char(config.admin_port_num)+ # преобразуем адрес получателя из десятичного в двоичный вид для передачи в кадре
                    config.get_code('err')+ # получаем код кадра err из конфигурационного файла
                    init_window.bin_char(int(self.port_num1))+ # формируем адрес отправителя
                    config.stop_byte) # стоповый байт

  def phy_read(self):
    try:
        byte = str(self.ser1.read())    # Читаем один байт
    except:
            pass
    if len(byte) == 1:
          self.msg += byte               # Составляем строку
          if time.time()-self.timer>=1:
              self.isDTR=True
          else:
                self.isDTR=False
                self.ser1.setDTR(False)
          self.timer=time.time()


  def channnel_start_detect(self):
          if len(self.msg) <16 and self.msg[-8:]==config.stop_byte: # и длина сообщения меньше минимального, но стоповый байт нормальный
              self.err=True # выставляем признак ошибки
          if self.msg[-8:]==config.start_byte and self.is_begin==False: # если считан стартовый байт и сообщение еще не началось
              self.is_begin=True
              self.msg=config.start_byte # убираем лишние биты
          if len(self.msg)==16: # мы считали адрес получателя
              self.supposed_reciever=self.msg[8:16] # присваиваем адрес получателя
              print(int(self.supposed_reciever,2))
              #print("supposed_reciever = "+ supposed_reciever+'    '+self.bin_char(int(self.port_num2))) # отладка
              if self.supposed_reciever==self.bin_char(int(self.port_num1)): # сравниваем считанный адрес с адресом COM порта в двоичном виде
                  self.reciever_True=1 # сообщение пришло по адресу
                  print('message delivered')
              else:
                  if self.supposed_reciever in config.connected_ports:
                    self.reciever_True=0 # сообщение нуждается в дальнейшей перессылке
                    print('message transit')
                  else:
                    self.reciever_True=-1 # удаляем сообщение
                    print('failed to find destination adress')

  def channel_reciever_true(self):
      self.check_err_true()
      self.check_link_true()
      self.check_ack_true()
      self.check_data_true()
      self.check_off_true()

  def check_err_true(self):
    if self.msg[16:24]==config.get_code('err'): # если тип сообщения равен типу err
        config.main_terminal.listWidget.addItem("User "+str(int(self.msg[24:32],2))+" is unlink") # в окно администратора выводим сообщение,

  def check_link_true(self):
      if self.msg[16:24]==config.get_code('link'): # если тип сообщения равен типу Link
           self.isLink=True # выставляем флаг установления соединения
           config.main_terminal._succeed() # успешное возвращение кадра link

  def check_ack_true(self):
      if self.msg[16:24]==config.get_code('ack'): # если тип сообщения равен типу ack
                            print("-----------------------------------------------------------------------------------")
                            # print('подтверждение') # отладка
                            #self.emit(QtCore.SIGNAL("self.msgIn(QString)"), self.msg[8:16]+"ackk") # посылаем сигнал о приеме сообщения,
                            self.onRcvd(self.msg[8:16]+"ackk")
                            #  указывая в параметрах адрес отправителя и тип кадра(ack)
                            if len(config.write_data_query)>0: # если очередь сообщений на отправку не пуста
                                self.send(config.write_data_query[0]) # отсылаем первое сообщение из очереди
                                config.write_data_query.pop(0) # удаляем первое сообщение из очереди

  def check_data_true(self):
      if self.msg[16:24]==config.get_code('info'):
          if len(config.write_data_query)>0: # если очередь сообщений на отправку не пуста
                self.send(config.write_data_query[0]) # отсылаем первое сообщение из очереди
                config.write_data_query.pop(0)
          else:
            self.onRcvd(self.msg+"data")

  def check_off_true(self):
      if self.msg[16:24]==config.get_code('off') and self.reciever_True==1:
                    self.combo.clear()
                    who_unlink=str(int(self.supposed_reciever,2)-int('00000001',2))
                    if who_unlink in config.ports_all['real_enter']:
                        config.ports_all['real_enter'] = [el for el in config.ports_all['real_enter'] if el !=  who_unlink]
                        msg_status='offline'
                    else:
                        config.ports_all['real_enter'].append(who_unlink)
                        msg_status='online'
                    QtGui.QMessageBox.critical( None,"status",
                                            "Yout status is now "+msg_status,
                                            buttons=QtGui.QMessageBox.Ok,
                                            defaultButton=QtGui.QMessageBox.Ok
                                            )


  def channel_reciever_false(self):
      self.check_err_false()
      self.check_off_false()
      self.check_link_false()
      self.check_ack_false()
      self.check_data_false()
      self.check_set_false()

  def check_err_false(self):
      self.send(str(self.msg))

  def check_off_false(self):
      if self.msg[16:24]==config.get_code('off'):
            self.combo.clear()
            self.combo.addItems(config.ports_all['real_enter'])
            self.send(str(self.msg))

  def check_link_false(self):
      if self.msg[16:24]==config.get_code('link'):
          self.isLink=True
          self.send(str(self.msg))

  def check_ack_false(self):
      if self.msg[16:24]==config.get_code('ack'):
           self.send(str(self.msg))
           print("-----------------------------------------------------------------------------------")

  def check_data_false(self):
      if self.msg[16:24]==config.get_code('data'):
            if len(config.write_data_query)>0: # если очередь сообщений на отправку не пуста
                self.send(config.write_data_query[0]) # отсылаем первое сообщение из очереди
                config.write_data_query.pop(0)
            else:
                self.send(self.msg)

  def check_set_false(self):
      if self.msg[16:24]==config.get_code('set'):
            msg1=self.msg[24:-8]
            for i in range (int((len(msg1)/88))):
                try:
                    self.ports.append(user_menu_window.reshifer(msg1[i:i+8]))
                    self.users.append(user_menu_window.reshifer(msg1[i+8:i+88]))
                except:
                    pass
            self.send(str(self.msg))

  def check_uplink_false(self):
      if self.msg[16:24]==config.get_code('uplink'):
            self.send(str(self.msg))




  def run(self,parent_serial=None): #read from port
    self.msg = ""                      # Заготовка для новой строки
    reciever_True=1
    self.is_begin=False
    self.timer_30_sec()

    while True:

        # Вывод ответа произведём только тогда, когда строка будет сформирована полностью

        '''
        ищем стартовый байт в начале кадра
        '''
        self.phy_read()
        if len(self.msg) >= 1: # если считан по крайней мере 1 байт
          self.channnel_start_detect()
          '''
          обрабатывам сообщение после получения стопового байта
          '''
          if self.msg[-8:]==config.stop_byte:  # найден стоповый байт
            if len(self.msg)  >16: # стартовый байт уже не не считан
                self.is_begin=False # нет смысла проводить проверку на стартовый байт
                if self.reciever_True==1: # сообщение пришло по адресу
                    self.channel_reciever_true()

                else:
                    if self.reciever_True==0:
                        self.channel_reciever_false()
                    else:
                        pass
            if self.check_uplink_false():
                return None
            print("message from "+str(int(self.bin_char(int(self.port_num1)),2))+"-->"+str(int(self.bin_char(int(self.port_num2)),2))+" adresat: "+str(int(self.supposed_reciever,2))+" type: "+self.msg[16:24])
            self.msg = ""
            # Заготовка для новой строки
            self.ser1.flushInput()



  '''
  '''
  def send(self, msg1): # функция окончательной отправки сообщения в выходной порт
    #print('                                '+self.port_num2)
    #msg_final=data_.port_write_query(self.port_num2,msg1)
    print("msg sent to port"+'COM'+msg1[16:24]+str(self.ser2.dtr))
    if self.ser2.dtr: # если на COM порте установлен сигнал "готов к приему"
        try: # проверяем,
            self.ser2.write(msg1 + '\n') # записываем сообщение в выходной COM порт
        except: # предохраням программу от исключений(попытка записи в закрытый COM порт)
            pass


  def bin_char(self,char): # преобразуем число из десятичного  вида в байт - строку
        char=bin(char)
        char_fixed=char[2:]
        a1='0'
        if len(char_fixed)!=7:
            for i in range(7-len(char_fixed)):
                a1=a1+'0'
        char_fixed_final=a1+char_fixed
        #print char_fixed_final
        return char_fixed_final

  def onRcvd(self, msg):
        type=msg[-4:]
        msg=msg[:-4]
        if type=="data":
            sender=msg[24:32]
            print("who sended :                                                 "+str(int(str(sender),2)))
            decoded_into_bits=code_decode1.Decode(msg[40:-10])
            print("decoded_into_bits : ",decoded_into_bits)
            if decoded_into_bits!=False or True:
                reshifer(str(decoded_into_bits))
                try:
                    msgs_all[''+str(int(sender))].append(unicode(reshifer(msg), encoding="UTF-8"))
                except:
                    print(reshifer(msg))
                    print (str(len(msg[40:-10]))+" vs "+msg[32:40])
                    msgs_all[''+str(int(sender))]=[unicode(reshifer(msg), encoding="UTF-8")]
                    for my in config.alpha:
                        print("my.portnum1 "+ my.portnum1+ "sender "+sender)
                        if (my.portnum2)==str(int(str(sender),2)):
                            print("msg finaly delivered :)")
                            if len(msg)>0:
                                my.txtHist.append(unicode(reshifer(msg), encoding="UTF-8"))
                                msg_ack=config.start_byte+sender+config.get_code('ack')+msg[8:16]+config.stop_byte
                                self.send (msg_ack) # посылаем сигнал о приеме сообщения,

                try:
                    for my in config.alpha:
                        print("my.portnum2"+my.portnum2)
                except:
                    print("someth_wrong                                   vvvvvvvvv           vvvvvvvvv        vvvvvv")
        if type=="ackk":
            msg1=int(str(msg),2)
            print("ack                                   recieved   ",msg1)
            for my in config.alpha:
                # print(str(int(my.portnum2)+1))
                if int(my.portnum2)==msg1:
                        my.ackRcv()
                        print("**************************************")


def reshifer(arr): # функция расшифровки сообщения
    #if str(arr[0:8])=="10000001":
    text=str(arr[40:-10]) # получаем информационную часть сообщения
    #else:
        #text=str(arr)
    #print(len(arr))
    i=len(text)/8 # получаем количество байт
    ans=''
    for k in range(i): # проходимся по байтам
        text_new=int(text[k*8:k*8+8],2) # получаем байт
        ans=ans+ str(chr(text_new)) # расшифровываем символ из байта и добавляем его в строку
    return ans # возвращаем расшифрованное слово


