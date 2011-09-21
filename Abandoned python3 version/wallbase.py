"""
Created on 21 Aug 2011

@author: shana

Wallbase back-end
"""

import helpers, re, queue, threading, time

MAX_THREADS = 3

def getLinks(tag):
    thumbLinkList = getThumbLinks(tag)
    if thumbLinkList == []:
        return []
    thumbQueue = queue.Queue()
    for link in thumbLinkList:
        thumbQueue.put(link)
    links = []
    grabLink(thumbQueue, links)
    #Now we should have links full of links
    
    return links
    

def getThumbLinks(tag):
    #Make a search based on a tag
    n = helpers.urllib.request.Request('http://wallbase.cc/search/%s/213/eqeq/0x0/0/111/60/relevance/wallpapers/0' % tag)
    n.add_header('Cookie', 'is_adult=1')
    tried = 0
    while tried < 3:
        try:
            n = str(helpers.urllib.request.urlopen(n).read())
        except:
            tried += 1
            continue
        break
    
    #Get number of images are reported by wallbase
    numberOfImages = int(re.search('Search.vars.results_count = (\d+);', n).groups()[0])
    
    #Get links from first(current) page
    links = []
    l = re.findall('a href="(http://wallbase.cc/wallpaper/\d+)"', n)
    for link in l:
        links.append(link)
    
    #Generate all other page links and put them in a queue
    i = 1
    pageQueue = queue.Queue()
    while not i > (numberOfImages//60):
        pageQueue.put('http://wallbase.cc/search/%s/213/eqeq/0x0/0/111/60/relevance/wallpapers/%d' % (tag, i * 60))
        i += 1
    
    #Decide on amount of threads to start and start extracting links to the wallpapers    
    if pageQueue.qsize() > MAX_THREADS and pageQueue.qsize() > 0:
        for i in range(MAX_THREADS):
            t = threading.Thread(target = extractLinks, args = (pageQueue, links))
            t.start()
            time.sleep(0.01)
    else:
        for i in range(pageQueue.qsize()):
            t = threading.Thread(target = extractLinks, args = (pageQueue, links))
            t.start()
            time.sleep(0.01)
            
    #Hold up until only one (main) thread is active
    while threading.active_count() > 1:
        pass

    #Should have all the links now, return a unique list
    return list(set(links))
    
    
def extractLinks(pageQueue, links):    
    #Get links from generated pages
    while pageQueue.qsize() > 0:
        page = pageQueue.get()

        n = helpers.urllib.request.Request(page)
        n.add_header('Cookie', 'is_adult=1')
        
        #Keep trying to get the source
        while True:
                try:
                    n = str(helpers.urllib.request.urlopen(n).read())
                except:
                    continue
                break
        #Pull out all the links to the source that holds wallpaper address and report a finished task    
        for link in re.findall('a href="(http://wallbase.cc/wallpaper/\d+)"', n):
            links.append(link)
        pageQueue.task_done()


def grabLink(thumbQueue, links):
    #Pulls out link
    while thumbQueue.qsize() > 0:
        #Get link to source from the queue
        tNum = thumbQueue.get()
        req = helpers.urllib.request.Request(tNum)
        req.add_header('Cookie', 'is_adult=1')
        
        #Keep trying to connect and read the source
        while True:
            try:
                linkedSource = str(helpers.urllib.request.urlopen(req).read())
            except:
                continue
            break
    
        #Pull out link to large image
        wallLink = re.search(r"http://wallbase\d*.org/[A-z-_]+/\w+/\w+-\d+.\w+", linkedSource)

        
        #If it is missing any information, it probably screwed up with getting the source, skip it
        if wallLink == None:
            return None
        
        #Put the data in a list that will later be used to download the images and report finished task
        links.append(wallLink.group())
        thumbQueue.task_done()



