# -*- coding:utf8 -*-
import urllib2
import re

class baiduTB:
	def  __init__ (self,baseURL,see_lz):
		self.baseURL = baseURL
		self.see_lz = '?see_lz=' + str(see_lz)
		self.file = None
	def getPage(self,pageNum,floor):
		url = self.baseURL + self.see_lz + '&pn=' + str(pageNum)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		content = response.read()
		pattern_3 = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		body = re.findall(pattern_3,content)
		if body:
			print u'正在爬取第',pageNum,u'页'
			for post in body:
				floorline = str(floor) + '楼---------------------------------------------------------------------------------------------------\n'
				postitem = Tool().replace(post) + '\n'
				self.file.write(floorline)
				self.file.write(postitem)
				floor += 1
		else:
			print 'None'
		return floor
	def loadPage(self,pageNum):
		floor = 1
		page = int(pageNum)
		url = self.baseURL + self.see_lz + '&pn=' + str(pageNum)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		content = response.read()
		pattern_1 = re.compile('<div class="core_title_bg j_core_title_bg"></div><h3 .*?>(.*?)</h3>',re.S)
		pattern_2 = re.compile('<li class="l_reply_num" .*?><span class="red" .*?>(.*?)</span>.*?<span class="red">(.*?)</span>.*?</li>',re.S)
		title = re.search(pattern_1,content)
		sumpage = re.search(pattern_2,content)
		self.file = open(title.group(1).strip() + '.txt','w+')
		print u'标题',title.group(1).strip(),sumpage.group(1).strip(),u'回复贴,共',sumpage.group(2).strip(),u'页'
		maxpage = sumpage.group(2).strip()
		while page <= int(maxpage):
			floor = self.getPage(page,floor)
			page += 1
		print '-------------------------------------------------------------------------------'
		print u'爬取完毕!'


class Tool:
    	#去除img标签,7位长空格
    	removeImg = re.compile('<img.*?>| {7}|')
    	#删除超链接标签
    	removeAddr = re.compile('<a.*?>|</a>')
    	#把换行的标签换为\n
    	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    	#将表格制表<td>替换为\t
    	replaceTD= re.compile('<td>')
    	#把段落开头换为\n加空两格
    	replacePara = re.compile('<p.*?>')
    	#将换行符或双换行符替换为\n
    	replaceBR = re.compile('<br><br>|<br>')
    	#将其余标签剔除
    	removeExtraTag = re.compile('<.*?>')
    	def replace(self,x):
        		x = re.sub(self.removeImg,"",x)
        		x = re.sub(self.removeAddr,"",x)
        		x = re.sub(self.replaceLine,"\n",x)
        		x = re.sub(self.replaceTD,"\t",x)
        		x = re.sub(self.replacePara,"\n    ",x)
        		x = re.sub(self.replaceBR,"\n",x)
        		x = re.sub(self.removeExtraTag,"",x)
        		return x.strip()

		


baseURL = 'http://tieba.baidu.com/p/3138733512'
print u'只看楼主请按1，否则请按0:'
see_lz = raw_input()
baidu = baiduTB(baseURL,see_lz)
print u'从第几页开始:'
fromWhere = raw_input()
baidu.loadPage(fromWhere)