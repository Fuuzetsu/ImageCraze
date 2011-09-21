#!/usr/bin/python
import os
def download(sourceLink):
	os.system('wget -q -nc  %s' % sourceLink)
