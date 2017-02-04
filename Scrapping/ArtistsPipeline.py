import pandas as pd
import numpy as np
import sys
sys.path.insert(0,'..\\Scripts\\Utils')
import ArtistExtractor as AE
import LocationUtils as LU
from ast import literal_eval
import moreFunction


PATH_DF = "FullDF_without_GPS.csv"
PATH_ARTISTS = "Artists.csv"	
PATH_DIC = "Dictionaries/"	
filename_spotify_dic = "SpotifyDictionary"
filename_ra_dic = "ResidentAdvisorDictionary"
filename_wiki_dic = "WikipediaDictionary"
filename_genres = "DictionaryOfGenres"
encoding = "utf-8"

def getArtistsList(df):
	df= df.fillna("None")
	print("Getting artists list from "+str(df.shape[0])+" events...")
	ArtistsDataFrame = pd.DataFrame()
	i=0
	for index,row in df.iterrows():
		lineup = str(row["artists"]) #get line-up
		artists = None
		if(lineup!="nan" and lineup!="None" and lineup!=None):
			try:
				artists = literal_eval(lineup)
			except:
				print("Malformed lineup : "+str(lineup))
				artists=None
		
		new_lineup=[]
		if(artists!=None):
			for a in artists:
				a = str(a).split("(")[0]#Remove parenthesis at end of artist (record label, live act..)

				#Use list for convenient format in clean_artists method
				artist_list = []
				artist_list.append(a)
				cleaned_artist = moreFunction.clean_artists(artist_list)
				if(len(cleaned_artist)>0):
					a = cleaned_artist[0]

				#Append artist in lineup
				new_lineup.append(a.strip())
	
				#Add artist to artists dataframe
				a = pd.Series(a.strip())
				ArtistsDataFrame = ArtistsDataFrame.append(a,ignore_index=True)

		
		#Replace artist in dataframe
		df.loc[index,"artists"] = str(new_lineup)
		
		#count iteration
		i+=1
		if(i%500==0):
			print(i)
	
	ArtistsDataFrame.columns=["artist"]

	ArtistsDataFrame.drop_duplicates()
	return ArtistsDataFrame,df

def downloadGenresSpotify(artistsDF,dictionarySpotify=None,begin=0,end=100000):

	Artists = artistsDF.copy()
	Artists = Artists.drop_duplicates().reset_index()[["artist"]]
	Artists.columns=["artist"]
	Artists["genres_spotify"]=None
	Artists["genres_ra"]=None
	Artists["genres_wiki"]=None
	Artists["genres_events"]=None
	Artists["main_genres"]=None
	Artists["top3_genres"]=None
	Artists["genre"]=None    
	
	if(end>Artists.shape[0]):
		end = Artists.shape[0]
        
	if(dictionarySpotify==None):
			dictionarySpotify = {}
	
	print("Downloading genres of "+str(end-begin)+" artist from Spotify...")
	last_read = 0
	for i in range(begin,end):
		S = Artists[Artists.index==i]
		artist = S["artist"].values[0]
		genres_spotify=None
		if(dictionarySpotify!=None and artist in dictionarySpotify):
			genres_spotify = dictionarySpotify.get(artist)
		else:
			genres_spotify = AE.getGenresFromSpotify(artist)
			dictionarySpotify.update({artist : genres_spotify})
			
		
		if(len(genres_spotify)<1):
			genres_spotify = None
		Artists.loc[Artists.index==i,"genres_spotify"] = str(genres_spotify)
		
		if(i%100==0):
			print(i)
			LU.saveDictionary(dictionarySpotify,filename_spotify_dic,PATH_DIC,encoding)
			
	LU.saveDictionary(dictionarySpotify,filename_spotify_dic,PATH_DIC,encoding)
	return Artists

def createDictionnaryFromArtists(artists):
	print("Creating dictionnary from genres downloaded from Spotify...")
	dic = AE.createDictionnary()
	genres_list = []
	for id,row in artists.iterrows():
		genres = literal_eval(row.genres_spotify)
		if(genres!=None):
			genres_list+=(genres)
		
	#print(genres_list)
	dic = AE.updateDictionnary(genres_list,dic)
	LU.saveDictionary(dic,filename_genres,PATH_DIC,encoding)
	return dic                   

