# -*- coding:utf8 -*-

import urllib
import os

def reporthook(blocks_read,block_size,total_size):
	if not blocks_read:
		print 'connection opend'
		return
 	if total_size < 0:
 		print 'read %d blocks (%d bytes)' % (blocks_read,blocks_read*block_size)
 	else:
 		amount_read = blocks_read*block_size
 		print 'read %d blocks, or %d/%d' %(blocks_read,amount_read,total_size)
 	return

 

try:
 	filename,msg = urllib.urlretrieve('http://www.sina.com.cn/',reporthook=reporthook)
 	print
 	print 'file: ',filename
 	print 'headers: '
 	print msg
 	print 'file exits before clean up: ',os.path.exists(filename)
finally:
 	urllib.urlcleanup()
 	print 'file still exists: ',os.path.exists(filename)