# -*- coding: utf-8 -*-
"""
Created on Tue May  1 00:10:26 2018

@author: 李莘
"""

#客户端实现
import socket  # 这块代码和上面的基本一致，可以参照上面的注释解释
sk=socket.socket()
address=("127.0.0.1",10001)
sk.connect(address)
while True:
    data=bytes(input(">>>"),"utf8")
    if str(data,"utf8")=="exit":
        sk.close()
        break
    sk.sendall(data)
    data=str(sk.recv(1024),"utf8")
    print("<<<",data)