def downloadGenresWikipediaAndRA(Artists,dictionaryOfGenres,dictionaryWiki=None, dictionaryRA=None, begin=0,end=100000):

	if(end>Artists.shape[0]):
		end = Artists.shape[0]
	
	#path = "FullData/ArtistDataframe_"+str(begin)+"_"+str(end)+".csv"
	print("Downloading genres from Wikipedia and Resident Advisor of "+str(end-begin)+" artist...")
	last_read = 0
	
	if(dictionaryWiki==None):
		dictionaryWiki = {}
	if(dictionaryRA==None):
		dictionaryRA = {}
	
	for i in range(begin,end):
		S = Artists[Artists.index==i]
		artist = S["artist"].values[0]
		
		#Get genres from wikipedia
		genres_wiki = None
		if(dictionaryWiki!=None and artist in dictionaryWiki):
			genres_wiki = dictionaryWiki.get(artist)
		else:
			genres_wiki = AE.getGenresFromWikipedia(artist,dictionaryOfGenres)
			dictionaryWiki.update({artist : genres_wiki})
			
			
		#Get genres from Resident Advisor
		genres_ra = None
		if(dictionaryRA!= None and artist in dictionaryRA):
			genres_ra = dictionaryRA.get(artist)
		else:
			genres_ra = AE.getGenresFromRA(artist,dictionaryOfGenres)
			dictionaryRA.update({artist : genres_ra})
		
		if(genres_wiki== None or len(genres_wiki)<1):
			genres_wiki = None
		if(genres_ra == None or len(genres_ra)<1):
			genres_ra = None
			
		Artists.loc[Artists.index==i,"genres_wiki"] = str(genres_wiki)
		Artists.loc[Artists.index==i,"genres_ra"] = str(genres_ra)

		if(i%100==0):
			print(str(i+1))
			LU.saveDictionary(dictionaryWiki,filename_wiki_dic,PATH_DIC,encoding)
			LU.saveDictionary(dictionaryRA,filename_ra_dic,PATH_DIC,encoding)
			
	#Saving dictionaries
	LU.saveDictionary(dictionaryWiki,filename_wiki_dic,PATH_DIC,encoding)
	LU.saveDictionary(dictionaryRA,filename_ra_dic,PATH_DIC,encoding)	
	return Artists
	
def computeGenresRatio(artists_df,dictionnaryOfGenres,debug=False):
	genres = list(set(dictionnaryOfGenres.values()))
	genres.append("unknown")
	
	#Extending
	#Getting columns
	columnsArtists = []
	for c in artists_df.columns:
		if("Unnamed" not in c):
			columnsArtists.append(c)
	columnsArtists = columnsArtists+genres+["total_genres"]
	print("Computing genres ratio...")
	i=0
	for id,row in artists_df.iterrows():
		i+=1
		if(debug and i%3000==0):
			print(i)
		main_genres = row["main_genres"]
		
		
		total = 0.0
		
		if(main_genres!=None and main_genres!="None"):
			try:
				total = len(literal_eval(main_genres))
			except:
				total = 0.0
            
			#Check if artist has a genre (from other dataframes)
			if(total==0):
				if(raw["genre"]!=None and raw["genre"]!="None"):
					main_genres = list(literal_eval(raw["genre"]))
					artists_df.loc[id,"main_genres"] = main_genres
					total = 1.0
				
		artists_df.loc[id,"total_genres"]=total
		
		#percententage of this genre
		for c in genres:
			if(total==0):
				artists_df.loc[id,c] = 0.0
				artists_df.loc[id,"unknown"]=1.0
			else:
				artists_df.loc[id,c] = main_genres.count(c)/total
				
	return artists_df

