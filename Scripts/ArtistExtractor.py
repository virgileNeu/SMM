import numpy as np
import requests
import json
import itertools
import bs4
import matplotlib.pyplot as plt


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

def createDictionnary(debug = False):
	'''Create the dictionnary of genres'''
	#wikiURL = "https://en.wikipedia.org/wiki/"+str(genre)
	listGenres = "https://en.wikipedia.org/wiki/List_of_electronic_music_genres"
	contentWIKI = requests.get(listGenres).text
	#content = requests.get(listGenres).text
	soup = bs4.BeautifulSoup(contentWIKI,"html5lib")
	mainList = []
	subgenres = []
	dic = {}
	main = ""
	
	for div in soup.findAll(attrs={"style" : "-moz-column-width: 20em; -webkit-column-width: 20em; column-width: 20em;"}):   
		if(div.attrs['style'] == "-moz-column-width: 20em; -webkit-column-width: 20em; column-width: 20em;"):
			if('style' in div.attrs):
				uls = div.find('ul')
				if(uls is not None):
					for groups in uls:
						for a in groups:
							b = str(a)
							soup2 = bs4.BeautifulSoup(b,"html5lib")
							if(len(soup2.text)>0 and soup2.text.count("\n")<2):
								mainList.append(soup2.text)
								main = soup2.text.replace("\n","")
								dic.update({main.lower() : main.lower()})
								if(debug):print("MAIN "+str(len(main))+" "+main)
                                
							if("ul" in b and len(b)>0):
								soup2 = bs4.BeautifulSoup(b,"html5lib")
								if(len(soup2.text)>0):
									t = soup2.text
									lines = t.split("\n")
									for genre in lines:
										if(len(genre)>0):
											if(debug):
												print(genre +"-"+main)
											if(debug):
												print("...")
											dic.update({genre.lower() : main.lower()})
                                
       
	##Manual Add
	dic.update({"house" : "house music"})
	dic.update({"tech" : "techno"})
	dic.update({"funk rock" : "funk"})
	dic.update({"trap francais" : "rap"})
	dic.update({"catstep":"drum and bass"})
	dic.update({"dance pop" : "pop"})
	dic.update({"complextro" : "uk garage"})
	dic.update({"hip hop" : "hip hop"})
	dic.update({"hip" : "hip hop"})
	dic.update({"hop" : "hip hop"})
	dic.update({"rock" : "rock"})
	dic.update({"rap" : "rap"})
	dic.update({"filthstep" : "uk garage"})
	
	return dic
	
	
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
	
def getGenre(Artist,dictionnary = None, Year=None, debug= False):
	'''Get the genre of an artist at this period.If period is None, 
	gets the most representative genre of the artist across time.'''
	if(dictionnary==None):
		dictionnary = createDictionnary()
	
	genres = getGenresFromWeb(Artist,dictionnary)
	if(len(genres)>0):
		genres = sanitize(genres)
	
	MG = mainGenres(genres,dictionnary, debug)
	
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