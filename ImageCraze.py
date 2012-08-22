#!/usr/bin/python
#Front-end interface for ImageCraze
from Tkinter import *
import source.mainWorker as mainWorker
import os
import threading


class App:
	def __init__(self, master):
		self.is_running = False        # inform the worker thread (mainWorker.work) the cancellation of downloading
		self.num_threads = 5           # number of downloader threads
		self.cacheDestination = ''     # path to save those downloaded images
		self.cacheTags = ''            # tags to filter images
		self.cacheSites  = ''          # a copy of self.listOfSites (see below)
		self.listOfSites = {
				'gelbooruCheck': 	BooleanVar(),
				'konachanCheck': 	BooleanVar(),
				'ichijouCheck': 	BooleanVar(),
				'danbooruCheck': 	BooleanVar(),
				'sankakuComplexCheck':  BooleanVar(),
				'safebooruCheck': 	BooleanVar(),
				'nekobooruCheck': 	BooleanVar(),
				'moeImoutoCheck': 	BooleanVar()
				}

		##################### UI stuffs #####################
		self.frame = Frame(master)
		self.frame.grid_propagate(False)
		self.frame.grid()
		
		#Checkboxes
		self.gelbooruCheck = Checkbutton(master, text = 'Gelbooru', variable = self.listOfSites['gelbooruCheck'], command = self.entryBoxState)
		self.konachanCheck = Checkbutton(master, text = 'Konachan', variable = self.listOfSites['konachanCheck'], command = self.entryBoxState)
		self.ichijouCheck = Checkbutton(master, text = 'Ichijou', variable = self.listOfSites['ichijouCheck'], command = self.entryBoxState)
		self.danbooruCheck = Checkbutton(master, text = 'Danbooru', variable = self.listOfSites['danbooruCheck'], command = self.entryBoxState)
		self.sankakuComplexCheck = Checkbutton(master, text = 'Sankaku', variable = self.listOfSites['sankakuComplexCheck'], command = self.entryBoxState)
		self.safebooruCheck = Checkbutton(master, text = 'Safebooru', variable = self.listOfSites['safebooruCheck'], command = self.entryBoxState)
		self.nekobooruCheck = Checkbutton(master, text = 'Nekobooru', variable = self.listOfSites['nekobooruCheck'], command = self.entryBoxState)
		self.moeImoutoCheck = Checkbutton(master, text = 'MoeImouto', variable = self.listOfSites['moeImoutoCheck'], command = self.entryBoxState)

		self.siteCheckBoxes = [self.gelbooruCheck, self.konachanCheck, self.ichijouCheck, self.danbooruCheck, self.sankakuComplexCheck,
				   self.safebooruCheck, self.nekobooruCheck, self.moeImoutoCheck]
		
		self.gelbooruCheck.grid(row = 1, column = 0, sticky = W+N)
		self.konachanCheck.grid(row = 1, column = 2, sticky = W+N)
		self.ichijouCheck.grid(row = 3, column = 2, sticky = W+N)
		self.danbooruCheck.grid(row = 3, column = 0, sticky = W+N)
		self.sankakuComplexCheck.grid(row = 2, column = 0, sticky = W+N)
		self.safebooruCheck.grid(row = 2, column = 2, sticky = W+N)
		self.nekobooruCheck.grid(row = 2, column = 3, sticky = W+N)
		self.moeImoutoCheck.grid(row = 1, column = 3, sticky = W+N)

		#All button
		self.tickAllVar = True
		self.allButton = Button(master, text = 'All', width = 5, command = self.tickAll)
		self.allButton.grid(row = 3, column = 3, sticky = W+N)

		#Save directory textbox
		Label(master, text = 'Save directory: ').grid(column = 0, sticky = W+N)
		self.saveDestinationBox = Entry(master, state = DISABLED)
		self.saveDestinationBox['width'] = 30
		self.saveDestinationBox.grid(row = 4, column = 1, columnspan = 3, sticky = W+N)
		
		#Tag directory textbox
		Label(master, text = 'Desired tags:  ').grid(column = 0, sticky = W+N)
		self.tagBox = Entry(master, state = DISABLED)
		self.tagBox['width'] = 30
		self.tagBox.grid(row = 5, column = 1, columnspan = 3, sticky = W+N)

		# Num of downloading threads
		Label(master, text = 'Number of threads: ').grid(column = 0, sticky = W+N)
		self.numThreadBox = Entry(master, state = NORMAL)
		self.numThreadBox['width'] = 4
		self.numThreadBox.grid(row = 6, column = 1, sticky = W+N)
		self.numThreadBox.insert(0, str(self.num_threads))   # set value to default number of threads
		
		#Download button
		self.downloadButton = Button(master, text = 'Download', state = DISABLED, command = self.startDownload)
		self.downloadButton.grid(row = 7, column = 0)

		# Cancel button
		self.cancelButton = Button(master, text = 'Cancel', state = DISABLED, command = self.cancelDownloading)
		self.cancelButton.grid(row = 7, column = 2)

		#Quit button
		self.quitButton = Button(master, text = 'Quit', command = self.frame.quit)
		self.quitButton.grid(row = 7, column = 3)

		#Message label
		self.messageLabel = Label(master, text = '\nPick your download sources.\n')
		self.messageLabel.grid(row = 0, column = 2, columnspan = 1)
			

	# Check if all settings were valid before downloading images
	def checkSetup(self):
		emptyTag = 0              # tag is empty
		emptyDestination = 0      # destination path is empty
		wrongDestination = 0      # destination path is does not exist
		notDestination = 0        # path specified does not lead to a  directory
		nthreadNotValid = 0       # number of threads is not an positive integer

		# we need to get '~' properly expanded
		save_dest = os.path.expanduser(self.saveDestinationBox.get())

		# check for errors
		if self.tagBox.get() == '':
			emptyTag = 1

		if save_dest == '':
			emptyDestination = 1
		elif not os.path.exists(save_dest):
			wrongDestination = 1
		elif not os.path.isdir(save_dest):
			notDestination = 1

		try:
			self.num_threads = int(self.numThreadBox.get())
			if self.num_threads <= 0: nthreadNotValid = 1   # num of threads must be positive
		except:
			nthreadNotValid = 1

		#Construct error message
		error = ''
		if emptyDestination:  error += 'Nothing in destination box.\n '
		if wrongDestination:  error += 'Destination doesn\'t exist.\n '
		if notDestination:    error += 'Destination is not a directory.\n '
		if nthreadNotValid:   error += 'Num of threads is not an positive integer.\n'
		if emptyTag:          error += 'Nothing in the tag box. '

		if not error == '':
			self.messageLabel['foreground'] = 'red'
			self.messageLabel['text'] = '\n' + error
			return False
		else:
			self.messageLabel['foreground'] = 'green'
			self.messageLabel['text'] = '\nAll checked out. Ready to go!\n'
			self.cacheDestination = save_dest
			self.cacheSites = self.listOfSites.copy()
			self.cacheTags = self.tagBox.get()
			return True
	

	def startDownload(self):
		if self.checkSetup():
			workerThread = threading.Thread(target = mainWorker.work, args = (self,))
			self.is_running = True
			workerThread.start()

	def cancelDownloading(self):
		self.is_running = False    # We cannot forcely kill a thread in python, since there's no "official" way of doing
					   # this. So we have to inform the worker thread to terminate itself "gracefully"
		self.messageLabel['text'] = 'Cancelling...'


	# Callback for the "All" button
	def tickAll(self):
		if self.tickAllVar:
			for checkbox in self.siteCheckBoxes:
				checkbox.select()
			self.allButton['text'] = 'None'
			self.tickAllVar = False
			self.saveDestinationBox['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.downloadButton['state'] = NORMAL
		else:
			for checkbox in self.siteCheckBoxes:
				checkbox.deselect()
			self.allButton['text'] = 'All'
			self.tickAllVar = True		
			self.saveDestinationBox['state'] = DISABLED
			self.tagBox['state'] = DISABLED
			self.downloadButton['state'] = DISABLED


	def entryBoxState(self):
		#Check download sources and set saveDestinationBox and allButton states and variables
		gotSource = 0
		for key in self.listOfSites.keys():
			if self.listOfSites[key].get() == 1:
				gotSource += 1

		if gotSource == len(self.listOfSites.keys()):
			self.saveDestinationBox['state'] = NORMAL
			self.downloadButton['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.allButton['text'] = 'None'
			self.tickAllVar = False
		elif gotSource > 0:
			self.saveDestinationBox['state'] = NORMAL
			self.downloadButton['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.allButton['text'] = 'All'
			self.tickAllVar = True
		else:
			self.saveDestinationBox['state'] = DISABLED
			self.downloadButton['state'] = DISABLED
			self.tagBox['state'] = DISABLED
			self.allButton['text'] = 'All'
			self.tickAllVar = True


	def enabler(self, enableRequest):
		if enableRequest == 'DISABLED':
			self.downloadButton['state'] = DISABLED
			self.tagBox['state'] = DISABLED
			self.saveDestinationBox['state'] = DISABLED
			self.numThreadBox['state'] = DISABLED
			self.allButton['state'] = DISABLED
			for checkbox in self.siteCheckBoxes:
				checkbox['state'] = DISABLED
			self.cancelButton['state'] = NORMAL

		elif enableRequest == 'NORMAL':
			self.downloadButton['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.saveDestinationBox['state'] = NORMAL
			self.numThreadBox['state'] = NORMAL
			self.allButton['state'] = NORMAL
			for checkbox in self.siteCheckBoxes:
				checkbox['state'] = NORMAL
			self.cancelButton['state'] = DISABLED

if __name__ == '__main__':
	root = Tk()
	root.title('ImageCraze by Shana')
	root.resizable(width = FALSE, height = FALSE)
	app = App(root)

	root.mainloop()
	os._exit(0)
