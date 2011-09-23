#!/usr/bin/python
import xml.dom.minidom, json, os
def parserXML(xmlsource):
	temporaryFile = open('temp.xml', 'w')
	temporaryFile.write(xmlsource)
	temporaryFile.close()
	temporaryFile = open('temp.xml', 'r')
	doc = xml.dom.minidom.parse(temporaryFile)
	mapping = {}
	 
	for node in doc.getElementsByTagName('post'):
	  link = node.getAttribute('file_url')
	  md5 = node.getAttribute('md5')
	  mapping[md5] = link
	temporaryFile.close()
	os.remove('temp.xml')

	return mapping

def parserJSON(jsonsource):
	split = json.loads(jsonsource)
	mapping = {}

	for dictionary in split:
		link = dictionary['file_url']
		md5 = dictionary['md5']
		mapping[md5] = link

	return mapping
		

def parse(source):
	imageDictionary = {}
	if source[0] == '[':
		imageDictionary = parserJSON(source)
	elif source[0] == '<':
		imageDictionary = parserXML(source)

	return imageDictionary
