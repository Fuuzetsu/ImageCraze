#!/usr/bin/python
import xml.dom.minidom, json, os
from lxml import etree

import sys
decoder = None
if sys.version_info[0] == 2:
    decoder = lambda x: x
else:
    decoder = lambda x: x.decode('utf-8')

# For now we dirty hack like this around Python 2/3 compat issues
FileIO = None

import sys
if sys.version_info[0] == 2:
    from StringIO import StringIO
    FileIO = StringIO
else:
    from io import BytesIO
    FileIO = BytesIO


def parserXML(source):
    mapping = {}
    for ev, el in etree.iterparse(FileIO(source)):
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

        if decoder(source)[0] == '[':
                imageDictionary = parserJSON(source)
        elif decoder(source)[0] == '<':
                imageDictionary = parserXML(source)

        return imageDictionary
