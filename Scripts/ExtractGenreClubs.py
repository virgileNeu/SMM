#!/usr/bin/python

import numpy as np
import ArtistExtractor as AE
import pandas as pd
import glob
import os
import LocationUtils as LU
import sys

def SplitLineup(st):
	'''Splits the artists in the line-up'''
	cleaned = ""
	for i in st:
		if(i.isalnum() or i==" " or i=="," or i == "(" or i==")" or i == "&"):
			cleaned+=i
	clean_lineup = cleaned.split(",")
	artists = []
	for a in clean_lineup:
		a = dropLabel(a)
		if(len(a)>1):
			artists.append(a.strip())
    
	return artists

def dropLabel(artist):
	'''Drop the label (if present) in the artist name'''
	a = ""
	for i in artist :
		if(i=="(" or i==")"):
			break
		a+=i
	return a 
	

def main():
	args = sys.argv
	
	if(len(args)>3):
		print("Please provide up to 2 arguments")
		
	files = []
	files = glob.glob("ClubData0/*.csv")+glob.glob("ClubData1/*.csv")+glob.glob("ClubData2/*.csv")+glob.glob("ClubData3/*.csv")
	print("Files : "+str(len(files)))
	ClubDataFrame = pd.read_csv(files[0],sep="\t")
	print("Loading dataframe...")
	for file in files:
		df= pd.read_csv(file,sep ="\t")
		ClubDataFrame = ClubDataFrame.append(df,ignore_index = True)

	print("Done!")
	#Drop Useless columns
	ClubDataFrame = ClubDataFrame.drop('Unnamed: 0', 1)
	ClubDataFrame.reset_index()
	
	init = 0
	end = ClubDataFrame.shape[0]
	
	if(len(args)==2):
		init = int(args[1])
	if(len(args)==3):
		init = int(args[1])
		end = int(args[2])
	
	## Getting artists genres
	print("Preparing for genre exportation : ")
	
	ExportGenres(ClubDataFrame.copy(),init,end)
	

def ExportGenres(ClubDataFrame,init,end):

	ArtistsSet = set()
	ArtistDicoMain = dict()
	ArtistDicoAll = dict()
	
	filenameMain = "ArtistDicoMain-"+str(init)+"-"+str(end)+"-temp"
	filenameAll = "ArtistDicoAll-"+str(init)+"-"+str(end)+"-temp"

	try:
		ArtistDicoMain = LU.loadDictionary(filenameMain,path = "Artists/")
		ArtistDicoAll = LU.loadDictionary(filenameAll,path = "Artists/")
		ArtistsSet = set(ArtistDicoMain.keys())
	except:
		print("Cannot find dictionnaries")
	
	ClubDataFrame["Genre"] = None
	ClubDataFrame["All Genres"] = None

	print("Retrieving genre for events[" +str(init)+","+str(end)+"] :")

	i=0
	for id,row in ClubDataFrame[init:end].iterrows():
		genres = []
		lineup = row["LineUp"]
		artists = SplitLineup(lineup)

		for artist in artists:
			mainGenre = None
			allGenres = None
			
			if(artist in ArtistsSet):
				mainGenre = ArtistDicoMain.get(artist)
				allGenres = ArtistDicoAll.get(artist)
			else:
				#Updating dictionnaries
				ArtistsSet.add(artist)
				allGenres = AE.getGenre(artist,ReturnAllGenres=True)
				mainGenre = AE.getMaxGenre(allGenres)
				ArtistDicoMain.update({artist : mainGenre})
				ArtistDicoAll.update({artist : allGenres})
			
			#Adding to LineUp genres
			genres.append(mainGenre) 
			
				
		if(len(genres)==0):
			print(artists)
		else:
			maxGenre =AE.getMaxGenre(genres)
			#updating dataframe
			ClubDataFrame = ClubDataFrame.set_value(id,"Genre",maxGenre)
			ClubDataFrame = ClubDataFrame.set_value(id,"All Genres",str(genres))
			ClubDataFrame = ClubDataFrame.set_value(id,"LineUp",str(artists))
			
		i+=1
		if(i%10==0):
			print(str(i))
		if(i%50==0):
			LU.saveDictionary(ArtistDicoMain,filenameMain,path = "Artists/",enc="UTF-8")
			LU.saveDictionary(ArtistDicoAll,filenameAll,path = "Artists/",enc="UTF-8")
			
	print("Extraction finished. Saving dictionnaries..")
	LU.saveDictionary(ArtistDicoMain,filenameMain,path = "Artists/",enc="UTF-8")
	LU.saveDictionary(ArtistDicoAll,filenameAll,path = "Artists/",enc="UTF-8")	
	print("Finished.")
	
if __name__ == "__main__":
    main()
	