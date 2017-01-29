import numpy as np
import requests
import json
import itertools
import bs4
import matplotlib.pyplot as plt
import LocationUtils as LU
import copy

dictionary = "MusicGenres"
dictionaryPath = "Artists/"
"""Country name to demonym table."""

__author__ = "leandro@tia.mat.br (Leandro Pereira)"

COUNTRY_DEMONYMS = {
    u'ERITREA': u'Eritrean',
    u'PORTUGAL': u'Portuguese',
    u'KOSOVO': u'Kosovan',
    u'INDIA': u'Indian',
    u'MONTENEGRO': u'Montenegrin',
    u'NEW CALEDONIA': u'New Caledonian',
    u'UZBEKISTAN': u'Uzbek',
    u'TOGO': u'Togolese',
    u'ARUBA': u'Aruban',
    u'MICRONESIA': u'Micronesian',
    u'IRAN': u'Irani',
    u'MALTA': u'Maltese',
    u'KIRIBATI': u'Kiribatian',
    u'BARBADOS': u'Barbadian',
    u'BENIN': u'Beninese',
    u'IRAQ': u'Iraqi',
    u'CHAD': u'Chadian',
    u'SAINT HELENA': u'Saint Helenian',
    u'TAJIKISTAN': u'Tajikistani',
    u'COSTA RICA': u'Costa Rican',
    u'ETHIOPIA': u'Ethiopian',
    u'SWEDEN': u'Swede',
    u'RWANDA': u'Rwandan',
    u'OMAN': u'Omani',
    u'SURINAME': u'Surinamer',
    u'ZAMBIA': u'Zambian',
    u'ANGUILLA': u'Anguillan',
    u'NORWAY': u'Norwegian',
    u'QATAR': u'Qatari',
    u'PALAU': u'Palauan',
    u'SUDAN': u'Sudanese',
    u'DENMARK': u'Dane',
    u'NEPAL': u'Nepalese',
    u'AZERBAIJAN': u'Azerbaijani',
    u'PAPUA NEW GUINEA': u'Guinean',
    u'ZIMBABWE': u'Zimbabwean',
    u'GABON': u'Gabonese',
    u'GIBRALTAR': u'Gibraltarian',
    u'SWAZILAND': u'Swazi',
    u'VANUATU': u'Vanuatuan',
    u'YEMEN': u'Yemeni',
    u'VENEZUELA': u'Venezuelan',
    u'ECUADOR': u'Ecuadorean',
    u'BAHAMAS': u'Bahamian',
    u'AUSTRALIA': u'Australian',
    u'ENGLAND': u'Englishman',
    u'KUWAIT': u'Kuwaiti',
    u'TANZANIA': u'Tanzanian',
    u'SCOTLAND': u'Scot',
    u'CENTRAL AFRICAN REPUBLIC': u'Central African',
    u'FRANCE': u'Frenchman',
    u'TRINIDAD AND TOBAGO': u'Trinidadian and Tobagan',
    u'ARMENIA': u'Armenian',
    u'AUSTRIA': u'Austrian',
    u'SRI LANKA': u'Sri Lankan',
    u'CROATIA': u'Croat',
    u'TURKS AND CAICOS ISLANDS': u'Turks and Caicos Islander',
    u'COMOROS': u'Comoran',
    u'TONGA': u'Tongan',
    u'GEORGIA': u'Georgian',
    u'HONDURAS': u'Honduran',
    u'GUINEA-BISSAU': u'Guinean',
    u'LIBYA': u'Libyan',
    u'NORTHERN MARIANAS': u'Northern Mariana Islander',
    u'MAYOTTE': u'Mahorais',
    u'INDONESIA': u'Indonesian',
    u'ANTARCTICA': u'Antarctican',
    u'VIETNAM': u'Vietnamese',
    u'MOZAMBIQUE': u'Mozambican',
    u'SOUTH SUDAN': u'South Sudanese',
    u'COLOMBIA': u'Colombian',
    u'MARTINIQUE': u'Martinican',
    u'SWITZERLAND': u'Swiss',
    u'CANADA': u'Canadian',
    u'MAURITANIA': u'Mauritanian',
    u'LITHUANIA': u'Lithuanian',
    u'CAMBODIA': u'Cambodian',
    u'EGYPT': u'Egyptian',
    u'CUBA': u'Cuban',
    u'LEBANON': u'Lebanese',
    u'SAINT PIERRE AND MIQUELON': u'Saint-Pierrais',
    u'BOTSWANA': u'Botswanan',
    u'SENEGAL': u'Senegalese',
    u'CONGO': u'Congolese', 
    u'ALGERIA': u'Algerian',
    u'MALI': u'Malian',
    u'NEW ZEALAND': u'New Zealander',
    u'VATICAN CITY': u'Vatican',
    u'COOK ISLANDS': u'Cook Islander',
    u'PAKISTAN': u'Pakistani',
    u'REUNIONESE': u'Reunionese',
    u'ANGOLA': u'Angolan',
    u'PRINCIPEAN': u'Principean',
    u'SAINT LUCIA': u'Saint Lucian',
    u'GUYANA': u'Guyanese',
    u'SAINT KITTS AND NEVIS': u'Kittsian',
    u'MALAYSIA': u'Malaysian',
    u'SAINT VINCENT AND THE GRENADINES': u'Saint Vincentian',
    u'GHANA': u'Ghanaian',
    u'IRELAND': u'Irishman',
    u'SYRIA': u'Syrian',
    u'NIGERIA': u'Nigerian',
    u'NORTH KOREA': u'North Korean',
    u'KYRGYZSTAN': u'Kirgizia',
    u'BANGLADESH': u'Bangladeshi',
    u'ESTONIA': u'Estonian',
    u'SLOVENIA': u'Slovenian',
    u'ICELAND': u'Icelander',
    u'SEYCHELLES': u'Seychellois',
    u'RUSSIA': u'Russian',
    u'LESOTHO': u'Mosotho',
    u'TUNISIA': u'Tunisian',
    u'BRITISH VIRGIN ISLANDS': u'British Virgin Islander',
    u'BOSNIA AND HERZEGOVINA': u'Bosnian',
    u'MONACO': u'Monacan',
    u'WALLIS AND FUTUNA': u'Wallis and Futuna Islander',
    u'UKRAINE': u'Ukrainian',
    u'BRUNEI': u'Bruneian',
    u'ISRAEL': u'Israeli',
    u'IVORY COAST': u'Ivoirian',
    u'KHALISTAN': u'Sikhistan',
    u'MEXICO': u'Mexican',
    u'TUVALU': u'Tuvaluan',
    u'SERBIA': u'Serbian',
    u'CAPE VERDE': u'Cape Verdean',
    u'UNITED KINGDOM': u'Briton',
    u'MOROCCO': u'Moroccan',
    u'NETHERLANDS': u'Holland',
    u'UGANDA': u'Ugandan',
    u'GRENADA': u'Grenadian',
    u'THAILAND': u'Thai',
    u'MONTSERRAT': u'Montserratian',
    u'BOLIVIA': u'Bolivian',
    u'SIERRA LEONE': u'Sierra Leonian',
    u'BRAZIL': u'Brazilian',
    u'MADAGASCAR': u'Madagascan',
    u'ALBANIA': u'Albanian',
    u'CZECH REPUBLIC': u'Czech',
    u'SOUTH AFRICA': u'South African',
    u'BRITAIN': u'Northern Ireland',
    u'SINGAPORE': u'Singaporean',
    u'GERMANY': u'German',
    u'PUERTO RICO': u'Puerto Rican',
    u'NIGER': u'Nigerien',
    u'NICARAGUA': u'Nicaraguan',
    u'MALAWI': u'Malawian',
    u'NIUE': u'Niuean',
    u'EAST TIMOR': u'East Timorese',
    u'SAUDI ARABIA': u'Saudi',
    u'ITALY': u'Italian',
    u'PERU': u'Peruvian',
    u'PHILIPPINES': u'Filipino',
    u'KENYA': u'Kenyan',
    u'BERMUDA': u'Bermudian',
    u'FRENCH GUIANA': u'Guianese',
    u'SOMALIA': u'Somali',
    u'PALESTINE': u'Palestinian',
    u'ARGENTINA': u'Argentinian',
    u'CYPRUS': u'Cypriot',
    u'BAHRAIN': u'Bahraini',
    u'FALKLAND ISLANDS': u'Falkland Islander',
    u'MALDIVES': u'Maldivian',
    u'WESTERN SAHARA': u'Sahrawi',
    u'CAYMAN ISLANDS': u'Caymanian',
    u'MARSHALL ISLANDS': u'Marshallese',
    u'MONGOLIA': u'Mongolian',
    u'LATVIA': u'Latvian',
    u'SLOVAKIA': u'Slovak',
    u'LAOS': u'Lao',
    u'BELGIUM': u'Belgian',
    u'GAMBIA': u'Gambian',
    u'BURKINA FASO': u'Burkinabe',
    u'US VIRGIN ISLANDS': u'US Virgin Islander',
    u'LIBERIA': u'Liberian',
    u'AFGHANISTAN': u'Afghan',
    u'KAZAKHSTAN': u'Kazakh',
    u'GUAM': u'Guamanian',
    u'AMERICAN SAMOA': u'American Samoan',
    u'MOLDOVA': u'Moldavia',
    u'MAURITIUS': u'Mauritian',
    u'LIECHTENSTEIN': u'Liechtensteiner',
    u'MYANMAR': u'Burma',
    u'NAMIBIA': u'Namibian',
    u'GREECE': u'Hellas',
    u'WALES': u'Welshman',
    u'NAURU': u'Nauruan',
    u'BELIZE': u'Belizean',
    u'FIJI': u'Fijian',
    u'TAIWAN': u'Republic of China',
    u'ROMANIA': u'Romanian',
    u'GREENLAND': u'Greenlander',
    u'TIBET': u'Tibetan',
    u'EL SALVADOR': u'Salvadoran',
    u'POLAND': u'Pole',
    u'UNITED STATES OF AMERICA': u'American',
    u'BRITTANY': u'Breton',
    u'LUXEMBOURG': u'Luxembourger',
    u'NORFOLK ISLAND': u'Norfolk Islander',
    u'ANTIGUA AND BARBUDA': u'Antiguan',
    u'CHRISTMAS ISLAND': u'Christmas Islander',
    u'HUNGARY': u'Hungarian',
    u'FAEROE ISLANDS': u'Faeroese',
    u'EUROPEAN UNION': u'European',
    u'SPAIN': u'Spaniard',
    u'CATALONIA': u'Catalan',
    u'JAMAICA': u'Jamaican',
    u'SOLOMON ISLANDS': u'Solomon Islander',
    u'UNITED ARAB EMIRATES': u'Emirati',
    u'FINLAND': u'Finn',
    u'COCOS ISLANDER': u'Cocos',
    u'PITCAIRN ISLANDS': u'Pitcairner',
    u'ANDORRA': u'Andorran',
    u'DJIBOUTI': u'Djiboutian',
    u'BELARUS': u'Byelorussia',
    u'JORDAN': u'Jordanian',
    u'MACEDONIA': u'Macedonian',
    u'JAPAN': u'Japanese',
    u'PARAGUAY': u'Paraguayan',
    u'DOMINICAN REPUBLIC': u'Dominican',
    u'HAITI': u'Haitian',
    u'DOMINICA': u'Dominican',
    u'TURKEY': u'Turk',
    u'SAMOA': u'Samoan',
    u'TURKMENISTAN': u'Turkmenia',
    u'BHUTAN': u'Bhutanese',
    u'URUGUAY': u'Uruguayan',
    u'GUINEA': u'Guinean',
    u'PANAMA': u'Panamanian',
    u'EQUATORIAL GUINEA': u'Equatorial Guinean',
    u'SAN MARINO': u'Sammarinese',
    u'FRENCH POLYNESIA': u'Polynesian',
    u'TOKELAU': u'Tokelauan',
    u'GUATEMALA': u'Guatemalan',
    u'CHILE': u'Chilean',
    u'BURUNDI': u'Burundian',
    u'CHINA': u'Chinese',
    u'SOUTH KOREA': u'South Korean',
    u'GUADELOUPE': u'Guadeloupean',
    u'CAMEROON': u'Cameroonian',
    u'BULGARIA': u'Bulgarian',
    u'BOUVET ISLAND': u'Bouvetan',
    u'BRITISH INDIAN OCEAN TERRITORY': u'British Indian',
    u'BRUNEI DARUSSALAM': u'Bruneian',
    u'COCOS (KEELING) ISLANDS': u'Cocos Islander',
    u'CONGO, THE DEMOCRATIC REPUBLIC OF THE': u'Congolese',
    u'CÔTE D\'IVOIRE': u'Ivorian',
    u'FALKLAND ISLANDS (MALVINAS)': u'Falkland Islander',
    u'FAROE ISLANDS': u'Faroese',
    u'HEARD ISLAND AND MCDONALD ISLANDS': u'Heard Islander',
    u'HOLY SEE (VATICAN CITY STATE)': u'Vatican Resident',
    u'HONG KONG': u'Hongkongese',
    u'IRAN, ISLAMIC REPUBLIC OF': u'Iranian',
    u'KOREA, DEMOCRATIC PEOPLE\'S REPUBLIC OF': u'North Korean',
    u'KOREA, REPUBLIC OF': u'Korean',
    u'LAO PEOPLE\'S DEMOCRATIC REPUBLIC': u'Laotian',
    u'LIBYAN ARAB JAMAHIRIYA': u'Libyan',
    u'MACAO': u'Macanese',
    u'MICRONESIA, FEDERATED STATES OF': u'Micronesian',
    u'MOLDOVA, REPUBLIC OF': u'Moldovan',
    u'NORTHERN MARIANA ISLANDS': u'Northern Marianan',
    u'PALESTINIAN TERRITORY, OCCUPIED': u'Palestinian',
    u'PITCAIRN': u'Pitcairn Islander',
    u'RUSSIAN FEDERATION': u'Russian',
    u'RÉUNION': u'Réunionese',
    u'SAO TOME AND PRINCIPE': u'São Toméan',
    u'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS': u'South Sandwich Islander',
    u'SVALBARD AND JAN MAYEN': u'Svalbardian',
    u'SYRIAN ARAB REPUBLIC': u'Syrian',
    u'TAIWAN, PROVINCE OF CHINA': u'Taiwanese',
    u'TANZANIA, UNITED REPUBLIC OF': u'Tanzanian',
    u'TIMOR-LESTE': u'Timorese',
    u'UNITED STATES': u'American',
    u'UNITED STATES MINOR OUTLYING ISLANDS': u'American',
    u'VIET NAM': u'Vietnamese',
    u'VIRGIN ISLANDS, BRITISH': u'Virgin Islander',
    u'VIRGIN ISLANDS, U.S.': u'Virgin Islander',
    u'[CITIZEN OF THE WORLD]': u'Earthling',
    u'[UNLISTED COUNTRY]': u'Unknownian',
}

