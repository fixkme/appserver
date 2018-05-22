# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 10:50:49 2018

@author: 李莘
"""

import os   
import re
import requests
from bs4 import BeautifulSoup as BS


u1 = "http://www.plantphoto.cn//list?latin="
u2 = "http://www.plantphoto.cn/list?keyword="

baidu_url = "http://baike.baidu.com/search/word?word="

head = {'user-agent' : 'Mozilla/5.0'} #浏览器身份标识

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"}

def getHTMLText(name, timeout = 30, headers = header):
    
    try:
        r = requests.get(baidu_url + name, timeout = 30, headers = headers)
        r.raise_for_status() #如果不是200引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except requests.ConnectionError as e:
        #raise e
        print("连接错误: " + str(e))
        return None
    except requests.HTTPError as e:
        print("HTTP错误： " + str(e))
        return None
    except requests.URLRequired as e:
        print("缺失url： " + str(e))
        return None
    except requests.ConnectTimeout as e:
        print("连接服务器超时： " + str(e))
        return None
    except requests.Timeout as e:
        print("请求url超时: " + str(e))
        return None
    except :
        print("产生异常")
        return None
    
def get_plant_figure(soup):
    name = soup.find("h1").string
    print('\t'+'植物名称：', name)
    img_url = ""
    try:
        p = soup.find("div", string = name+"图册").parent.parent
        img_tag = p.find("img")
        img_url = img_tag.attrs['src']
        print('\t'+'img_figure_url == ', len(img_url))
    except:
        pass
    '''
    img_content = requests.get(img_url, headers = head).content
    with open("./data/%s.jpg" % name, 'wb') as f:
        f.write(img_content) 
    '''
    return img_url
        
        
def get_basic_infos(soup):
    
    sp_name = ""    #拉丁学名
    nickname = ""   # 别称
    phylum = ""     # 门
    classis = ""    # 纲
    order = ""      # 目
    family = ""     # 科
    genus = ""      # 属
    classification = "植物界>" #植物界分类
    
    try:
        loc = soup.find('div', 'basic-info cmn-clearfix')
        judge = loc.find('dt', string='界').find_next_sibling('dd')
        if judge.text == '植物界':
            pass
    except:
        raise
    
    #拉丁学名
    b = loc.find('dt', string='拉丁学名')
    if b:
        sp_tag = b.find_next_sibling('dd')
        if not sp_tag.find('i'):
            sp_name = sp_tag.text.strip()
        else:
            sp_name = sp_tag.find('i').text.strip()
    print('\t'+sp_name)
    
    #别称
    bb = loc.find('dt', string='别\xa0\xa0\xa0\xa0称')
    if bb:
        nick_tag = bb.find_next_sibling('dd')
        nickname = nick_tag.text.strip().replace('\n','')
    print('\t'+nickname)
    
    #门
    b1= loc.find('dt', string='门')
    if b1:
        phylum_tag = b1.find_next_sibling('dd')
        phylum = phylum_tag.text.strip().replace('\n','')
        classification = classification + phylum + ">"
    print('\t'+phylum)
    
    #纲
    b2= loc.find('dt', string='纲')
    if b2:
        classis_tag = b2.find_next_sibling('dd')
        classis = classis_tag.text.strip().replace('\n','')
        classification = classification + classis + ">"
    print('\t'+classis)
    #目
    b3= loc.find('dt', string='目')
    
    if b3:
        order_tag = b3.find_next_sibling('dd')
        order = order_tag.text.strip().replace('\n','')
        classification = classification + order + ">"
    print('\t'+order)
    
    #科
    b4 = loc.find('dt', string='科')
    if b4:
        family_tag = b4.find_next_sibling('dd')
        family = family_tag.text.strip().replace('\n','')
        classification = classification + family + ">"
    print('\t'+family)
    
    #属
    b5 = loc.find('dt', string='属')
    if b5:
        genus_tag = b5.find_next_sibling('dd')
        genus = genus_tag.text.strip().replace('\n','')
        classification = classification + genus 
    print('\t'+genus)

    return sp_name, nickname, family, genus, classification


def get_describe_infos(soup):
    
    intro = ""      #介绍
    feature = ""    #形态特征
    effect = ""     #功能价值
    
    #介绍
    try:
        divs = soup.find('div', attrs={'label-module':'lemmaSummary'}).find_all('div', 'para')
        for div in divs:
            text = div.text
            if text.find('参考') != -1:
                continue
            sups = div.find_all('sup')
            for sup in sups:
                ds = sup.text + sup.find_next_sibling('a').text
                text = text.replace(ds, '').strip()
            
            intro = intro + text.replace('\n', '')
    except:
        pass
    print('\t'+'简单介绍：',len(intro))
    
    #形态特征
    try:
        loc = soup.find('a', attrs= {'name':'形态特征'})
        p = loc.parent
        fea_tag = p.find_next('div', 'para')
        
        while True:
            feature = fea_tag.text
            ds = ''
            for i in fea_tag.find_all('div'):
                ds = i.text
                text = text.replace(ds, '')
            
            for i in fea_tag.find_all(attrs={'class':'description'}):
                ds = i.text
                feature = feature.replace(ds, '')
            
            for i in fea_tag.find_all('sup'):
                ds = i.text
                feature = feature.replace(ds, '')
            feature = feature.strip().replace('\n','')
            
            if not feature:
                fea_tag = fea_tag.find_next_sibling('div', 'para')
            else:
                break
    except:
        pass
    print('\t'+'形态特征：',len(feature))
        
    #功能价值
    ds = ''
    try:
        loc = soup.find('a', attrs= {'name':'主要价值'})
        if not loc:
            loc = soup.find('a', attrs= {'name':'营养价值'})
        p = loc.parent
        effect_tag = p.find_next_sibling('div', 'para')
        while True:
            if effect_tag:
                text = effect_tag.text
            else:
                break
            for i in effect_tag.find_all('div'):
                ds = i.text
                text = text.replace(ds, '')
                
            for i in effect_tag.find_all(attrs={'class':'description'}):
                ds = i.text
                text = text.replace(ds, '')
                
            for i in effect_tag.find_all('sup'):
                ds = i.text
                text = text.replace(ds, '')
            effect = effect + text.strip().replace('\n','')
            
            tag = effect_tag.find_next_sibling('div')
            if tag:
                if tag.attrs.get('label-module') != "para":
                    #print('\n', tag.attrs)
                    break
                else:
                    effect_tag = effect_tag.find_next_sibling('div', 'para')
            else:
                break
    except:
        pass
    print('\t'+"价值：", len(effect))
    
    return intro, feature, effect
        
    
def get_img_urls(img_name, num = 60, n = 1):    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"    
    headers = {'User-Agent':user_agent}    
    try:  
        url = "http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=" + img_name.replace(' ','%20') + "&cg=girl&rn=" +str(num)+ "&pn=" +str(n*num)  
        r = requests.get(url, headers=headers)
        r.raise_for_status() #如果不是200引发HTTPError异常
        r.encoding = r.apparent_encoding
        page = r.text
        img_srcs = re.findall('"objURL":"(.*?)"', page, re.S)  
        
        for i in img_srcs:
            if not i.endswith('.jpg'):
                img_srcs.remove(i)
        print('\t'+img_name+'图片urls：',len(img_srcs))
    except:  
        print('\t'+img_name+'图片urls：'," error.")  
    
    return img_srcs



def test():

    word = "红花檵木"
    text = getHTMLText(word)
    soup = BS(text, "html.parser")
    get_plant_figure(soup)
    get_basic_infos(soup)
    get_describe_infos(soup)
    
    #print(r)


'''
n = get_img_urls('叶子花')
for i in n:
    print(i+'\n')
    

name = 'http://img.plantphoto.cn/image2/152/163238.jpg'
img_content = requests.get(name, headers = head).content
with open("./data/%s.jpg" % name.split('/')[-1], 'wb') as f:
    f.write(img_content)
    
    
'''







