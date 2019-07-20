# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 23:22:21 2019

@author: roshan
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import re,json,os
import pandas as pd

url = "https://twitter.com/iamsrk"
#driver = webdriver.Chrome("D:/python/\chromedriver_win32/chromedriver.exe") 
#driver.get(url)

def twitter_wrapper(url):
    driver = webdriver.Chrome("D:/python/\chromedriver_win32/chromedriver.exe") 
    driver.get(url)
     
    #scrolling down...
    pause = 3    
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    #print(lastHeight)
    count = 1
    sub_url_lst =[]
    div_data_lst =[]#set()
    i = 0
    source =""
        
    driver.get_screenshot_as_file("srk"+".png")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        #print(newHeight)
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
        i += 1
    
        #extract JSON from web pages...
        source = BeautifulSoup(driver.page_source)
        for st in source.findAll('div'):
            try:
                
                if "content" in st["class"]:
                    sub_url_lst.append(st)
            except:
                pass
        
        for d in sub_url_lst:
            name,post,_datetime =[],'',''
            for d1 in d.findAll('strong'):
                name.append(d1.get_text())
                
            for d2 in d.findAll('p'):
                post = d2.get_text()
            for d3 in d.findAll('small'):
                for d4 in d3.findAll('a'):
                    _datetime = d4["title"]
            
            _name =name[0]
            if _datetime !='' and post !="":
                div_data_lst.append([_name,_datetime,post])
    
    df = pd.DataFrame(div_data_lst,columns=['name','datetime','post'])
    df.drop_duplicates(['post'],keep='first')
    df.to_csv("twitter_post.csv",index=False)
    driver.close()
    return df

twitter_wrapper(url)