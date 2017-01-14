import numpy as np
import requests
import json
import itertools
import bs4
import matplotlib.pyplot as plt
import LocationUtils as LU

dictionary = "MusicGenres"
dictionaryPath = "Artists/"

def updateDictionnary(genres,dictionnary,debug = False):
	'''This method update the dictionary using the genres list'''
	if(genres==None):
		return dictionnary
		
	for genre in genres:
		genre = genre.lower()
		if(not genre in dictionnary):
			#gs = itertools.combinations(genre.split(" "),i)
			spacesplit = genre.split(" ")
			gs = []
			for a in spacesplit:
				linesplit = a.split("-")
				for l in linesplit:
					gs.append(str(l))
				
			mainGenre = None
			for g in gs:
				#g = str(g).replace("', '"," ").replace("')","").replace("('","").replace("',)","")
				if(g in dictionnary):
					if(not genre in dictionnary):
						mainGenre = dictionnary[g]
						dictionnary.update({genre : mainGenre})   
						if(debug):            
							print("added : dic{"+genre+" : "+mainGenre+"}")
						#return dictionnary
				else:
					if(len(g)>1):
						dictionnary.update({g : g})
						if(debug):
							print("added : dic{"+g+" : "+g+"}")
				#if(genre in dictionnary):
					#   return dictionnary
					#else:
						# dictionnary.update({genre : genre)
		if(genre not in dictionnary):  
			if(debug):
				print("missing genre : "+genre)
			dictionnary.update({genre : genre})
			
	return dictionnary
	
def sanitize(genres):
	'''This method remove unwanted features from the list of genres'''
	if(genres is None):
		return genres
	else:
		gen = []
		
		nations = ["italian","autralian","french","english","greek","latin"]
		for genre in genres:
			gs = genre.split(" ")
			valid = True
			for g in gs:
				if(g in nations):
					valid = False
			if(valid):
				gen.append(genre)
	return gen

def getMaxGenre(genres,debug = False):
	'''Get the genre in genres that appears the most'''
	dicnum = {}
	for g in genres :
		dicnum.update({g : genres.count(g)})
   
	maxKey = 0
	maxEntry = None
	
	if(debug):
		print(dicnum)
		plt.bar(range(len(dicnum)), dicnum.values(), align='center')
		plt.xticks(range(len(dicnum)), dicnum.keys())
        
	for entry in dicnum :
		if dicnum[entry]>maxKey and entry is not None:
			maxEntry = entry
			maxKey = dicnum[entry]
	
	return maxEntry     
	
def parseSection(section,level=2):
	#print(section)
	#print("#############################")
	soup = bs4.BeautifulSoup(section,"html5lib")
	MAIN_GENRE = soup.findAll("span")[0].text.lower()
	#print(MAIN_GENRE)
	#print("#############################")
	
	level1dic = {}
	level2dic = {}
	
	for div in soup.findAll("li"):
		level1 = div.text
		if(level==3): #Spanning 3 level dictionnary
			if("ul" in str(div)):
				level1split = level1.split("\n")
				subgenre1 = level1split[0].lower()
                
				if(subgenre1 not in level2dic):
					#print("\t"+subgenre1)
					level1dic.update({subgenre1 : MAIN_GENRE})
					subgenre2 = level1split[1:]
					for s2 in subgenre2:
						if(len(s2)>1):
							#print("\t\t"+str(s2))
							level2dic.update({s2 : subgenre1})
			else:
				level1split = level1.split("\n")
				subgenre1 = level1split[0].lower()
				level1dic.update({subgenre1 : MAIN_GENRE})
				#print(level2dic)
		if(level==2):
			level1split = level1.split("\n")
			subgenre1 = level1split[0].lower()
			level1dic.update({subgenre1 : MAIN_GENRE})
			#print(level2dic)
			
	if(level==2):
		return MAIN_GENRE,level1dic
	
	return MAIN_GENRE,level1dic,level2dic
	
