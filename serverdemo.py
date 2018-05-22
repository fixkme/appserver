# -*- coding: utf-8 -*-
"""
Created on Wed May  2 10:21:54 2018

@author: 李莘
"""

#服务端实现
import socket
import threading 
import socketserver  # 导入socketserver模块

IP = '127.0.0.1'
PORT = 10002
LOCALHOST = (IP, PORT)
BUFFER_SIZE = 1024

client_addr = [] 
client_socket = []

  
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):  
  
    timeout = 4
    
    def setup(self):  
        ip = self.client_address[0].strip()     # 获取客户端的ip  
        port = self.client_address[1]           # 获取客户端的port  
        self.request.settimeout(self.timeout)   # 对socket设置超时时间
        print(ip+":"+str(port)+" is connect!")  
        client_addr.append(self.client_address) # 保存到队列中  
        client_socket.append(self.request)      # 保存套接字socket
    
    def handle(self):  
        while True: # while循环  
            data = str(self.request.recv(1024), 'ascii')  
            if data:    # 判断是否接收到数据  
                cur_thread = threading.current_thread()  
                response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')  
                self.request.sendall(response)
                
    def finish(self):  
        print("client is disconnect!")
        client_addr.remove(self.client_address)  
        client_socket.remove(self.request)
  
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):  
    pass  
  
def client(ip, port, message):  
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  
        sock.connect((ip, port))  
        sock.sendall(bytes(message, 'ascii'))  
        response = str(sock.recv(1024), 'ascii')  
        print("Received: {}".format(response))  
  
if __name__ == "__main__":  
    # Port 0 means to select an arbitrary unused port  
  
    server = ThreadedTCPServer(LOCALHOST, ThreadedTCPRequestHandler)  
    ip, port = server.server_address  
  
    # Start a thread with the server -- that thread will then start one  
    # more thread for each request  
    server_thread = threading.Thread(target=server.serve_forever)  
    # Exit the server thread when the main thread terminates  
    server_thread.daemon = True  
    server_thread.start()  
    print("Server loop running in thread:", server_thread.name)  
  
    client(ip, port, "Hello World 1")  
    client(ip, port, "Hello World 2")  
    client(ip, port, "Hello World 3")  
    print("\nclient_addr:"+str(client_addr))
    server.shutdown()  
    server.server_close()