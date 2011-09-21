"""
Created on 21 Aug 2011

@author: shana

This module aims to put all the *booru sites into a single file
"""
import helpers

def getLinks(tag, hFile = ''):
    """
    Take a tag argument and use predetermined values to return a list will links to all images.
    
    Returns: list - list of links to all images accross *booru websites
    """
    allImageLinks = []
    
    #gelbooru.com
    print('Gelbooru.')
    rawLink = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=100&tags='
    imagePattern = helpers.re.compile(r'file_url="(http://\w+\.gelbooru\.com/images/\d+/\w+\.\w+)".+md5="(\w+)"')
    pageFlag = '&pid='
    for link in helpers.obtainFileLinks(tag, rawLink, imagePattern, pageFlag):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))
   
    #konachan.com
    print('Konachan.')
    rawLink = 'http://konachan.com/post/index.xml?limit=100&tags='
    imagePattern = helpers.re.compile(r'file_url="(http://\w+\.\w+\.\w+/\w+/(\w+)/[A-z0-9_%.-]+\.\w+)"')
    pageFlag = '&page='
    for link in helpers.obtainFileLinks(tag, rawLink, imagePattern, pageFlag):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))
    
    #ichijou.org
    print('ichijou')
    rawLink = 'http://ichijou.org/post/index.xml?limit=100&tags='
    imagePattern = helpers.re.compile(r'file_url="(http://ichijou.org/\w+/\w+/\w+/(\w+)\.\w+)"')
    pageFlag = '&page='
    for link in helpers.obtainFileLinks(tag, rawLink, imagePattern, pageFlag):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))

    #danbooru.donmai.us
    print('Danbooru.')
    rawLink = 'http://danbooru.donmai.us/post/index.xml?limit=100&tags='
    imagePattern = helpers.re.compile(r'file_url="(http://\w+\.\w+\.\w+/\w+/(\w+)\.\w+)"')
    pageFlag = '&page='
    for link in helpers.obtainFileLinks(tag, rawLink, imagePattern, pageFlag):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))

    #chan.sankakucomplex.com
    print('Sankaku Complex.')
    rawLink = 'http://chan.sankakucomplex.com/post/index.xml?tags='
    rawJSONLink = 'http://chan.sankakucomplex.com/post/index.json?tags='
    imagePattern = helpers.re.compile(r'"md5":"(\w+)"[a-z:,"0-9]+"file_url":"(http://chan\.sankakustatic\.com/data/\w\w/\w\w/\w+\.\w+)",')
    pageFlag = '&page='
    for link in helpers.obtainFileLinksJSON(tag, rawLink, imagePattern, pageFlag, rawJSONLink):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))
    
    #safebooru.org
    print('Safebooru.')
    rawLink = 'http://safebooru.org/index.php?page=dapi&s=post&q=index&tags='
    imagePattern = r'file_url="(http://safebooru\.org/images/\d+/\w+\.\w+).+md5="(\w+)"'
    pageFlag = '&pid='
    for link in helpers.obtainFileLinks(tag, rawLink, imagePattern, pageFlag):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))

    
    #nekobooru.net
    print('Nekobooru.')
    rawLink = 'http://nekobooru.net/post/index.xml?tags='
    rawJSONLink = 'http://nekobooru.net/post/index.json?tags='
    imagePattern = helpers.re.compile(r'"md5":"(\w+)"[a-z:,"0-9]+"file_url":"(http://nekobooru\.net/data/\w\w/\w\w/\w+\.\w+)",')
    pageFlag = '&page='
    for link in helpers.obtainFileLinksJSON(tag, rawLink, imagePattern, pageFlag, rawJSONLink):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))

    #moe.imouto.org
    print('Moe Imouto.')
    rawLink = 'http://oreno.imouto.org/post/index.xml?tags='
    imagePattern = helpers.re.compile(r'file_url="(http://\w+\.\w+\.\w+/\w+/(\w+)/[A-z0-9_%.-]+\.\w+)"')
    pageFlag = '&page='
    for link in helpers.obtainFileLinks(tag, rawLink, imagePattern, pageFlag, linksPerPage = 16):
        allImageLinks.append(link)
    print('Links so far: {0}'.format(len(allImageLinks)))
    
    #Remove duplicates based on recovered MD5
    linkDictionary = {}
    for tup in allImageLinks:
        #Make keys based on MD5, ignore repeating keys
        if not tup[1] in linkDictionary:
            linkDictionary[tup[1]] = tup[0]
    
    
    existingMD5list = []
    if not hFile == '':
        try:
            for line in open(hFile, 'r'):
                existingMD5list.append(line[:-1])
        except:
            pass
    
    for k in list(linkDictionary.keys()):
        if k in existingMD5list:
            del linkDictionary[k]
    
    #Put links back in a list
    allImageLinks = list(linkDictionary.values())
    print('Finished *booru tasks. Returning {0} links.'.format(len(allImageLinks)))
    return allImageLinks

if __name__ == '__main__':
    print(len(getLinks('trefoil')))
