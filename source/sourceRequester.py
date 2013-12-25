#!/usr/bin/python
"""
This module requests the web page and returns source.
"""

# Python 2/3 hacks
urlmodule = None
import sys
if sys.version_info[0] == 2:
        import urllib2
        urlmodule = urllib2
else:
        import urllib.request
        urlmodule = urllib.request

def replace_spaces(x):
    """
    Temporary function to hack up links with spaces to links with %20
    """
    return x.replace(' ', '%20')

def getSource(link):
        if link.find('http://') < 0:
                link = 'http://' + link

        source = ''
        tried = 0
        max_tries = 3
        while tried <= max_tries:
                try:
                        source = urlmodule.urlopen(replace_spaces(link)).read()
                except urlmodule.URLError as e:
                        if tried >= max_tries:
                            raise
                        else:
                            print('URLError on %s' % link)
                            tried += 1
                        continue
                break

        return source
