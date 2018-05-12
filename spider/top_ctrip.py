# -*- coding:utf8 -*-

import re
import urllib2
import time
import os

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}

# 爬取国家/地区列表
country_list_url = 'http://you.ctrip.com/place/countrylist.html'
request = urllib2.Request(country_list_url, headers = headers)
response = urllib2.urlopen(request)
countrylist_html = response.read()
countrylist_pattern = re.compile('<li><a href="/place/(.*?).html">(.*?)</a> <span>(.*?)</span></li>',re.S)
countrylist = re.findall(countrylist_pattern, countrylist_html)

# f = open('countrylist.txt','w') # china110000,中国,China
if os.path.exists('top_sightlist.txt') == False:
	fp = open('top_sightlist.txt','w')
	fp.write('景点名称,城市,城市编号,国家/地区(中文),国家/地区(英文),国家编号\n')
else:
	fp = open('top_sightlist.txt','a')

total = len(countrylist)
for i, el in enumerate(countrylist):
	# 爬取每个国家的城市列表
	print u'已完成',i + 1,'/',total,u',正在爬取',el[1].decode('utf8'),el[2],u',编号',el[0]
	# 断点续传
	# if i < 64:
	# 	continue
	# f.write(el[0] + ',' + el[1] + ',' + el[2] + '\n')
	countrysightlist_url = 'http://you.ctrip.com/countrysightlist/' + el[0] + '.html'
	try:
		request = urllib2.Request(countrysightlist_url, headers = headers)
		response = urllib2.urlopen(request)
	except Exception,e:
		print e
		print countrysightlist_url
		continue
	countrysightlist_html = response.read()
	# 获取到每个list模块
	list_mod1_pattern = re.compile('<div class="list_mod1">(.*?)</dl>(.*?)</div>',re.S)
	countrysightlist_pattern = re.compile('<a href="/sightlist/(.*?).html" target="_blank">(.*?)景点速览',re.S)
	topsight_pattern = re.compile('<dd class="ellipsis">(.*?)推荐景点：(.*?)</dd>',re.S)
	singlesight_pattern = re.compile('<a href="/sight/(.*?).html" target="_blank">(.*?)</a>',re.S)
	countrysightlist_mod_html = re.findall(list_mod1_pattern, countrysightlist_html)
	sightlist = 0
	for html in countrysightlist_mod_html:
		countrysightlist = re.findall(countrysightlist_pattern, html[0])
		topsight_data = re.findall(topsight_pattern, html[0])
		# 第一页内容
		if len(topsight_data) != 0:
			sightlist = sightlist + 1
			topsight = re.findall(singlesight_pattern, topsight_data[0][1])
			for item in topsight:
				fp.write(','.join([item[1],countrysightlist[0][1],countrysightlist[0][0],el[1],el[2],el[0]]) + '\n')
	# 页数
	countrysightlist_page_pattern = re.compile('<b class="numpage">(.*?)</b>',re.S)
	countrysightlist_page = re.findall(countrysightlist_page_pattern, countrysightlist_html)
	if len(countrysightlist_page) != 0:
		pages_countrysightlist = int(countrysightlist_page[0])
		for p in xrange(2, pages_countrysightlist + 1):
			countrysightlist_url = 'http://you.ctrip.com/countrysightlist/' + el[0] + '/p' + str(p) + '.html'
			try:
				request = urllib2.Request(countrysightlist_url, headers = headers)
				response = urllib2.urlopen(request)
			except Exception,e:
				print e
				print countrysightlist_url
				continue
			countrysightlist_html = response.read()
			countrysightlist_mod_html = re.findall(list_mod1_pattern, countrysightlist_html)
			for html in countrysightlist_mod_html:
				countrysightlist = re.findall(countrysightlist_pattern, html[0])
				topsight_data = re.findall(topsight_pattern, html[0])
				if len(topsight_data) != 0:
					sightlist = sightlist + 1
					topsight = re.findall(singlesight_pattern, topsight_data[0][1])
					for item in topsight:
						fp.write(','.join([item[1],countrysightlist[0][1],countrysightlist[0][0],el[1],el[2],el[0]]) + '\n')
			time.sleep(0.1)
	print u'已收录',el[1].decode('utf8'),u'的',sightlist,u'个城市的top景点'
fp.close()
# f.close()