#!/usr/bin/python
"""
This module will get the initial number of links in minimal time and generate links to every page.
"""
import sourceRequester, re

def generateLinks(listOfSiteObjects, tag):
	pageLinkList = []
	totalNumberOfImages = 0
	for obj in listOfSiteObjects:
		if obj.queryType == 'JSON':
			#Retrieve source of the regular page
			temporarySource = sourceRequester.getSource(obj.siteRoot + '?tags=%s' % tag)
			
			try:
				searchResult = re.search(r'<link href="/post\?page=(\d+)&amp;tags=%s" rel="last" title="Last Page"' % tag, temporarySource).groups()
			except:
				continue

			temporarySource = sourceRequester.getSource(obj.siteRoot + '?tags=%s' % tag + obj.pageFlag + searchResult[0])
			
			numberOfImages = (20 * (int(searchResult[0]) - 1)) + len(re.findall(r'Post\.register\(\{', temporarySource))

			totalNumberOfImages += numberOfImages

			for pageNumber in [p + 1 for p in range(numberOfImages / 20 + 1) if True]:
				pageLinkList.append(obj.siteRoot + obj.siteQuery + tag + obj.pageFlag + str(pageNumber))

		elif obj.queryType == 'XML':
			temporarySource = sourceRequester.getSource(obj.siteRoot + obj.siteQuery + tag + '&limit=1')
			try:
				numberOfImages = int(re.search(r'<posts count="(\d+)" offset="0">', temporarySource).groups()[0])
			except:
				continue

			totalNumberOfImages += numberOfImages
		
			for pageNumber in [p + 1 for p in range(numberOfImages / 100 + 1) if True]:
				pageLinkList.append(obj.siteRoot + obj.siteQuery + tag + obj.pageFlag + str(pageNumber))

	return (pageLinkList, totalNumberOfImages)
			
			
			
