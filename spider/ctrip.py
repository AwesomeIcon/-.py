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
if os.path.exists('sightlist.txt') == False:
	fp = open('sightlist.txt','w')
	fp.write('景点名称,城市,城市编号,国家/地区(中文),国家/地区(英文),国家编号\n')
else:
	fp = open('sightlist.txt','a')

total = len(countrylist)
for i, el in enumerate(countrylist):
	# 爬取每个国家的城市列表
	print u'已完成',i + 1,'/',total,u',正在爬取',el[1].decode('utf8'),el[2],u',编号',el[0]
	# 断点续传
	# if i < 4:
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
	countrysightlist_pattern = re.compile('<a href="/sightlist/(.*?).html" target="_blank">(.*?)景点速览',re.S)
	countrysightlist = re.findall(countrysightlist_pattern, countrysightlist_html)
	sightlist = []
	# 第一页内容
	if len(countrysightlist) == 0:
		continue
	else:
		for sight in countrysightlist:
			sightlist.append(sight)
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
			countrysightlist = re.findall(countrysightlist_pattern, countrysightlist_html)
			for sight in countrysightlist:
				sightlist.append(sight)
			time.sleep(0.1)
	print u'已发现',el[1].decode('utf8'),u'有',len(sightlist),u'个城市,正在收录...'
	# 爬取每个城市的景点列表
	for s in sightlist:
		sight_url = 'http://you.ctrip.com/sightlist/' + s[0] + '.html'
		try:
			request = urllib2.Request(sight_url, headers = headers)
			response = urllib2.urlopen(request)
		except Exception,e:
			print e
			print sight_url
			continue
		sight_html = response.read()
		sight_pattern = re.compile('<i class="sight"></i>(.*?)<a target="_blank" href="/sight/(.*?).html" title="(.*?)">(.*?)</a>',re.S)
		sights = re.findall(sight_pattern, sight_html)
		if len(sights) == 0:
			continue
		for name in sights:
			fp.write(','.join([name[2],s[1],s[0],el[1],el[2],el[0]]) + '\n')
		# 页数
		sight_page = re.findall(countrysightlist_page_pattern, sight_html)
		if len(sight_page) != 0:
			pages_sight = int(sight_page[0])
			for p in xrange(2, pages_sight + 1):
				sight_url = 'http://you.ctrip.com/sightlist/' + s[0] + '/s0-p' + str(p) + '.html'
				try:
					request = urllib2.Request(sight_url, headers = headers)
					response = urllib2.urlopen(request)
				except Exception,e:
					print e
					print sight_url
					continue
				sight_html = response.read()
				sights = re.findall(sight_pattern, sight_html)
				for name in sights:
					fp.write(','.join([name[2],s[1],s[0],el[1],el[2],el[0]]) + '\n')
				time.sleep(0.1)
fp.close()
# f.close()