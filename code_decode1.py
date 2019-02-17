__author__ = 'Work'
class Loop:
    def __init__(self,Object):
        self.Object=Object
        self.Syndrome = {'001':1, '010':2, '100':4, '011':8, '110':16, '111':32, '101':64}
cicle_codes=["0000000","0001011","0010110","0011101","0100111","0101100","0110001","0111010","1000101","1001110","1010011","1011000","1100010","1101001","1110100","1111111"]

"0000000000101100101100011101010011101011000110001011101010001011001110101001110110001100010110100111101001111111"

def Code(msg):
        if msg!="":
            return msg+Xor(msg,bin(int(msg,2) << 3)[2:].zfill(7))
        else:
            return ""

def Xor(msg, *args):
    temp_div = ""
    temp = ""
    if len(args) == 1:
        temp_div = "1011"
        temp = args[0]
    elif 3 > len(args) > 1:
        temp = args[0]
        temp_div = args[1]
    else: assert AttributeError, "AttributeError in func.Xor"
    while(True):
        temp = bin(int(temp[:4],2)^int(temp_div,2))[2:] + temp[4:]
        need = temp.find("1")
        if len(temp) < 4:
            return temp.zfill(3)
        temp = temp[need:]

def Code_all(msg):
    result=""
    for i in range(int(len(msg)/4)):
        result=result+Code(msg[4*i:4*i+4])#msg[4*i:4*i+4])
    return result

def Decode(msg):
        result=""
        for i in range(int(len(msg)/7)):
                sub_=msg[7*i:7*i+7]
                if sub_ in cicle_codes and len(sub_)>0:
                    result=result+sub_[0:4]
                else:
                    return False
        return result

print("coded: ",Code_all('0101000010100001010000101000010100001010000101000010100001010000101000'))
print ("decoded: ",Decode(Code_all('0101000010100001010000101000010100001010000101000010100001010000101000')))

