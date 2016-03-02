import robotparser
import urlparse

AGENT_NAME = 'huangjunqin'
URL_BASE = 'http://www.huangjunqin.com'
parser = robotparser.RobotFileParser()
parser.set_url(urlparse.urljoin(URL_BASE,'robots.txt'))
parser.read()

PATHS = [
	'/',
	'/PyMOTW/',
	'/admin/',
	'/downloads/PyMOTW-1.92.tar.gz',
]

for path in PATHS:
	print '%6s : %s' % (parser.can_fetch(AGENT_NAME,path),path)
	url = urlparse.urljoin(URL_BASE,path)
	print '%6s : %s' % (parser.can_fetch(AGENT_NAME,url),url)
	print