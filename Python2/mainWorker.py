#!/usr/bin/python
import source.booruInitializer as booruInitializer
import source.linkGenerator as linkGenerator
import source.sourceParser as sourceParser
import source.sourceRequester as sourceRequester
import source.linkDownloader as linkDownloader

if __name__ == '__main__':
	tag = 'cirno+cum'
	saveDestination = '/home/shanachan/test - %s' % tag
	listOfSites = {
					'gelbooruCheck': 		1,
					'konachanCheck': 		1,
					'ichijouCheck': 		1,
					'danbooruCheck': 		1,
					'sankakuComplexCheck': 	1,
					'safebooruCheck': 		1,
					'nekobooruCheck': 		1,
					'moeImoutoCheck': 		1
				}
	
	objectList = booruInitializer.initialize(listOfSites)
	pageLinks = linkGenerator.generateLinks(objectList, tag)
	
	imageLinkDictionary = {}

	visited = 0
	for page in pageLinks[0]:
		pageSource = sourceRequester.getSource(page)
		currentPageDictionary = sourceParser.parse(pageSource) 
		
		for key in currentPageDictionary.keys():
			if not key in imageLinkDictionary:
				imageLinkDictionary[key] = currentPageDictionary[key]
		visited += 1
		print 'Visited %d out of %d pages so far. Got %d links to unique images so far.' % (visited, len(pageLinks[0]), len(imageLinkDictionary))
	
	downloaded = 0
	for link in imageLinkDictionary.values():
		linkDownloader.download(link, saveDestination)
		downloaded += 1
		print 'Downloaded %d out of %d images.' % (downloaded, len(imageLinkDictionary.values()))
	
	

