# -*- coding: cp1251 -*-
__author__ = 'Work'
import time


class Phy():
    def __init__(self,ser1):
        self.ser1=ser1


    def port_read(self,msg,isDTR):
        try:
            byte = str(self.ser1.read())    # Читаем один байт
        except:
            pass
        if len(byte) == 1:
          msg += byte               # Составляем строку
          if time.time()-self.timer>=1:
              isDTR=True
          else:
                isDTR=False
                self.ser1.setDTR(False)
          self.timer=time.time()

