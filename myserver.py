# -*- coding: utf-8 -*-
"""
Created on Tue May  1 00:10:13 2018

@author: 李莘
"""

#服务端实现
import socketserver  # 导入socketserver模块

class Myserver(socketserver.BaseRequestHandler):  # 定义一个类名继承自socketserver.BaseRequestHandler
    def handle(self):  # 自定义一个函数名handle（注意这个名字不能命名成别的名字，父类中有这个方法，相当于重写了这个方法）里面实现的是socket通信的逻辑代码块
        while True:
            conn=self.request
            while True:
                try:
                    data=str(conn.recv(1024),"utf8")
                    print("<<<",data)
                    data=bytes(input(">>>"),"utf8")
                    conn.sendall(data)
                except Exception as e:
                    print(e)
                    conn.close()
                    break

if __name__=="__main__":
    server=socketserver.ThreadingTCPServer(("127.0.0.1",10001),Myserver)  # 创建socketserver.ThreadingTCPServer实例，将地址及端口以及我们刚刚创建的类传递进去，这个类将会在客户端请求过来时threading一个线程来处理这个请求
    server.serve_forever()  # 调用实例的serve_forever方法