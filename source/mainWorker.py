#!/usr/bin/python
import booruInitializer
import linkGenerator
import sourceParser
import sourceRequester
import linkDownloader

def work(appObject):
	appObject.enabler('DISABLED')
	printToLabel(appObject, 'Gathering links to all the pages...')
	objectList = booruInitializer.initialize(appObject.cacheSites)
	pageLinks = linkGenerator.generateLinks(objectList, appObject.cacheTags)
	
	imageLinkDictionary = {}

	visited = 0
	for page in pageLinks[0]:
		pageSource = sourceRequester.getSource(page)
		currentPageDictionary = sourceParser.parse(pageSource) 
		
		for key in currentPageDictionary.keys():
			if not key in imageLinkDictionary:
				imageLinkDictionary[key] = currentPageDictionary[key]
		visited += 1
		printToLabel(appObject, 'Visited %d out of %d pages so far.\nGot %d links to unique images so far.' % (visited, len(pageLinks[0]), len(imageLinkDictionary)), freeEndLine = 0)
	
	downloaded = 0

	for link in imageLinkDictionary.values():
		linkDownloader.download(appObject.cacheDestination, link)
		downloaded += 1
		printToLabel(appObject, 'Downloaded %d out of %d images.' % (downloaded, len(imageLinkDictionary.values())))
	
	printToLabel(appObject, 'Finished.\nDownloaded %d images.' % downloaded, freeEndLine = 0)
	appObject.enabler('NORMAL')

def printToLabel(mainApp, string, color = 'black', freeLine = 1, freeEndLine = 1):
	if freeLine == 1: string = '\n' + string
	if freeEndLine == 1: string += '\n'
	mainApp.messageLabel['text'] = string
	mainApp.messageLabel['foreground'] = color
	
	
