"""
Created on 21 Aug 2011

@author: shana

Front-end CLI
"""
import helpers, boorulink, wallbase
from sys import argv
if len(argv) < 3:
    print('Not enough arguments. Use <script name> <tag> <save Directory> [<MD5 file>]')
    helpers.shutil.sys.exit(1)
tagWanted = argv[1]
saveDirectory = argv[2]
if len(argv) > 3:
    md5file = argv[3]
    if not helpers.shutil.os.path.exists(md5file):
        print('MD5 file path doesn\'t exist.')
        helpers.shutil.os._exit(1)
else:
    md5file = ''
    
imageLinks = boorulink.getLinks(tagWanted, md5file)
"""
print('Getting wallbase links')
for link in wallbase.getLinks(tagWanted):
    imageLinks.append(link)
print('Done with wallbase, now have {0} links'.format(imageLinks))
"""
allNumberOfLinks = len(imageLinks)
fileList = [file for file in helpers.shutil.os.listdir(saveDirectory) if not helpers.shutil.os.path.splitext(helpers.shutil.os.path.join(saveDirectory, file))[1] == '']
tempLinks = imageLinks[:]
for link in tempLinks:
    if helpers.shutil.os.path.split(link)[1] in fileList:
        imageLinks.remove(link)
        
del tempLinks  
numberOfLinks = len(imageLinks)
print('Got {0} links after back-end duplicate removal, will download {1} images after filtering based on local files'.format(allNumberOfLinks, numberOfLinks))
for index, link in enumerate(imageLinks):
    savePath = helpers.downloadFile(link, saveDirectory)
    print('Got {0} out of {1} images with a tag {2}'.format(index + 1, numberOfLinks, tagWanted))
    if not savePath == 0:
        print('It was saved to {0}'.format(savePath))
    else:
        print('Skipping this file as it is present already.')

print('Done.')
