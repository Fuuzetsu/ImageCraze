#!/usr/bin/python
import booruClass

def initialize(wantedSites):
	"""
	Function that creates the objects based on user preferences. Can then be used to establish download links.
	Takes a dictionary argument with all the sites available and their value (0 or 1).

	Returns: list - initialized objects
	"""
	objectsToReturn = []

	if wantedSites['gelbooruCheck']:
		gelbooru = booruClass.Booru(
						'Gelbooru',
						'http://gelbooru.com/',
						'index.php?page=dapi&s=post&q=index&limit=100&tags=',
						r'file_url="(http://\w+\.gelbooru\.com/images/\d+/\w+\.\w+)".+md5="(\w+)"',
						'&pid=',
						'XML'
						)
		objectsToReturn.append(gelbooru)

	if wantedSites['konachanCheck']:
		konachan = booruClass.Booru(
						'Konachan',
						'http://konachan.com/post/',
						'index.xml?limit=100&tags=',
						r'file_url="(http://\w+\.\w+\.\w+/\w+/(\w+)/[A-z0-9_%.-]+\.\w+)"',
						'&page=',
						'XML'
						)
		objectsToReturn.append(konachan)

	if wantedSites['ichijouCheck']:
		ichijou = booruClass.Booru(
						'ichijou',
						'http://ichijou.org/post/',
						'index.xml?limit=100&tags=',
						r'file_url="(http://ichijou.org/\w+/\w+/\w+/(\w+)\.\w+)"',
						'&page=',
						'XML'
						)
		objectsToReturn.append(ichijou)

	if wantedSites['danbooruCheck']:
		danbooru = booruClass.Booru(
						'Danbooru',
						'http://danbooru.donmai.us/post/',
						'index.xml?limit=100&tags=',
						r'file_url="(http://\w+\.\w+\.\w+/\w+/(\w+)\.\w+)"',
						'&page=',
						'XML'
						)
		objectsToReturn.append(danbooru)

	if wantedSites['sankakuComplexCheck']:
		sankakuComplex = booruClass.Booru(
						'Sankaku Complex',
						'http://chan.sankakucomplex.com/post/',
						'index.json?tags=',
						r'"md5":"(\w+)"[a-z:,"0-9]+"file_url":"(http://chan\.sankakustatic\.com/data/\w\w/\w\w/\w+\.\w+)",',
						'&page=',
						'JSON'
						)
		objectsToReturn.append(sankakuComplex)

	if wantedSites['safebooruCheck']:
		safebooru = booruClass.Booru(
						'Safebooru',
						'http://safebooru.org/',
						'index.php?page=dapi&s=post&q=index&tags=',
						r'file_url="(http://safebooru\.org/images/\d+/\w+\.\w+).+md5="(\w+)"',
						'&pid=',
						'XML'
						)
		objectsToReturn.append(safebooru)

	if wantedSites['nekobooruCheck']:
		nekobooru = booruClass.Booru(
						'Nekobooru',
						'http://nekobooru.net/post/',
						'index.json?tags=',
						r'"md5":"(\w+)"[a-z:,"0-9]+"file_url":"(http://nekobooru\.net/data/\w\w/\w\w/\w+\.\w+)",',
						'&page=',
						'JSON'
						)
		objectsToReturn.append(nekobooru)

	if wantedSites['moeImoutoCheck']:
		moeImouto = booruClass.Booru(
						'Moe Imouto',
						'http://oreno.imouto.org/post/',
						'index.xml?tags=',
						r'file_url="(http://\w+\.\w+\.\w+/\w+/(\w+)/[A-z0-9_%.-]+\.\w+)"',
						'&page=',
						'XML'
						)
		objectsToReturn.append(moeImouto)
		

	return objectsToReturn

if __name__ == '__main__':
	listOfSites = {
						'gelbooruCheck': 		False,
						'konachanCheck': 		False,
						'ichijouCheck': 		True,
						'danbooruCheck': 		False,
						'sankakuComplexCheck': 	False,
						'safebooruCheck': 		True,
						'nekobooruCheck': 		True,
						'moeImoutoCheck': 		False
					}
	obj = initialize(listOfSites)
	for each in obj:
		print each.siteName + ' - ' + each.queryType
