# -*- coding: utf-8 -*-
"""
Created on Tue May  1 00:10:26 2018

@author: 李莘
"""

#客户端实现
import socket
import threading 
from PIL import Image
import matplotlib.pyplot as plt

IP = '127.0.0.1'
PORT = 10002
BUFFER_SIZE = 1024

def run_th(sock):
    while True:
        data=str(sock.recv(BUFFER_SIZE),"utf8")
        print(data)
        break
    
sock=socket.socket()
address=(IP, PORT)
sock.connect(address)

message = {'name':'哈哈哈', 'password':'108955','phone':'1234567','email':'qq@qq.com'}
sock.sendall(bytes(str(message), 'utf8'))

rt = threading.Thread(target = run_th, args=(sock,))
rt.setDaemon(True)
rt.start()