def createDictionnary(level=2,debug=False,returnMains = False):
	#wikiURL = "https://en.wikipedia.org/wiki/"+str(genre)
	listGenres = "https://en.wikipedia.org/wiki/List_of_popular_music_genres"
	contentWIKI = requests.get(listGenres).text
	#content = requests.get(listGenres).text
	soup = bs4.BeautifulSoup(contentWIKI,"html5lib")
	mainList = []
	subgenres = []
	subgenres = {}
	mainGenres = {}

	sections = str(soup).split("<h2>")
	for i in range(2,18):
		MAIN_GENRE,level1dic= parseSection(sections[i])
		mainGenres.update({MAIN_GENRE:MAIN_GENRE})
		subgenres.update(level1dic)
		
	subgenres.update(mainGenres)
	
	
	#Manual adds :
	subgenres.update({"rap":"hip hop"})
	subgenres.update({"orchestral":"orchestral"})
	
	LU.saveDictionary(subgenres,dictionary,dictionaryPath,enc="UTF-8")
		
	if(returnMains):
		return mainGenres,subgenres
	return subgenres
	
        
def mainGenres(genres,dictionnary=None, debug = False):
	'''This function associates a genre with the best match in dictionnary'''
	dictionnary = updateDictionnary(genres,dictionnary, debug)
		
	mainGenreAssociates = []
	if(genres==None):
		return mainGenreAssociates
		
	for genre in genres :
		#Update the list with the new genre
		#if(genre not in dictionnary):
			# dictionnary = updateDictionnary(genre,dictionnary, debug)        
    
		#mainGenreAssociates.append(associates[genre])
		if(debug):
			print("for "+str(genre)+" found "+dictionnary[genre])
		mainGenreAssociates.append(dictionnary[genre])
				
	return mainGenreAssociates
	
def extractGenresFromRA(Artist,dic=None):
	#print("Extract from RA"	)
	artist = Artist.lower().replace(" ","")
	URL = "https://www.residentadvisor.net/dj/"+artist+"/biography"
	content = requests.get(URL).text
	
	soup = bs4.BeautifulSoup(content, "html5lib")   
	#print(content)
	listGenre = []
	for art in soup.findAll("article"):
		text = art.text
		if(dic==None):
			dic=createDictionnary()
            
		for genre in dic:
			if(genre in text):
				listGenre.append(genre)
	return listGenre
		
def getGenresFromWeb(Artist,dictionnary=None):
	SpotifySearchURL = "https://api.spotify.com/v1/search"
	
	#arguments
	args = {
	'q' : str(Artist),
	'type' : 'artist'
	}
	
	#Query 
	request = requests.get(SpotifySearchURL, params = args)
	content = json.loads(request.text)
	genres = []
	genresSPOT = []
	if(content!=None and ('artists' in content.keys()) and content['artists']['total']>0):
		genresSPOT= genresSPOT + content['artists']['items'][0]['genres']

	genresRA = extractGenresFromRA(Artist,dictionnary)
	
	genres = genres + genresSPOT +genresRA
	genres = genres + genresSPOT + genresSPOT #Add More weight to spotify
	#print(genres)
	return genres
	
def getGenre(Artist,ReturnAllGenres = False, dictionnary = None, Year=None, debug= False):
	'''Get the genre of an artist at this period.If period is None, 
	gets the most representative genre of the artist across time.'''
	if(dictionnary==None):
		dictionnary = createDictionnary()
	
	genres = getGenresFromWeb(Artist,dictionnary)
	if(len(genres)>0):
		genres = sanitize(genres)
	
	MG = mainGenres(genres,dictionnary, debug)
	if(ReturnAllGenres == True):
		return MG
	#print("Genres : "+str(genres))
	#print("mainGenres : "+str(MG))
		
	mainGenre = getMaxGenre(MG,debug)
	
	return mainGenre
	
def getMeanGenre(genres):
	'''If an artist has a lot of genres, try to find the more representative'''
	return
	
def getDiscography(Artist,Year = None):
	'''return the discography of the Artist'''
	#TODO
	return