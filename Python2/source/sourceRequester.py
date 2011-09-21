#!/usr/bin/python
"""
This module requests the web page and returns source.
"""
import urllib

def getSource(link):
	if link.find('http://') < 0:
		link = 'http://' + link
	
	source = ''
	tried = 0
	while tried < 4:
		try:
			source = urllib.urlopen(link).read()
		except:
			tried += 1
			continue
		break
	
	return source	
