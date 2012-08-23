#!/usr/bin/python
import xml.dom.minidom, json, os
from lxml import etree
from StringIO import *
def parserXML(source):  
    mapping = {}
    for ev, el in etree.iterparse(StringIO(source)):
	    if el.tag == 'post':
		        mapping[el.attrib['md5']] = el.attrib['file_url']
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
