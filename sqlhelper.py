# -*- coding: utf-8 -*-
"""
Created on Tue May  1 23:47:59 2018

@author: 李莘
"""

import pymysql

LOCALHOST = "localhost"
USER = "root"
PASSWORD = "108955"
DBNAME = "myapp"



def getDBversion(db):
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
     
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute("SELECT VERSION()")
     
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
     
    return "Database version : %s " % data

    
def insert(sql, values = None):
    
    succeed = True
    if not sql:
        return 
    if not values:
        pass
    else:
        sql = sql % values
        #print(sql)
    try:
        db= pymysql.connect(LOCALHOST, USER, PASSWORD,  DBNAME)
        cursor = db.cursor()
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        succeed = False
        print('insert error...')
        #raise
    finally:
        # 关闭数据库连接
        db.close()
        return succeed
        
        
def select_all(sql, values = None):
    if not values:
        pass
    else:
        sql = sql % values
        #print(sql)
    try:
        db= pymysql.connect(LOCALHOST, USER, PASSWORD,  DBNAME)
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        results = None
        print("select all error...")
    finally:
        db.close()
        return results
    
def select_one(sql, values = None):
    if not values:
        pass
    else:
        sql = sql % values
        #print(sql)
    try:
        db= pymysql.connect(LOCALHOST, USER, PASSWORD,  DBNAME)
        cursor = db.cursor()
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchone()
    except:
        result = None
        print("select all error...")
    finally:
        db.close()
        return result

def test():
    
    sql = r"select * from t_user where nickname = '%s' and pwd = '%s';"
    val = ('abc', '123')
    
    r = select_one(sql, val)
    
    # SQL 查询语句
    print(not r)