def updateDictionnary(genres,dictionnary,debug = False):
	'''This method update the dictionary using the genres list'''
	
	dicKeys = dictionnary.keys()
	actualKeys = set(dicKeys)
	
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
						
				else:
					for genreDic in actualKeys:
						if(g in genreDic or genreDic in g):
							mainGenre = dictionnary.get(genreDic)
							
			if(mainGenre!=None):				
				dictionnary.update({genre : mainGenre})   
				if(debug):            
					print("added : dic{"+genre+" : "+mainGenre+"}")
					#return dictionnary
				'''
				else:
					if(len(g)>1 and not g.title() in COUNTRY_DEMONYMS.values()):
						#dictionnary.update({g : g})
						if(debug):
							print("added : dic{"+g+" : "+g+"}")
					
					#manual add
					if("hip hop" in genre):
						dictionnary.update({"hip" : "hip hop"})
						dictionnary.update({"hop" : "hip hop"})
						dictionnary.update({"hop" : "hip hop"})
						dictionnary.update({genre: "hip hop"})
						if(debug):
							print("added : dic{"+genre+" : hip hop}")
				'''		
				#if(genre in dictionnary):
					#   return dictionnary
					#else:
						# dictionnary.update({genre : genre)
		if(genre not in dictionnary):  
			if(debug):
				print("missing genre : "+genre)
			#dictionnary.update({genre : genre})
			
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

