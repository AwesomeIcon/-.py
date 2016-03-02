# -*- coding:utf8 -*-
import chardet,sys
import urllib2

response = urllib2.urlopen('http://www.huangjunqin.com/')
print 'response:', response
print 'url            :',response.geturl()

headers = response.info()
print 'date         :',headers['date']
print 'headers  :'
print '-------------'
print headers

data = response.read()
sysEncode = sys.getfilesystemencoding()
infoEncode = chardet.detect(data).get('encoding','utf-8')
html = data.decode(infoEncode,'ignore').encode(sysEncode)
print 'length      :',len(data)
print 'data         :'
print '--------------'
print html
