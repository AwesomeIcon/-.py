# -*- coding:utf-8 -*-
import urllib2
import re
import os

class baiduTP:
	def __init__(self,url):
		self.url = url
		self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
	def getImg(self,num = 1):
		request = urllib2.Request(self.url,headers = self.headers)
		response = urllib2.urlopen(request)
		Imgs = response.read()
		objURL = re.compile('"objURL":"(.*?)"',re.S)
		link = re.compile('</span></strong>(.*?)<div class="goto">',re.S)
		linkBlock = re.search(link,Imgs).group(1).strip()
		nextPage = re.compile('<a href="(.*?)"',re.S)
		allImg = re.findall(objURL,Imgs)
		nextLink = re.findall(nextPage,linkBlock)
		# print nextLink[3]
		for img in allImg:
			# print img.strip()
			try:
				Imgrequest = urllib2.Request(img.strip(),headers = self.headers)
				ImgtoSave = urllib2.urlopen(Imgrequest)
				data = ImgtoSave.read()
			except:
				print u'连接超时'
				num += 1
				continue
			print u'正在保存第',num,u'张图片'
			f = open('/home/developer/Pictures/' + str(num) + '.jpg','wb')
			f.write(data)
			f.close()
			num += 1
		input = raw_input("If continue(y/n):")
		if input == 'y':
			self.url = 'http://image.baidu.com' + nextLink[3]
			self.getImg(num)
		else:
			return

url = raw_input("Enter image.baidu URL:")
baiduTP = baiduTP(url)
baiduTP.getImg()