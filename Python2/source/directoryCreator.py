import os
def createDirectory(saveDestination):
	if not os.path.exists(saveDestination):
		print 'Destination doesn\'t exist. Making a temporary one.'
		os.mkdir('temporaryDownloads')
		os.chdir('temporaryDownloads')
	elif os.path.exists(saveDestination) and not os.path.isdir(saveDestination):
		print 'Your save destination is not a directory. Making an emergency download location at script\'s location.'
		os.mkdir('emergency')
		os.chdir('emergency')
	else:
		os.chdir(saveDestination)
