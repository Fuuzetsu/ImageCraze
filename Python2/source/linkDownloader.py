#!/usr/bin/python
import os
def download(saveDestination, sourceLink):
	os.system('wget -q -nc -P %s %s' % (saveDestination, sourceLink))
