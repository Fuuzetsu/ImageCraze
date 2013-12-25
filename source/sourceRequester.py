#!/usr/bin/python
"""
This module requests the web page and returns source.
"""

# Python 2/3 hacks
urlmodule = None
fopener = None
import sys

header = "Mozilla/5.0 (X11; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0"

if sys.version_info[0] == 2:
    import urllib2
    urlmodule = urllib2
    o = urllib2.build_opener()
    o.addheaders = [('User-agent', header)]
    fopener = o
else:
    import urllib.request
    urlmodule = urllib.request

    class BooruURLopener(urlmodule.FancyURLopener):
        version = header

        def open(self, fullurl, data=None):
            return super(BooruURLopener, self).open(fullurl, data=data)

        def http_error_default(self, url, fp, errcode, errmsg, headers):
            print("%d error when fetching %s: %s" % (errcode, url, errmsg))
            return super(BooruURLopener, self).http_error_default(
                url, fp, errcode, errmsg, headers)

    fopener = BooruURLopener()


def getSource(link):
        if link.find('http://') < 0:
                link = 'http://' + link

        source = ''
        tried = 0
        max_tries = 3
        while tried <= max_tries:
            try:
                source = fopener.open(link).read()
            except urlmodule.URLError as e:
                if tried >= max_tries:
                    raise
                else:
                    print('URLError on %s' % link)
                    tried += 1
                continue
            break

        return source
