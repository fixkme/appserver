# -*- coding: utf-8 -*-
"""
Created on Tue May  1 00:10:13 2018

@author: 李莘
"""

#服务端实现
import socket
import threading 
import socketserver  # 导入socketserver模块
import json
import sqlhelper 
import baike

IP = '192.168.191.4'
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
        #self.request.settimeout(self.timeout)   # 对socket设置超时时间
        print(ip+":"+str(port)+" is connect!")  
        client_addr.append(self.client_address) # 保存到队列中  
        client_socket.append(self.request)      # 保存套接字socket
    
    def handle(self):  
        while True: # while循环  
            data = str(self.request.recv(1024), 'utf8')  
            if data:    # 判断是否接收到数据  
                data_json = json.loads(data, encoding='utf-8')
                op = data_json.get("op")
                if op == "register":
                    if register(data_json):
                        response = bytes("注册成功", 'utf8')
                        print("{0} : {1} 注册成功".format(self.client_address[0], self.client_address[1]))
                    else:
                        response = bytes("注册失败", 'utf8')
                        print("{0} : {1} 注册失败".format(self.client_address[0], self.client_address[1]))
                elif op == "login":
                    if login(data_json):
                        response = bytes("登录成功", 'utf8')
                        print("{0} : {1} 登录成功".format(self.client_address[0], self.client_address[1]))
                    else:
                        response = bytes("登录失败", 'utf8')
                        print("{0} : {1} 登录失败".format(self.client_address[0], self.client_address[1]))
                elif op == "baike":
                    data = get_plant_data(data_json)
                    if data:
                        #print('\n\n\n', data)
                        response = bytes(json.dumps(data), 'utf8')
                        print("{0} : {1}获取百科数据成功".format(self.client_address[0], self.client_address[1]))
                    else:
                        response = bytes("获取百科数据失败", 'utf8')
                        print("{0} : {1}获取百科数据失败".format(self.client_address[0], self.client_address[1]))
                #cur_thread = threading.current_thread()  
                self.request.sendall(response)
                break
                
    def finish(self):  
        print("{0} : {1} is disconnect!".format(self.client_address[0], self.client_address[1]))
        client_addr.remove(self.client_address)  
        client_socket.remove(self.request)
        
  
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):  
    pass  
		
################################################################################
def register(user):
    name = user.get("name")
    password = user.get("password")
    phone = user.get("phone")
    email = user.get("emial")
    
    sql = r"insert into t_user (nickname, pwd, phone, email) values( '%s', '%s', '%s', '%s');"
    val = (name, password, phone, email)
    
    r = sqlhelper.insert(sql, val)
    return r
    
def login(user):
    name = user.get("name")
    password = user.get("password")
    
    sql = r"select * from t_user where nickname = '%s' and pwd = '%s';"
    val = (name, password)
    
    r = sqlhelper.select_one(sql, val)
    if not r:
        return False
    else:
        return True

def get_plant_data(data_json):
    
    res_json = {}
    
    plant_name = data_json.get('plant_name')
    count = data_json.get('count')
    
    html_page = baike.getHTMLText(plant_name)
    soup = baike.BS(html_page, "html.parser")
    if html_page:
        try:
            plant_figure_url = baike.get_plant_figure(soup)
            plant_basic_info = baike.get_basic_infos(soup)
            plant_des_info = baike.get_describe_infos(soup)
            plant_img_urls = baike.get_img_urls(plant_name, 30, int(count))
        except:
            
            return None
        res_json['figure_url'] = plant_figure_url
        res_json['basic_info'] = plant_basic_info
        res_json['describe_info'] = plant_des_info
        res_json['img_urls'] = plant_img_urls
        
    return res_json
	
if __name__ == "__main__":  
    # Port 0 means to select an arbitrary unused port  
  
    server = ThreadedTCPServer(LOCALHOST, ThreadedTCPRequestHandler)  
    ip, port = server.server_address  
    
    try:
        server.serve_forever()
        '''
        # Start a thread with the server -- that thread will then start one  
        # more thread for each request  
        server_thread = threading.Thread(target=server.serve_forever)  
        # Exit the server thread when the main thread terminates  
        server_thread.daemon = True  
        server_thread.start()  
        print("Server loop running in thread:", server_thread.name)  
    
        '''
        #print("\nclient_addr:"+str(client_addr))
        server.shutdown()  
        server.server_close()
        
    except:
        print("ERROR...")
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    