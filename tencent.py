# -*- coding:utf8 -*-
import os
import time
import urllib2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class Comic:
    def __init__(self,url):
        self.url = url
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

    def getLink(self):
        driver = webdriver.PhantomJS(executable_path='/home/huangjunqin/phantomjs/bin/phantomjs')
        driver.get(self.url)
        driver.find_element_by_id('crossPage').click()
        imgs = driver.find_elements(By.XPATH,"//img[@data-pid]")
        i = len(imgs)
        for img in imgs:
            img_url = img.get_attribute("src")
            if img_url is None:
                img_url = img.get_attribute("data-src")
            print img_url
            self.saveFile(img_url,driver.title,i)
            i -= 1;
        driver.close()

    def saveFile(self,url,name,i):
        isExist = os.path.exists(name)
        if not isExist:
            print u'+ mkdir ',name
            os.makedirs(name)
        img_url = open(name + '/' + str(i) + ".jpg",'w+')
        request = urllib2.Request(url,headers=self.headers)
        data = urllib2.urlopen(request).read()
        img_url.write(data)
        img_url.close()

while 1:
    comic_url = raw_input("The Comic Link is:")
    Comic(comic_url).getLink()
    go_on = raw_input('Continue Or Not(Y/N):').lower()
    if go_on == 'y':
        continue
    else:
        break
