import pandas as pd
import numpy as np
import sys
sys.path.insert(0,'..\\Scripts\\Utils')
import ArtistExtractor as AE
import LocationUtils as LU
from ast import literal_eval
import moreFunction

def getArtistsList(df):
    print("Getting artists list from "+str(df.shape[0])+" events...")
    ArtistsDataFrame = pd.DataFrame()
    i=0
    for index,row in df.iterrows():
        lineup = row["artists"] #get line-up
        artists = literal_eval(lineup)
        
        new_lineup=[]
        for a in artists:
            a = a.split("(")[0]#Remove parenthesis at end of artist (record label, live act..)
            
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
        if(i%5000==0):
            print(i)
    
    ArtistsDataFrame.columns=["artist"]
    #ArtistsDataFrame.to_csv("ClubDataTest/ArtistsList.csv",encoding="utf-8")
    #ArtistsDataFrame.head(10)
    ArtistsDataFrame.drop_duplicates()
    return ArtistsDataFrame,df

def downloadGenresSpotify(artistsDF,dictionarySpotify=None,begin=0,end=100000):

    Artists = artistsDF.copy()
    Artists = Artists.drop_duplicates().reset_index()[["artist"]]
    Artists.columns=["artist"]
    Artists["genres_spotify"]=None
    Artists["genres_ra"]=None
    Artists["genres_wiki"]=None
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

        if(i%300==0):
            print(str(i+1))
            
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
            total = len(literal_eval(main_genres))
            
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
    #dictionnaryOfGenres = LU.loadDictionary("FullData/AllGenresDic",enc="utf-8")
    i=0
    for id,row in artists.iterrows():
        i+=1
        #if(i>20):
         #   break
        if(i%1000==0):
            print(i)

        artist = row["artist"]
        genres_ra = literal_eval(row.genres_ra)
        genres_s = literal_eval(row.genres_spotify)
        genres_w = literal_eval(row.genres_wiki)
       
        if(genres_ra==None):
            genres_ra =[]
        if(genres_s == None):
            genres_s = []
        if(genres_w == None):
            genres_w = []
        
        genres = genres_ra+genres_s+genres_w
        
        genres = genres_s+genres_ra+genres_w
        
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
            
        artists.loc[id,"genres_ra"] = str(genres_ra)
        artists.loc[id,"main_genres"] = str(main_genres)
        artists.loc[id,"top3_genres"] = str(top3)
        artists.loc[id,"all_genres"] = str(genres)
        artists.loc[id,"genre"] = main_genre


    #df3.to_csv("FullData/ArtistDF_withGenres.csv",encoding="utf-8")
    return artists

def artistsPipeline(Dataframe, dictionaryOfGenres=None,dictionarySpotify=None,dictionaryRA=None,dictionaryWiki=None):
    if(dictionarySpotify==None):
        dictionarySpotify={}
    if(dictionaryRA ==None):
        dictionaryRA = {}
    if(dictionaryWiki ==None):
        dictionaryWiki = {}
    
    Artists,Dataframe = getArtistsList(Dataframe)
    Artists = downloadGenresSpotify(Artists,dictionarySpotify) #Assign first styles
    
    #Creating the dictionary from artists
    dicGenresArtists = createDictionnaryFromArtists(Artists)
    if(dictionaryOfGenres==None):
        dictionaryOfGenres = dicGenresArtists
    else:
        dictionaryOfGenres.update(dicGenresArtists)
    
    #Getting genres from Wiki And RA
    Artists = downloadGenresWikipediaAndRA(Artists,dictionaryOfGenres,dictionaryWiki,dictionaryRA)
    
    #Compute extended fields
    Artists = computeMainGenres(Artists,dictionaryOfGenres)
    Artists = computeGenresRatio(Artists,dictionaryOfGenres)
    print("Pipeline of artists completed.")
    
    return Artists,Dataframe,dictionaryOfGenres,dictionarySpotify,dictionaryRA,dictionaryWiki
	
if __name__ == '__main__':

	PATH_DF = "TEST_Pipe.csv"
	PATH_ARTISTS = "Artists.csv"
	
	PATH_DIC = "Dictionaries/"
	
	filename_spotify_dic = "SpotifyDictionary"
	filename_ra_dic = "ResidentAdvisorDictionary"
	filename_wiki_dic = "WikipediaDictionary"
	filename_genres = "DictionaryOfGenres"
	
	DataFrame = None
	SpotifyDic = None
	RADic = None
	WikiDic = None
	GenresDic = None
	
	encoding="utf-8"
	
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
	
	