#!/usr/bin/python
import os
import platform
import urllib


# Return the path to specified executable, code fragment from stackoverflow
def which(program):
    def is_exe(fpath):
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
	if is_exe(program):
	    return program
    else:
	for path in os.environ["PATH"].split(os.pathsep):
	    exe_file = os.path.join(path, program)
	    if is_exe(exe_file):
		return exe_file

    return None        # program not found


# Download sourceLink to saveDestination
def download(saveDestination, sourceLink):
	# test if wget is avaliable on our system
	if which('wget') is not None:
		# we prefer using wget as our downloading tool
		os.system('wget -q -nc -P %s %s' % (saveDestination, sourceLink))
	else:
		# since wget is not avaliable for now, we have to do this on our own
		originalDirectory = os.path.abspath(os.curdir)
		os.chdir(saveDestination)
		tried = 0
		maxTries = 3
		while maxTries > tried:
			# Download the file
			try:
				# Download the data and file size information
				fileData = urllib.urlopen(sourceLink)
				fileSize = int(fileData.headers['Content-Length'])
				fileData = fileData.read()

				# Obtain file name
				saveFileTo = os.path.split(sourceLink)[1]

				# Save the file
				fileSaveObject = open(saveFileTo, 'wb')
				fileSaveObject.write(fileData)
				fileSaveObject.close()
				
				# Check that the file size matches
				if not os.path.getsize(saveFileTo) == fileSize:
					tried += 1
					continue
				else:
					break
			except:
				tried += 1
				# Go back to the initial directory
				os.chdir(originalDirectory)
