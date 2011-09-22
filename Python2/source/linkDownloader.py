#!/usr/bin/python
import os
import platform
import urllib
def download(saveDestination, sourceLink):
	if platform.system == 'Linux':
		os.system('wget -q -nc -P %s %s' % (saveDestination, sourceLink))
	else:
		originalDirectory = os.path.abspath(os.curdir)
		os.chdir(saveDestination)
		tried = 0
		maxTries = 3
        	while maxTries > tried:
            	#Download the file
				try:
					#Download the data and file size information
					fileData = urllib.urlopen(linkToFile)
					fileSize = int(fileData.headers['Content-Length'])
					fileData = fileData.read()

					#Obtain file name
					saveFileTo = os.path.split(linkToFile)[1]

					#Save the file
					fileSaveObject = open(saveFileTo, 'wb')
					fileSaveObject.write(fileData)
					fileSaveObject.close()
                    
					#Check that the file size matches
					if not os.path.getsize(saveFileTo) == fileSize:
						tried += 1
						continue
					else:
						break
				except:
					tried += 1
				#Go back to the initial directory
				os.chdir(originalDirectory)
