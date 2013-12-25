#!/usr/bin/python
import booruInitializer
import linkGenerator
import sourceParser
import sourceRequester
import linkDownloader
import threading


def work(appObject):
        appObject.enabler('DISABLED')
        printToLabel(appObject, 'Gathering links to all the pages...')
        objectList = booruInitializer.initialize(appObject.cacheSites)
        pageLinks = linkGenerator.generateLinks(objectList, appObject.cacheTags)

        imageLinkDictionary = {}

        # gathering links to the images we want
        visited = 0
        for page in pageLinks[0]:
                if appObject.is_running:
                        pageSource = sourceRequester.getSource(page)
                        currentPageDictionary = sourceParser.parse(pageSource)

                        for key in currentPageDictionary.keys():
                                if not key in imageLinkDictionary:
                                        imageLinkDictionary[key] = currentPageDictionary[key]
                        visited += 1
                        printToLabel(appObject, 'Visited %d out of %d pages so far.\nGot %d links to unique images so far.'
                                     % (visited, len(pageLinks[0]), len(imageLinkDictionary)), freeEndLine = 0)
                else:
                        # cancel button was hit
                        printToLabel(appObject, "Link gathering cancelled")
                        appObject.enabler('NORMAL')
                        return None

        # download images
        llink = list(imageLinkDictionary.values())
        l_thread = []

        # spawn multiple threads
        for i_thread in range(appObject.num_threads):
                dl_thread = threading.Thread(target = downloadWorker, args = (appObject, llink))
                l_thread.append(dl_thread)
                dl_thread.start()

        # wait for all threads to finish
        for dl_thread in l_thread:
                dl_thread.join()


        appObject.enabler('NORMAL')
        printToLabel(appObject, "Downloading terminated, %d links remaining" % (len(llink)))


def printToLabel(mainApp, string, color = 'black', freeLine = 1, freeEndLine = 1):
        if freeLine == 1: string = '\n' + string
        if freeEndLine == 1: string += '\n'
        mainApp.messageLabel['text'] = string
        mainApp.messageLabel['foreground'] = color


def downloadWorker(app_obj, llink):
        while len(llink) != 0:
                if app_obj.is_running:
                        try:
                                link = llink.pop()   # atomic operation
                                linkDownloader.download(app_obj.cacheDestination, link)
                                printToLabel(app_obj, "Downloading... %d links remaining" % (len(llink)))
                        except:
                                # llink is empty, this could happen due to some kind of race condition
                                return None
                else:
                        printToLabel(app_obj, "Threads exiting due to cancellation, be patient...")
                        return None