def computeMainGenres(artists,dictionnary):
    
    artists["all_genres"] = None
    
    i=0
    for id,row in artists.iterrows():
        i+=1
        if(i%1000==0):
            print(i)

        artist = row["artist"]
        genres_ra = literal_eval(row.genres_ra)
        genres_s = literal_eval(row.genres_spotify)
        genres_w = literal_eval(row.genres_wiki)
        #events
        genres_e = str(row.genres_events)
        genres_e = literal_eval(genres_e)
       
        if(genres_ra==None):
            genres_ra =[]
        if(genres_s == None):
            genres_s = []
        if(genres_w == None):
            genres_w = []
        if(genres_e == None):
            genres_e = []
            
        #Set genres_events to None if there already exist some genres
        if(len(genres_ra)>0 or len(genres_s)>0 or len(genres_w)>0):
            genres_e = []
        
        genres = genres_s+genres_ra+genres_w+genres_e
        
        main_genres = AE.mainGenres(genres,dictionnary)
        top3 = AE.getMaxGenre(main_genres,3)
        main_genre = None

        if(top3!=None and len(top3)>=1):
            main_genre = top3[0]
            
        #Assigning None values for empty lists
        if(len(main_genres)<1):
            main_genres = None
        if(len(genres_ra)<1):
            genres_ra = None
        if(len(genres)<1):
            genres = None
        if(len(genres_e)<1):
            genres_e = None
            
        artists.loc[id,"genres_ra"] = str(genres_ra)
        artists.loc[id,"main_genres"] = str(main_genres)
        artists.loc[id,"top3_genres"] = str(top3)
        artists.loc[id,"all_genres"] = str(genres)
        artists.loc[id,"genre"] = main_genre

    return artists
	
def fillGenresFromEvents(artists,events):
	print("Filling missing genres artists <- events")

	i =0
	for id, row in events.iterrows():
		i+=1
		if(i%1000==0):
			print(i)
		
		#getting genre
		str_genres = str(row["genre"])
		genres = []
		
		#case list
		if("[" in str_genres): 
			genres = literal_eval(str_genres)
		#case alone
		else:
			if(str_genres!="None" and str_genres!="nan"):
				genres.append(str_genres)
			
		#reformating
		genres_refo = []
		if(len(genres)>0):
			for g in genres:
				genres_refo.append(g.lower())
			genres = genres_refo
		else:
			genres=None
		#getting artist
		artists_lineup= str(row["artists"])
		
		lineup=[]
		if(artists_lineup!="nan" and artists_lineup!="None" and artists_lineup!=None):
			try:
				lineup = (literal_eval(artists_lineup))
			except:
				print("Malformed line-up : "+str(lineup))
				lineup=[]
        
		for a in lineup:
			artist = artists[artists.artist==a]
			genres_events = artist.genres_events.values
			if(len(genres_events)>0):
				genres_events = genres_events[0]
			else:
				genres_events = None
				
			genres_list = []
			if(genres_events!=None and "None" not in genres_events):
				genres_list+=literal_eval(str(genres_events))
			
			if(genres!=None):
				genres_list+=genres
			if(len(genres_list)<1):
				genres_list=None
				
			artists.loc[artists.artist==a,"genres_events"] = str(genres_list)
			
	return artists
	
def fillGenresEvents(events,artists,dictionnaryOfGenres):
	print("Filling missing genres events <- artists")
	
	i =0
	for id, row in events.iterrows():
		i+=1
		if(i%1000==0):
			print(i)
		
		lineup = str(row.artists)
		if(lineup!="nan" and lineup!="None" and lineup!=None):
			try:
				lineup = literal_eval(lineup)
			except:
				print("Malformed lineup :"+str(lineup))
				lineup=[]
		else:
			lineup = []
           
		genres_in_lineup = []
		
		#Adding each genre of artist to list genres_in_lineup
		for a in lineup:
			#Getting value
			artist = artists[artists.artist == a]
			genre_artist = None
			if(len(artist.genre.values)>0):
				genre_artist = artist.genre.values[0]
			
			#Add to list of genres   
			if(genre_artist!="nan" and genre_artist!="None" and genre_artist!=None):
				genres_in_lineup.append(genre_artist)
				
			
		#getting most representative genre among all artists
		maxGenre = AE.getMaxGenre(genres_in_lineup)
		#If an artist has a genre, then we set the genre of event to this artist genre
		if(maxGenre!=None):
			events.loc[id,"genre"] = maxGenre[0].lower()
		else:
			events.loc[id,"genre"] = None
	
	return events,artists

