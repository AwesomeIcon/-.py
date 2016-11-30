# -*- coding:utf8 -*-
import urllib2
import re
import os
import sys
import httplib

class dota:
	def __init__(self):
		self.url = "http://www.dota2.com.cn/heroes/";
		self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
	def getHero(self):
		request = urllib2.Request(self.url,headers = self.headers)
		response = urllib2.urlopen(request)
		Heroes = response.read()
		pattern = re.compile('<a.*?heroPickerIconLink.*?href="(.*?)">',re.S)
		hero_href = re.findall(pattern,Heroes)
		i = 1
		for href in hero_href:
			hero_pattern = re.compile('/hero/(.*?)/',re.S)
			hero_name = re.search(hero_pattern,href).group(1)
			path = '/home/developer/Pictures/' + hero_name
			print u'正在爬取第',i,u'位英雄',hero_name,u'的信息'
			self.mkdir(path,hero_name)
			self.getHeroInfo(href,path)
			i = i + 1
		print u'所有英雄已就位！'
	def getHeroInfo(self,href,path):
		httplib.HTTPConnection._http_vsn = 10
		httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
		request = urllib2.Request(href,headers = self.headers)
		response = urllib2.urlopen(request)
		heroInfo = response.read()
		httplib.HTTPConnection._http_vsn = 11
		httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
		story_box = re.compile('<div class="story_pic">.*?</div>(.*?)</div>',re.S)
		story = re.search(story_box,heroInfo).group(1).strip()
		story_file = open(path + '/' + u'故事背景' + '.txt','w+')
		print u'正在保存英雄故事背景'
		story_file.write(story)
		story_file.close()
		skill_intro = re.compile('<img class="skill_b" src="(.*?)".*?<p class="skill_intro">.*?<span>(.*?)</span><br/>(.*?)</ul>',re.S)
		skill = re.findall(skill_intro,heroInfo)
		for skill_name in skill:
			print u'正在保存技能',skill_name[1]
			skill_img = skill_name[0]
			req = urllib2.Request(skill_img,headers = self.headers)
			try:
				res = urllib2.urlopen(req)
			except:
				print u'技能所提供的链接为',skill_img,'不是个链接'
				continue
			skill_img_data = res.read()
			skill_img_file = open(path + '/' + skill_name[1] + '.png','wb')
			skill_img_file.write(skill_img_data)
			skill_img_file.close()
			skill_body = Tool().replace(skill_name[2])
			skill_body_file = open(path + '/' + skill_name[1] + '.txt','w+')
			skill_body_file.write(skill_body)
			skill_body_file.close()
		hero_prop = re.compile('<ul class="pro6_box">(.*?)</ul>',re.S)
		hero_prop_data = re.search(hero_prop,heroInfo).group(1).strip()
		print u'正在保存英雄属性'
		hero_prop_file = open(path + '/' + u'英雄属性' + '.txt','w+')
		hero_prop_file.write(Tool().replace(hero_prop_data))
		hero_prop_file.close()
		print 

	def mkdir(self,path,name):
		path = path.strip()
		isExist = os.path.exists(path)
		if not isExist:
			print u'正在创建名为',name,u'的文件夹'
			os.makedirs(path)	
			return True
		else:
			print u'名为',name,u'的文件夹已存在'
			return False

class Tool:
    	removeImg = re.compile('<img.*?>| {7}|')
    	removeAddr = re.compile('<a.*?>|</a>')
    	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    	replaceTD= re.compile('<td>')
    	replacePara = re.compile('<p.*?>')
    	replaceBR = re.compile('<br><br>|<br>')
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

dota_obj = dota()
dota_obj.getHero()
