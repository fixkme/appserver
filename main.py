# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 19:16:07 2018

@author: 李莘
"""

from bs4 import BeautifulSoup  
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys  
import time  

root = "http://www.plantphoto.cn"
u1 = "http://www.plantphoto.cn/list?latin="
u2 = "http://www.plantphoto.cn/list?keyword="
word = "叶子花"


header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"}
url = 'http://www.kfc.com.cn/kfccda/storelist/index.aspx'  
  
driver = webdriver.PhantomJS()  
# 也可以使用Firefox驱动，区别在于有无界面的显示  
# driver = webdriver.Firefox()  
  
# driver.implicitly_wait(10) # 隐式等待  
  
driver.get("http://www.plantphoto.cn/sp/12485")    
  
# 线程休眠，和隐式等待的区别在于前者执行每条命令的超时时间是一样的而sleep()只会在调用时wait指定的时间  
time.sleep(10)
t = driver.page_source
g = driver.find_elements_by_class_name('img')

for i in g:
    m = i.find_element_by_tag_name('img')
    print(m.get_attribute('src'))

with open('./data/mmm.html', 'w') as f:
    f.write(t)
  
print(len(g)) 



driver.close()




