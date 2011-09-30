#Front-end interface for ImageCraze
from Tkinter import *
import source.mainWorker as mainWorker
import os
import threading

class App:
	def __init__(self, master):
		self.frame = Frame(master)
		self.frame.grid_propagate(False)
		self.frame.grid()
		self.listOfSites = {
				'gelbooruCheck': 		BooleanVar(),
				'konachanCheck': 		BooleanVar(),
				'ichijouCheck': 		BooleanVar(),
				'danbooruCheck': 		BooleanVar(),
				'sankakuComplexCheck': 	BooleanVar(),
				'safebooruCheck': 		BooleanVar(),
				'nekobooruCheck': 		BooleanVar(),
				'moeImoutoCheck': 		BooleanVar()
			}
		
		#Checkboxes
		self.gelbooruCheck = Checkbutton(master, text = 'Gelbooru', variable = self.listOfSites['gelbooruCheck'], command = self.entryBoxState)
		self.konachanCheck = Checkbutton(master, text = 'Konachan', variable = self.listOfSites['konachanCheck'], command = self.entryBoxState)
		self.ichijouCheck = Checkbutton(master, text = 'Ichijou', variable = self.listOfSites['ichijouCheck'], command = self.entryBoxState)		
		self.danbooruCheck = Checkbutton(master, text = 'Danbooru', variable = self.listOfSites['danbooruCheck'], command = self.entryBoxState)
		self.sankakuComplexCheck = Checkbutton(master, text = 'Sankaku', variable = self.listOfSites['sankakuComplexCheck'], command = self.entryBoxState)
		self.safebooruCheck = Checkbutton(master, text = 'Safebooru', variable = self.listOfSites['safebooruCheck'], command = self.entryBoxState)
		self.nekobooruCheck = Checkbutton(master, text = 'Nekobooru', variable = self.listOfSites['nekobooruCheck'], command = self.entryBoxState)
		self.moeImoutoCheck = Checkbutton(master, text = 'MoeImouto', variable = self.listOfSites['moeImoutoCheck'], command = self.entryBoxState)
		

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

		#Check button
		self.checkButton = Button(master, text = 'Check', state = DISABLED, disabledforeground = 'grey', command = self.checkSetup)
		self.checkButton.grid(row = 6, column = 0)
		
		#Download button
		self.downloadButton = Button(master, text = 'Download', state = DISABLED, command = self.startDownload)
		self.downloadButton.grid(row = 6, column = 2)
		self.cacheDestination = ''
		self.cacheTags = ''
		self.cacheSites  = ''

		#Quit button
		self.quitButton = Button(master, text = 'Quit', command = self.frame.quit)
		self.quitButton.grid(row = 6, column = 3)

		#Message label
		self.messageLabel = Label(master, text = '\nPick your download sources.\n')
		self.messageLabel.grid(row = 0, column = 2, columnspan = 1)

	def tickAll(self):
		if self.tickAllVar:
			self.gelbooruCheck.select()
			self.konachanCheck.select()
			self.ichijouCheck.select()
			self.danbooruCheck.select()
			self.sankakuComplexCheck.select()
			self.safebooruCheck.select()
			self.nekobooruCheck.select()
			self.moeImoutoCheck.select()
			self.allButton['text'] = 'None'
			self.tickAllVar = False
			self.saveDestinationBox['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.checkButton['state'] = NORMAL
		else:
			self.gelbooruCheck.deselect()
			self.konachanCheck.deselect()
			self.ichijouCheck.deselect()
			self.danbooruCheck.deselect()
			self.sankakuComplexCheck.deselect()
			self.safebooruCheck.deselect()
			self.nekobooruCheck.deselect()
			self.moeImoutoCheck.deselect()
			self.allButton['text'] = 'All'
			self.tickAllVar = True		
			self.saveDestinationBox['state'] = DISABLED
			self.tagBox['state'] = DISABLED
			self.checkButton['state'] = DISABLED
			

	def checkSetup(self):
		emptyTag = 0
		emptyDestination = 0
		wrongDestination = 0
		notDestination = 0
		if self.tagBox.get() == '':
			emptyTag = 1

		if self.saveDestinationBox.get() == '':
			emptyDestination = 1
		elif not os.path.exists(self.saveDestinationBox.get()):
			wrongDestination = 1
		elif not os.path.isdir(self.saveDestinationBox.get()):
			notDestination = 1

		#Construct error message
		error = ''
		if emptyDestination: error += 'Nothing in destination box.\n '
		if wrongDestination: error += 'Destination doesn\'t exist.\n '
		if notDestination: error += 'Destination is not a directory.\n '
		if emptyTag: error += 'Nothing in the tag box. '

		if not error == '':
			self.messageLabel['foreground'] = 'red'
			self.messageLabel['text'] = '\n' + error
		else:
			self.messageLabel['foreground'] = 'green'
			self.messageLabel['text'] = '\nAll checked out. Ready to go!\n'
			self.downloadButton['state'] = NORMAL
			self.cacheDestination = self.saveDestinationBox.get()
			self.cacheSites = self.listOfSites.copy()
			self.cacheTags = self.tagBox.get()
			
		#Check download sources
		gotSource = False
		for key in self.listOfSites.keys():
			if self.listOfSites[key].get() == 1:
				gotSource = True
				break
		
		#Check save destination
		if not os.path.exists(self.saveDestinationBox.get()):
			print 'Destination %s doesn\'t exist.' % os.path.abspath(self.saveDestinationBox.get())
		
	
	def entryBoxState(self):
		#Check download sources and set saveDestinationBox and allButton states and variables
		gotSource = 0
		for key in self.listOfSites.keys():
			if self.listOfSites[key].get() == 1:
				gotSource += 1

		if gotSource == len(self.listOfSites.keys()):
			self.saveDestinationBox['state'] = NORMAL
			self.checkButton['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.allButton['text'] = 'None'
			self.tickAllVar = False
		elif gotSource > 0:
			self.saveDestinationBox['state'] = NORMAL
			self.checkButton['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.allButton['text'] = 'All'
			self.tickAllVar = True
		else:
			self.saveDestinationBox['state'] = DISABLED
			self.checkButton['state'] = DISABLED
			self.tagBox['state'] = DISABLED
			self.allButton['text'] = 'All'
			self.tickAllVar = True

	
	def startDownload(self):
		#Make sure user didn't change anything
		if not self.cacheSites == self.listOfSites or not self.cacheTags == self.tagBox.get() or not self.cacheDestination == self.saveDestinationBox.get():
			self.messageLabel['foreground'] = 'red'
			self.messageLabel['text'] = '\nDon\'t change the settings after checking.\nCheck again before downloading.'
			self.downloadButton['state'] = DISABLED
		else:
			workerThread = threading.Thread(target = mainWorker.work, args = (self,))
			workerThread.start()


	def enabler(self, enableRequest):
		if enableRequest == 'DISABLED':
			self.downloadButton['state'] = DISABLED
			self.tagBox['state'] = DISABLED
			self.saveDestinationBox['state'] = DISABLED
			self.checkButton['state'] = DISABLED
			self.allButton['state'] = DISABLED
			self.gelbooruCheck['state'] = DISABLED
			self.konachanCheck['state'] = DISABLED
			self.ichijouCheck['state'] = DISABLED
			self.danbooruCheck['state'] = DISABLED
			self.sankakuComplexCheck['state'] = DISABLED
			self.safebooruCheck['state'] = DISABLED
			self.nekobooruCheck['state'] = DISABLED
			self.moeImoutoCheck['state'] = DISABLED
		elif enableRequest == 'NORMAL':
			self.downloadButton['state'] = NORMAL
			self.tagBox['state'] = NORMAL
			self.saveDestinationBox['state'] = NORMAL
			self.checkButton['state'] = NORMAL
			self.allButton['state'] = NORMAL
			self.gelbooruCheck['state'] = NORMAL
			self.konachanCheck['state'] = NORMAL
			self.ichijouCheck['state'] = NORMAL
			self.danbooruCheck['state'] = NORMAL
			self.sankakuComplexCheck['state'] = NORMAL
			self.safebooruCheck['state'] = NORMAL
			self.nekobooruCheck['state'] = NORMAL
			self.moeImoutoCheck['state'] = NORMAL

if __name__ == '__main__':
	root = Tk()
	root.title('ImageCraze by Shana')
	root.resizable(width = FALSE, height = FALSE)
	app = App(root)

	root.mainloop()
	os._exit(0)
