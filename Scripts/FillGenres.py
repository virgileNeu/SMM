import numpy as np
import ArtistExtractor as AE
import pandas as pd
import glob
import os
import LocationUtils as LU
from ExtractGenreClubs import SplitLineup
from ast import literal_eval
import logging
import desaggregate
import moreFunction

def fillGenres(events,artists,dictionnaryOfGenres,encoding = "utf-8"):
    print("---BEGIN MERGE----")
    print("This script takes approximately one hour to perform")
    
    dataframe_merged = events.copy()
    
    cleanArtistDF(artists)
    
    #Getting columns
    columnsArtists = []
    columnsEvents = []
    for c in artists.columns:
        if("Unnamed" not in c):
            columnsArtists.append(c)
    
    for c in events.columns:
        if("Unnamed" not in c):
            columnsEvents.append(c)
           
    logging.basicConfig(filename='LOG/merging_events_and_artists.log',level=logging.DEBUG)
    
    i =0
    for id, row in dataframe_merged.iterrows():
        logging.info("-------------------------------")
        i+=1
        if(i%1000==0):
            print(i)
            #Saving actual state
            artists = artists[columnsArtists]
            events = events[columnsEvents]
            #artists.to_csv(artists_filename.replace(".csv","_merged.csv"),encoding=encoding)
            #events.to_csv(eventsdf_filename.replace(".csv","_merged.csv"),encoding=encoding)
        
        #getting genre
        genre = str(row["genre"])
        #getting artist
        lineup = moreFunction.clean_artists(literal_eval(row["artists"]))
        #remplace
        events.loc[id,"artists"] = str(lineup)
        logging.info(lineup)
        
        #looking for corresponding genre in dictionnary:
        maingenre = dictionnaryOfGenres.get(genre.lower())

        logging.info("event genre is: "+str(genre)+"->"+str(maingenre))

        maxGenre = None
        #check if artists has a genre to complete artists database
        if(maingenre!="None" and maingenre!=None and maingenre in dictionnaryOfGenres):
            for a in lineup:
                
                #Getting value
                vals = artists[artists["artist"] == a.strip()]["genre"].values
                genre_artist = "None"
                if(len(vals)>0):
                    genre_artist = str(vals[0])
                    
                #Setting artist genre
                if(genre_artist=="nan" or genre_artist=="None"):
                    #set genre of artist to genre of event and convert genre in dataframe
                    artists.loc[artists["artist"] == a.strip(),"genre"] = maingenre.lower()
                    maxGenre = maingenre.lower()
                    logging.info(str(a)+"<-"+maingenre.lower())
        
        genres_in_lineup = []
        
        for a in lineup:
            
            #Getting value
            vals = artists[artists["artist"] == a.strip()]["genre"].values
            genre_artist = "None"
            if(len(vals)>0):
                genre_artist = str(vals[0])
                
            #Getting corresponding maingenre for this artist   
            if(genre_artist!="nan" and genre_artist!="None" and genre_artist!=None):
                genres_in_lineup.append(genre_artist)
            
        #getting most representative genre among all artists
        maxGenre = AE.getMaxGenre(genres_in_lineup)
        
        #If an artist has a genre, then we set the genre of event to this artist genre
        if(maxGenre!=None):
            logging.info("From lineup : "+str(genres_in_lineup)+"->"+str(maxGenre[0]))
            if(maxGenre[0] in dictionnaryOfGenres):
                events.loc[id,"genre"] = maxGenre[0].lower()
            else:
                #Not in dictionnary
                events.loc[id,"genre"] = None
        else:
            events.loc[id,"genre"] = None
    
    artists = artists[columnsArtists]
    events = events[columnsEvents]
    #artists.to_csv(artists_filename.replace(".csv","_merged.csv"),encoding=encoding)
    #events.to_csv(eventsdf_filename.replace(".csv","_merged.csv"),encoding=encoding)
    
    return events,artists