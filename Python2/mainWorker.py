#!/usr/bin/python
import source.booruInitializer as booruInitializer
import source.linkGenerator as linkGenerator
import source.sourceParser as sourceParser
import source.sourceRequester as sourceRequester
import source.linkDownloader as linkDownloader
import source.directoryCreator as directoryCreator
import sys

if __name__ == '__main__':
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
	if len(sys.argv) < 3:
		print 'Not enough arguments. The arguments are save destination and a tag. Example:\nmainWorker.py /home/user/cirno/ cirno+rating:safe'
		sys.exit(1)
	else:
		tag = sys.argv[2]
		saveDestination = sys.argv[1]
	
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
	directoryCreator.createDirectory(saveDestination)
	for link in imageLinkDictionary.values():
		linkDownloader.download(link)
		downloaded += 1
		print 'Downloaded %d out of %d images.' % (downloaded, len(imageLinkDictionary.values()))
	
	

