# -*- coding: cp1251 -*-
__author__ = 'Work'
import sys
from PyQt5 import QtGui
import dialog_window
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import admin_window
import admin_manage
import main
num_wins=1
import config
import user_menu_window




def create_dialog(port_num1,port_num2,main_obg,user_name,main_terminal): # ������������ ������������
    global num_wins
    if num_wins==1: # ������������ ��������������
        config.ports_all['real_user_name'].append(user_name) # ��������� � ���� ���� � ���������������� ����� ��������� ��� ������������
        global childwin # ������� ���������� ���������� ��� ������������� ���� ���� ������������ � ��� ������ � ����������� �����
        extract_(port_num1, port_num2, main_obg)
        childwin = user_menu_window.Ui_Dialog(port_num1,port_num2,user_name) # �������������� ���������� ���������� �������� ���� ������������
        config.connected_ports.append(bin_char(int(port_num1))) # ����� �������� ����� ���������� � ���������������� ���� � ������ ������������ ������
        config.connected_ports.append(bin_char(int(port_num2))) # ����� ��������� ����� ���������� � ���������������� ���� � ������ ������������ ������

        childwin.show() # ��������� ����������� ���� ������ ����
        config.users_.append(childwin)
        num_wins=num_wins+1 # �������������� ������� ���������� �������������

        # ��������� ����� ��� ��������������, ��������� � ��������������� ���� �������������� � ���� ������������-��������������
        config.admin_port1=childwin.ser1 # ������ �������� ����� �������������� ���������� � ���������������� ����
        config.admin_port2=childwin.ser2 # ������ ��������� ����� �������������� ���������� � ���������������� ����
        config.admin_port_num=int(port_num1) # ����� �������� ����� ��������������  ���������� � ����������������� ����
        config.main_terminal=main_terminal # ������ �� ���� �������������� ���������� � ����������������� ����


    else:# ������� ������������, ��� �� �� �����, �� ����������� ��������� ����� ��� ��������������
        if num_wins==2:
            config.ports_all['real_user_name'].append(user_name)
            global childwin2
            extract_(port_num1, port_num2, main_obg)
            childwin2 = user_menu_window.Ui_Dialog(port_num1,port_num2,user_name)
            childwin2.show()
            config.users_.append(childwin2)
            num_wins=num_wins+1
            extract_(port_num1,port_num2,main_obg)
        else:
            if num_wins==3:
                config.ports_all['real_user_name'].append(user_name)
                global childwin3
                extract_(port_num1, port_num2, main_obg)
                childwin3 = user_menu_window.Ui_Dialog(port_num1,port_num2,user_name)
                childwin3.show()
                config.users_.append(childwin3)
                num_wins=num_wins+1
                extract_(port_num1,port_num2,main_obg)
            else:
                if num_wins==4:
                    config.ports_all['real_user_name'].append(user_name)
                    global childwin4
                    extract_(port_num1, port_num2, main_obg)
                    childwin4 = user_menu_window.Ui_Dialog(port_num1,port_num2,user_name)
                    childwin4.show()
                    config.users_.append(childwin4)

                    for i in config.users_:
                        i.init_combo()

                    num_wins=num_wins+1
                    extract_(port_num1,port_num2,main_obg)

                else:
                    if num_wins==5:
                        config.ports_all['real_user_name'].append(user_name)
                        global childwin5
                        extract_(port_num1, port_num2, main_obg)
                        childwin5 = user_menu_window.Ui_Dialog(port_num1,port_num2,user_name)
                        childwin5.show()
                        config.users_.append(childwin5)
                        num_wins=num_wins+1
                        extract_(port_num1,port_num2,main_obg)

def bin_char(char): # ����������� ����� �� �����������  ���� � ���� - ������
        char=bin(char) # ����������� ����� �� �����������  ���� � ��������
        char_fixed=char[2:] # ������� ��������������� �������
        a1='0'
        if len(char_fixed)!=7:
            for i in range(7-len(char_fixed)):
                a1=a1+'0'
        char_fixed_final=a1+char_fixed #��������� ������ ������������ ������ �� �����-������
        #print char_fixed_final
        return char_fixed_final # ���������� ����-������

def extract_(port_num1,port_num2,main_obg): #changes the array of ports in data_
    config.connected_ports.append(bin_char(int(port_num1))) # ����� �������� ����� ���������� � ���������������� ���� � ������ ������������ ������
    config.connected_ports.append(bin_char(int(port_num2))) # ����� ��������� ����� ���������� � ���������������� ���� � ������ ������������ ������
    index1=config.ports_all['pairs'].index(port_num1)
    index2=config.ports_all['pairs'].index(port_num2)
    config.ports_all['real_enter'].append(port_num1)
    config.ports_all['real_exit'].append(port_num2)
    port_num1_1='COM'+str(port_num1)
    port_num2_1='COM'+str(port_num2)
    if index1 % 2 == 0:
        index1=index1+1
    else:
        index1=index1-1
    if index2 % 2 == 0:
        index2=index2+1
    else:
        index2=index2-1
    index1=config.ports_all['pairs'][index1]
    index2=config.ports_all['pairs'][index2]
    for i in config.ports_all['suposed_enter']:
        print(i)
    print("\n")
    for i in config.ports_all['suposed_exit']:
        print(i)

    print([port_num1_1,port_num2_1,index1])
    print([port_num1_1, port_num2_1, index2])
    config.ports_all['suposed_enter']=list(filter(lambda x:x not in [port_num1_1,port_num2_1,index1],config.ports_all['suposed_enter']))
    config.ports_all['suposed_exit']=list(filter(lambda x:x not in [port_num1_1,port_num2_1,index2],config.ports_all['suposed_exit']))

        # print(i)
    main_obg.init_combos()