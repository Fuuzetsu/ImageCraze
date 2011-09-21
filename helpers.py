#!/usr/bin/python
"""
Created on 20 Aug 2011

@author: shana
Contact: ShanaLover on irc.rizon.net
This module contains helper functions usable with Python3 interpreters.
"""
import shutil, hashlib, platform, urllib, re, socket

def downloadFile(linkToFile, saveDestination, maxTries = 5):
    """
    This function takes a link to a file and a save destination to a file.
    It will download and save the file and return the path of the saved file.
    Will use regular urllib.request download if platform is not Linux.
    
    arguments: (linkToFile, saveDestination) -- link to a file and path to a directory
    keyword arguments: (maxTries = 5) -- number of tries before ditching the download. Default unlimited.
    
    Returns: string - path to the saved file
    """
    if not shutil.os.path.exists(shutil.os.path.join(saveDestination, shutil.os.path.split(linkToFile)[1])):
        if platform.system() == 'Linux':
            shutil.os.system('wget -q -nc -t %s -P %s %s' % (maxTries, saveDestination, linkToFile))
            return shutil.os.path.join(saveDestination, shutil.os.path.split(linkToFile)[1])
        #Must be on non-Linux system therefore no wget
        else:
            #Navigate to specified directory
            if not shutil.os.path.isdir(saveDestination):
                shutil.os.mkdir(saveDestination)
            originalDirectory = shutil.os.path.abspath(shutil.os.curdir)
            shutil.os.chdir(saveDestination)
            
            #Append http:// if necessary
            if not linkToFile.find('http://') == 0:
                linkToFile = 'http://' + linkToFile
            tried = 0
            while maxTries > tried:
                #Download the file
                try:
                    #Download the data and file size information
                    fileData = urllib.request.urlopen(linkToFile)
                    fileSize = int(fileData.headers['Content-Length'])
                    fileData = fileData.read()
                    
                    #Obtain file name
                    saveFileTo = shutil.os.path.split(linkToFile)[1]
                    
                    #Save the file
                    fileSaveObject = open(saveFileTo, 'wb')
                    fileSaveObject.write(fileData)
                    fileSaveObject.close()
                    
                    #Check that the file size matches
                    if not shutil.os.path.getsize(saveFileTo) == fileSize:
                        tried += 1
                        continue
                    else:
                        break
                except:
                    tried += 1
            #Go back to the initial directory
            shutil.os.chdir(originalDirectory)
            
            return shutil.os.path.join(saveDestination, shutil.os.path.split(linkToFile)[1])
    else:
        return 0


def obtainFileLinks(tag, rawLinkGiven, imagePattern, pageFlag, linksPerPage = 100):
    """
    Given a tag, this will return a list of links to images with this tag.
    
    Returns: list - list of links to download
    """
    
    #Helper function
    def extractImageLinks(source, pattern):
        """
        Takes a page source and returns a list of links to images contained in that source.
        
        Returns: list - list of links to images
        """
        #Find all image links in the source
        linksGroup = re.findall(pattern, source)
        
        #Put every image link in a list
        extractedLinks = []
        for item in linksGroup:
            extractedLinks.append(item)
        
        return list(set(extractedLinks))
    #end of helper function
    
    #Set timeout for socket operations
    socket.setdefaulttimeout(15)
    
    #Get initial number of images
    rawLink = '%s%s' % (rawLinkGiven, tag)
    tried = 0
    while tried < 4:
        try:
            source = urllib.request.urlopen(rawLink).read().decode("utf8", 'ignore')
        except:
            tried += 1
            continue
        break
    try:
        numberOfImages = int(re.findall(r'count="(\d+)" ', source)[0])
    except:
        return []
    
    #Establish total number of pages
    if numberOfImages == 0:
        return []
    else:
        numberOfPages = numberOfImages // linksPerPage
    
    #Generate a link to every page
    pageList = []
    for i in range(numberOfPages + 1):
        pageList.append('%s%s%s%s' % (rawLinkGiven, tag, pageFlag, i))
    
    #Get link to every image
    imageLinks = []
    tried = 0
    for page in pageList:
        while tried < 4:
            try:
                pageSource = urllib.request.urlopen(page).read().decode('utf8', 'ignore')
            except:
                tried += 1
                continue
            break
    
        for link in extractImageLinks(pageSource, imagePattern):
            imageLinks.append(link)
    
    #Return the complete list of links to the images
    return imageLinks
    
    
def obtainFileLinksJSON(tag, rawLinkGiven, imagePattern, pageFlag, rawJSONLinkGiven):
    """
    Given a tag, this will return a list of links to images with this tag.
    
    Returns: list - list of links to download
    """
    
    #Helper function
    def extractImageLinks(source, pattern):
        """
        Takes a page source and returns a list of links to images contained in that source.
        
        Returns: list - list of links to images
        """
        if source == '[]':
            return []
        #Find all image links in the source
        linksGroup = re.findall(pattern, source)
               
        
        #Put every image link in a list, flip tuples because of JSON ordering
        extractedLinks = []
        for item in linksGroup:
            extractedLinks.append((item[1], item[0]))
        
        return list(set(extractedLinks))
    #end of helper function
    
    #Set timeout for socket operations
    socket.setdefaulttimeout(15)
    
    #Get initial number of images
    rawLink = '%s%s' % (rawLinkGiven, tag)
    tried = 0

    while tried < 4:
        try:
            source = urllib.request.urlopen(rawLink).read().decode("utf8", 'ignore')
        except:
            tried += 1
            continue
        break
    try:
        numberOfImages = int(re.findall(r'count="(\d+)" ', source)[0])
    except:
        return []
    
    #Establish total number of pages
    if numberOfImages == 0:
        return []
    else:
        numberOfPages = (numberOfImages // 20) + 1
    
    #Generate a link to every page
    pageList = []
    for i in range(numberOfPages + 1):
        pageList.append('%s%s%s%s' % (rawJSONLinkGiven, tag, pageFlag, i))

    #Get link to every image
    imageLinks = []
    tried = 0
    for page in pageList:
        while tried < 4:
            try:
                pageSource = urllib.request.urlopen(page).read().decode('utf8', 'ignore')
            except:
                tried += 1
                continue
            break
    
        for link in extractImageLinks(pageSource, imagePattern):
            imageLinks.append(link)
    
    #Return the complete list of links to the images
    return imageLinks
