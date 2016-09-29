# -*- coding:utf8 -*-
import os
import time
import cookielib
import threading
import re
import urllib2
import sys
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

reload(sys)
sys.setdefaultencoding('utf8')

print '\033[1;34m*************************************************************************'
print ' > Author: huangjunqin'
print ' > Mail: uestc_ccse@outlook.com'
print ' > Version: 0.1.0'
print '*************************************************************************\033[0m\n'

class Comic:
    def __init__(self,url):
        self.url = url
        self.cookie = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(self.opener)
        self.headers = [{'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                         'Host':'ac.tc.qq.com',
                         'Accept':'*/*',
                         'Accept-Language':'en-US,en;q=0.5',
                         'Accept-Encoding':'gzip, deflate',
                         'Referer':url,
                         'Connection':'keep-alive'
                        },
                        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                         'Host':'ac.tc.qq.com',
                         'Accept':'*/*',
                         'Accept-Language':'en-US,en;q=0.5',
                         'Accept-Encoding':'gzip, deflate',
                         'Referer':url,
                         'Connection':'keep-alive'
                        },
                        {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                         'Host':'ac.tc.qq.com',
                         'Accept':'*/*',
                         'Accept-Language':'en-US,en;q=0.5',
                         'Accept-Encoding':'gzip, deflate',
                         'Referer':url,
                         'Connection':'keep-alive'
                        },
                        {'User-Agent': 'Mozilla/5.0',
                         'Host':'ac.tc.qq.com',
                         'Accept':'*/*',
                         'Accept-Language':'en-US,en;q=0.5',
                         'Accept-Encoding':'gzip, deflate',
                         'Referer':url,
                         'Connection':'keep-alive'
                        },
                        {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                         'Host':'ac.tc.qq.com',
                         'Accept':'*/*',
                         'Accept-Language':'en-US,en;q=0.5',
                         'Accept-Encoding':'gzip, deflate',
                         'Referer':url,
                         'Connection':'keep-alive'
                        }
                       ]

    def getLink(self):
        for key, value in enumerate(random.choice(self.headers)):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
        driver = webdriver.PhantomJS(executable_path='/home/huangjunqin/phantomjs/bin/phantomjs')
        driver.get(self.url)
        WebDriverWait(driver,5).until(lambda x: x.find_element_by_id("crossPage")).click()
        WebDriverWait(driver,5).until(lambda x: x.find_elements(By.XPATH,"//img[@data-pid]"))
        time.sleep(3)
        imgs = driver.find_elements(By.XPATH,"//img[@data-pid]")
        i = len(imgs)
        pattern = re.compile('》(.*?)-'.decode('utf8'),re.S)
        comic_title = re.search(pattern,driver.title).group(1)
        lock = threading.Lock()
        for img in imgs:
            img_url = img.get_attribute("src")
            if img_url is None:
                img_url = img.get_attribute("data-src")
            t = threading.Thread(target=self.saveFile,args=(img_url,comic_title,i,lock))
            t.start()
            i -= 1;
        driver.close()

    def saveFile(self,url,name,i,lock):
        isExist = os.path.exists('/home/huangjunqin/Documents/' + name)
        if not isExist:
            lock.acquire()
            if not isExist:
                print '\033[1;32m'
                print '+ mkdir ', '\033[0m' ,name ,u' 共' ,i ,'P'
                os.makedirs('/home/huangjunqin/Documents/' + name)
            lock.release()
        print '\033[1;32m','+ Saving','\033[0m', url
        img_url = open('/home/huangjunqin/Documents/' + name + '/' + str(i) + ".jpg",'w+')
        request = urllib2.Request(url,headers=random.choice(self.headers))
        data = urllib2.urlopen(request).read()
        img_url.write(data)
        img_url.close()

while 1:
    comic_url = raw_input("输入想要保存的漫画链接:")
    Comic(comic_url).getLink()
    go_on = raw_input('是否继续保存下一话(Y/N):').lower()
    if go_on == 'y':
        continue
    else:
        break
