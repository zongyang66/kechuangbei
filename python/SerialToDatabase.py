import serial
import struct
import pymysql
from time import sleep


ser = serial.Serial()
db = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='caizongyang', db='new_schema', charset='utf8mb4')
cursor = db.cursor()

#开启串口
def port_open_recv():
    ser.port='com7'
    ser.baudrate=9600
    ser.bytesize=8
    ser.stopbits=1
    ser.parity="N"
    ser.open()
    if(ser.isOpen()):
        print("串口打开成功！")
    else:
        print("串口打开失败！")

#关闭串口
def port_close():
    ser.close()
    if(ser.isOpen()):
        print("串口关闭失败！")
    else:
        print("串口关闭成功！")
        
#串口发送数据
def send(send_data):
    if(ser.isOpen()):
        data = bytes.fromhex(send_data);
        ser.write(data);
        print("发送成功",)
    else:
        print("发送失败！")

#发送数据至数据库
def sendtodb(data1,data2,data3,data4):
    try:
        sql = "INSERT INTO newtable_2(temp,humi, weight,lignt_level,time) VALUES (%s,%s,%s,%s,NOW())"
        print(data1,data2,data3,data4)
        VALUES = (data1,data2,data3,data4)
        print(sql)
        cursor.execute(sql,VALUES)
        
        db.commit()
    except:
        print("fail")
        db.rollback()




#串口接收单片机数据
def serial_receice_data():
    com_input = ser.read(1)  
    if struct.unpack('@B',com_input)[0] == 255:#检测数据包的开头
        com_input = ser.read(16)#接收16位数据
        data = struct.unpack('@BBBBBBBBBBBBBBBB',com_input)
        datapack_1 = data[0:4]
        datapack_2 = data[4:8]
        datapack_3 = data[8:12]
        datapack_4 = data[12:16]#将数据进行分类
        
        com_input = ser.read(1)
        
        if struct.unpack('@B',com_input)[0] == 255:#检测数据包的结尾
            if datapack_1 == datapack_3 and datapack_2 == datapack_4:#数据校验（数据发送了两次，将两个数据进行比较，排除数据传输过程中的干扰信号的影响）
                print("data vaild!");#数据有效
                
                temp = (datapack_1[2] << 8) + datapack_1[3]
                sendtodb(datapack_1[0],datapack_1[1],temp,datapack_2[0])




#主函数
if __name__ == '__main__':
    port_open_recv()#打开串口
    count = 0
    while 1:
        serial_receice_data()
        count = count + 1
        print(count)

        
    
    
    
    
    