import operator
def getMaxGenre(genres,top=1,debug = False):
	'''Get the genre in genres that appears the most'''
	if(genres==None or genres=="None"):
		return []
		
	dicnum = {}
	for g in genres :
		if(g!=None and g!="None"):
			dicnum.update({g : genres.count(g)})
	
	sorted_dicnum = sorted(dicnum.items(), key=operator.itemgetter(1))
	sorted_dicnum.reverse()
	if(debug):
		print(sorted_dicnum)
	
	#for entry in dicnum :
	#	if dicnum[entry]>maxKey and entry is not None:
	#		maxEntry = entry
	#		maxKey = dicnum[entry]
	list = sorted_dicnum[0:top]
	max_genres = []
	for l in list:
		max_genres.append(l[0])
	
	if(len(max_genres)==0):
		return None
	return max_genres     
	
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
	subgenres.update({"classic":"orchestral"})
	subgenres.update({"classical":"orchestral"})
	subgenres.update({"step":"electronic"})
	
	LU.saveDictionary(subgenres,dictionary,dictionaryPath,enc="UTF-8")
		
	if(returnMains):
		return mainGenres,subgenres
	return subgenres
	
        
def mainGenres(genres,dictionnary=None, debug = False):
	'''This function associates a genre with the best match in dictionnary'''
	#dictionnary = updateDictionnary(genres,dictionnary, debug)
		
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
		if(genre in dictionnary):
			mainGenreAssociates.append(dictionnary[genre])
				
	return mainGenreAssociates
	
