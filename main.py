# -*- coding: cp1251 -*-

from PyQt5.QtWidgets import QApplication
import sys  # We need sys so that we can pass argv to QApplication
import admin_manage
import index

need_dialog=False

def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form1 = admin_manage.ExampleApp()  # We set the form to be our ExampleApp (design)
    form1.show()  # Show the form
    app.exec_()  # and execute the app



if __name__ == '__main__':  # if we're running file directly and not importing it
    app = QApplication(sys.argv)  # A new instance of QApplication
    form1=index.InitialWindow() # создаем главное окно
    form1.show() # выводим его на экран
    app.exec_()  # and execute the app