def artistsPipeline(Events,dictionaryOfGenres=None,dictionarySpotify=None,dictionaryRA=None,dictionaryWiki=None):
    if(dictionarySpotify==None):
        dictionarySpotify={}
    if(dictionaryRA ==None):
        dictionaryRA = {}
    if(dictionaryWiki ==None):
        dictionaryWiki = {}
    
    Artists,Events = getArtistsList(Events)
    Artists = downloadGenresSpotify(Artists,dictionarySpotify) #Assign first styles
    
    #Creating the dictionary from artists
    dicGenresArtists = createDictionnaryFromArtists(Artists)
    if(dictionaryOfGenres==None):
        dictionaryOfGenres = dicGenresArtists
    else:
        dictionaryOfGenres.update(dicGenresArtists)
    
    #Getting genres from Wiki And RA
    Artists = downloadGenresWikipediaAndRA(Artists,dictionaryOfGenres,dictionaryWiki,dictionaryRA)
    #Getting genres from Events
    Artists = fillGenresFromEvents(Artists,Events)
    
    #Compute extended fields
    Artists = computeMainGenres(Artists,dictionaryOfGenres)
    Artists = computeGenresRatio(Artists,dictionaryOfGenres)
    Events,Artists = fillGenresEvents(Events,Artists,dictionaryOfGenres)
    print("Computation of genres finished.")
    
    return Artists,Events,dictionaryOfGenres,dictionarySpotify,dictionaryRA,dictionaryWiki
	
	
	
if __name__ == '__main__':
	
	DataFrame = None
	SpotifyDic = None
	RADic = None
	WikiDic = None
	GenresDic = None
	
	#Getting the dataframe
	try:
		Dataframe = pd.read_csv(PATH_DF,index_col=0)
	except:
		print("Error occured during read of "+PATH_DF+". Maybe can't find the file.")
		sys.exit(0)
	
	#Getting the Spotify dictionary
	try:
		SpotifyDic = LU.loadDictionary(filename_spotify_dic,PATH_DIC,encoding)
	except:
		print("Can't find the dictionary of Spotify genres.")
		SpotifyDic = None
		
	#Getting the RA dictionary
	try:
		RADic = LU.loadDictionary(filename_ra_dic,PATH_DIC,encoding)
	except:
		print("Can't find the dictionary of RA genres.")
		RADic = None
		
	#Getting the Wikipedia dictionary
	try:
		WikiDic = LU.loadDictionary(filename_wiki_dic,PATH_DIC,encoding)
	except:
		print("Can't find the dictionary of Wikipedia genres.")
		WikiDic = None
	
	#Getting the dictionary of genres
	try:
		GenresDic = LU.loadDictionary(filename_genres,PATH_DIC,encoding)
	except:
		print("Can't find the dictionary of genres.")
		GenresDic = None
		
	#Running the pipeline
	artists,Dataframe, GenresDic, SpotifyDic, RADic, WikiDic = artistsPipeline(Dataframe, GenresDic, SpotifyDic, RADic, WikiDic)
	
	print("Saving artists dataframe to : "+PATH_ARTISTS)
	#Saving the Dataframe of artists
	artists.to_csv(PATH_ARTISTS)
	
	print("Saving cleaned dataframe to :"+PATH_DF)
	Dataframe.to_csv(PATH_DF)
	
	print("Saving dictionaries to : "+PATH_DIC)
	#Saving dictionaries
	LU.saveDictionary(GenresDic,filename_genres,PATH_DIC,encoding)
	LU.saveDictionary(SpotifyDic,filename_spotify_dic,PATH_DIC,encoding)
	LU.saveDictionary(RADic,filename_ra_dic,PATH_DIC,encoding)
	LU.saveDictionary(WikiDic,filename_wiki_dic,PATH_DIC,encoding)
	
	