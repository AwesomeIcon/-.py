# -*- coding:utf-8 -*-
import urllib2
import re
import chardet
import sys
import os

class MM:
	def __init__ (self):
		self.url = 'https://mm.taobao.com/json/request_top_list.htm?page=1'
		self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
	def getInfo(self):
		request = urllib2.Request(self.url,headers = self.headers)
		response = urllib2.urlopen(request)
		content = self.ZhongWen(response.read())
		list_item = re.compile('<div class="pic-word">.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
		MM_list = re.findall(list_item,content)
		num = 1
		for mm in MM_list:
			print u'正在偷偷为你爬取第',num,u'位美女信息'
			path = 'https:' + mm[0].strip()
			print u'芳名:',mm[2].strip()
			print u'芳龄',mm[3].strip()
			print u'个人主页:',path
			print u'照片链接:',mm[1].strip()
			print u'来自',mm[4].strip()
			print u'将为你保存',mm[2].strip(),u'个人主页照片'
			self.getImg(path,mm[2].strip())
			print '---------------------------------------------------------------------'
			num += 1
	def ZhongWen(self,html_content):
		typeEncode = sys.getfilesystemencoding()
		infoEncode = chardet.detect(html_content).get('encoding','utf-8')
		html = html_content.decode(infoEncode,'ignore').encode(typeEncode)
		return html
	def getImg(self,Imgurl,name):
		response = urllib2.urlopen(Imgurl)
		data = response.read()
		pattern = re.compile('<div class="mm-aixiu-content" id="J_ScaleImg">(.*?)<!--',re.S)
		aixiu = re.search(pattern,data)
		src = re.compile('<img.*?src="(.*?)"',re.S)
		allImg = re.findall(src,aixiu)
		print name,u'共有',len(allImg),u'张私密照'
		path = '/home/developer/Pictures/' + name
		self.mkdir(path,name)
		num = 1
		for img in allImg:
			toSaveUrl = urllib2.urlopen('https:' + img)
			imgContent = toSaveUrl.read()
			filename = path + str(num) + '.jpg'
			print u'正在保存第',num,u'张图片'
			f = open(filename,'wb')
			f.write(imgContent)
			f.close()
	def mkdir(self,path,name):
		path = path.strip()
		isExist = os.path.exist(path)
		if not isExist:
			print u'正在创建名为',name,u'的文件夹'
			os.makedirs(path)	
			return true
		else:
			print u'名为',name,u'的文件夹已存在'
			return false
mm = MM()
mm.getInfo()