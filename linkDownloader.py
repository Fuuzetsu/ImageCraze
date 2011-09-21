#!/usr/bin/python
import os
def download(sourceLink, saveDestination):
	if not os.path.exists(saveDestination):
		try:		
			os.mkdir(saveDestination)
			print 'Successfully made %d' % saveDestination
		except:
			print 'Could not make new folder. Making an emergency one in the current directory.'
			os.mkdir('./emergency')
			os.chdir('./emergency')
		os.chdir(saveDestination)
	elif os.path.exists(saveDestination) and not os.path.isdir(saveDestination):
		print 'Your save destination is not a directory. Making an emergency download location at script\'s location.'
		os.mkdir('./emergency')
		os.chdir('./emergency')
	else:
		os.chdir(saveDestination)
	os.system('wget -q -nc  %s' % sourceLink)