def getGenresFromRA(Artist,dic=None):
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
		
def getGenresFromWikipedia(Artist,dic=None):
	#print("Extract from RA")
	artist = str(Artist).replace(" ","_")
	listGenre = []
	
	URL = "https://fr.wikipedia.org/wiki/"+artist
	content = requests.get(URL).text
	
	soup = bs4.BeautifulSoup(content, "html5lib")   
	#print(content)
	
	for art in soup.findAll("a"):
		text = art.text
		if(dic==None):
			dic=createDictionnary()
		
		whitelist = set('abcdefghijklmnopqrstuvwxy ABCDEFGHIJKLMNOPQRSTUVWXYZ')
		answer = ''.join(filter(whitelist.__contains__, text))
		words = text.split(" ")
		for word in words :
			for genre in dic:
				if(genre.lower() == word.lower() and genre!= "oi"):
					listGenre.append(genre)
	
	if(len(listGenre<1)):
		#try with english version
		
		URL = "https://en.wikipedia.org/wiki/"+artist
		content = requests.get(URL).text
		
		soup = bs4.BeautifulSoup(content, "html5lib")   
		#print(content)
		
		for art in soup.findAll("a"):
			text = art.text
			if(dic==None):
				dic=createDictionnary()
				
			whitelist = set('abcdefghijklmnopqrstuvwxy ABCDEFGHIJKLMNOPQRSTUVWXYZ\'')
			answer = ''.join(filter(whitelist.__contains__, text))
			words = text.split(" ")
			for word in words :
				for genre in dic:
					if(genre.lower() == word.lower() and genre!= "oi"):
						listGenre.append(genre)
					
					
	return list(set(listGenre))
		
def getGenresFromWeb(Artist,dictionnary=None,onResidentAdvisor=True, onSpotify = True):
	
	genresRA = []
	if(onResidentAdvisor):
		genresRA = getGenresFromRA(Artist,dictionnary)
	
	genresSPOT = []
	if(onSpotify):
		genresSPOT = getGenresFromSpotify(Artist)
	
	genres = []
	genres = genres + genresSPOT +genresRA
	genres = genres + genresSPOT + genresSPOT #Add More weight to spotify
	#print(genres)
	return genres
	
def getGenresFromSpotify(Artist):
	SpotifySearchURL = "https://api.spotify.com/v1/search"
	#arguments
	args = {
	'q' : str(Artist),
	'type' : 'artist'
	}
	
	#Query 
	request = requests.get(SpotifySearchURL, params = args)
	content = json.loads(request.text)
	genresSpotify = []
	if(content!=None and ('artists' in content.keys()) and content['artists']['total']>0):
		genresSpotify = genresSpotify + content['artists']['items'][0]['genres']
		
	return genresSpotify
	
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