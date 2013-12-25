"""
Booru class that aims to encapsulate different booru sites in a clean way.
"""

import re

class Booru:
        def __init__(self, siteName, siteRoot, siteQuery, pattern, pageFlag, queryType):
                self.siteName = siteName
                self.siteRoot = siteRoot
                self.siteQuery = siteQuery
                self.pageFlag = pageFlag
                self.imagePattern = re.compile(pattern)
                self.queryType = queryType
