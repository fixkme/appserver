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

    
def insert(cursor, sql, values = None):
    
    if not sql:
        return 
    if not values:
        pass
    else:
        sql = sql % values
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()
        
def selectAll(cursor, sql):
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        results = None
    finally:
        return results
    
def selectOne(cursor, sql):
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchone()
    except:
        result = None
    finally:
        return result
 
# 打开数据库连接
db= pymysql.connect(LOCALHOST, USER, PASSWORD,  DBNAME)
    
cursor = db.cursor()
 
# SQL 查询语句
sql = "select * from t_user;"
r = selectAll(cursor, sql)
print(r)
# 关闭数据库连接
db.close()










