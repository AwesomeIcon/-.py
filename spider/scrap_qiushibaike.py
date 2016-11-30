import urllib2
import re

class Spider:
	def __init__(self):
		self.pageIndex = 1
		self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
		self.headers = {'User-Agent':self.user_agent}
	def getPage(self):
		url = 'http://www.qiushibaike.com/hot/page/' + str(self.pageIndex)
		request = urllib2.Request(url,headers = self.headers)
		response = urllib2.urlopen(request)
		content = response.read()
		pattern = re.compile('<div class="article.*?>.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>(.*?)<div class="stats">.*?<i .*?>(.*?)</i>.*?<i .*?>(.*?)</i>.*?</div>',re.S)
		data = re.findall(pattern,content)
		print 'Page:',self.pageIndex
		for item in data:
			haveImg = re.search("img",item[2])
			if not haveImg:
				print  'Title:',item[0]
				print item[1].strip()
				print 'vote:',item[3],'comments:',item[4]
				print 
	def loadPage(self):
		while True:
			input = raw_input('Enter Q to quit:')
			if input == "Q":
				return
			else:
				self.getPage()
				self.pageIndex += 1


spider = Spider()
spider.loadPage()