# -*- coding: cp1251 -*-
__author__ = 'Work'

#com_ports=['COM4','COM5','COM6']
ports=[]
std_speeds = ['9600','1843200', '921600', '460800', '230400', '115200', '57600', '38400', '19200', '4800', '2400', '1200', '600', '300', '150', '100', '75', '50'] #
data_bits=['8','5','6','7']
paritys = ['N', 'E', 'O']
stop_bits=['1','0.5','2']

start_byte='10000001'
stop_byte='01111110'
admin_port_num=0



signals_codes=[
    {
    'name':'info',
    'code':'00000001',
    'msg':'10000001000101010000000101111110'
    },
    {
    'name':'link',
    'code':'00000010',
    'msg':'10000001000101010000001001111110',
    },
    {
    'name':'uplink',
    'code':'00000011'
    },
    {
    'name':'set',
    'code':'00000100'
    },
    {
    'name':'ack',
    'code':'00000101'
    },
    {
    'name':'err',
    'code':'00000111'
    },
    {
    'name':'off',
    'code':'00001000'
    },

            ]

b=['COM17','9600','8','1','N']
ext_readed=[]
connected_ports=[]
connected_ports1=[]


ports_all={
    #'pairs':['21','22','23','24','25','26','27','28','7','8'],
    #'suposed_enter':['COM21','COM22','COM23','COM24','COM25','COM26','COM27','COM28','COM7', 'COM8'],
    'pairs':[],
    'suposed_enter':[],
    'real_enter':[],
    #'suposed_exit':['COM21','COM22','COM23','COM24','COM25','COM26','COM27','COM28', 'COM7', 'COM8'],
    'suposed_exit':[],
    'real_exit':[],
    'real_user_name':[],
}

timers={
    'link':0,
    'is_link':False,
}

sleep_={
    'link':20,
}

admin_port1=0
admin_port2=0

alpha=[]
users_=[]

main_terminal=0

def get_code(name):
    for i in signals_codes:
        if i['name'] == name:
            return i['code']
    return signals_codes[len(signals_codes)-1]['code']

DTRs=[]

write_query=[]
write_data_query=[]

def port_write_query(port_num,msg_):
    for i in DTRs:
        if i['port_num1']==port_num:
            if len(msg_)>0:
                i['data'].append(msg_)
            if i['is_DTR']:
                try:
                    return i['data'][0]
                except:
                    return False
            return False

isLink=False


