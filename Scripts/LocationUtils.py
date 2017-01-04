import glob
import numpy as np
import pandas as pd
import json
import requests
import ArtistExtractor as AE

GOOGLE_API_KEY = "AIzaSyBHFQP-QhcaV7CG7o7-FLacHtlE0YI_E1E"

def getLocation(LocationName,dictionnary =None,SwissSafety=True):
	'''Returns the location of the club with a tuple (lat,lng)'''
	
	location = None
	lat = None
	lng = None
	
	if(dictionnary != None and (LocationName in dictionnary)):
		return dictionnary[LocationName],dictionnary
	else:
		if(location==None): #Try with geoCodeAPI
			baseURL1 = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
			try:
				location = getFromAPI(LocationName,baseURL1)
			except:
				location = None
            
		if(location==None): #Try with textSearchAPI
			baseURL2 = 'https://maps.googleapis.com/maps/api/geocode/json'
			try:
				location = getFromAPI(LocationName,baseURL2)
			except:
				location = None
            
		if(location == None): #Try usingAddressAPI
			#Try with address 
			address = getAddress(LocationName)
			if(address!=None):
				(lat,lng) = getLocation(address)
            
		else:
			#print("location is "+str(location))
			if(location!="ERROR"):
				lat = location['lat']
				lng = location['lng']
			else:
				lat = "ERROR"
				lng = "ERROR"
		
		#Checks if the club is in Switzerland
		if(SwissSafety and lat!=None and lng!=None):
			if(lng<5.7 or lng>10.73 or lat<45.6 or lat>47.9):
				#Out of Switzerland
				print("out of bounds")
				(lat,lng) = getLocation(LocationName+", Switzerland")
			
		if(dictionnary!=None):
			dictionnary.update({LocationName : (lat,lng)})
			return (lat,lng),dictionnary
			
def computeDictionaryOfLocations(df,debug=False):
	'''Map each location to a latlng'''
	dictionary = {}
	allClubs = set(df["Address"])
	nbClubs = len(allClubs)
	i = 0
	
	
	#Computing dictionnary
	if(debug):
		print("NbClubs : "+str(nbClubs))
		print("Begin mapping...")
	bTime = datetime.datetime.now()
	estimate = 123456
    
	for c in allClubs:
		locC = getLocation(c,dictionary)
		if(locC!=None):
			dictionary.update({c : locC[0]})
		else:
			dictionary.update({c : locC})
            
		if(debug and i%30==1):
			delta = datetime.datetime.now()-bTime
			estimate = (nbClubs-i)*delta/30
			timeLeft = bTime+estimate-datetime.datetime.now()
			print("{nb}/{to}, time left = {t}".format(nb = i, to = nbClubs, t=timeLeft))
			bTime = datetime.datetime.now()
		i = i+1
		
	if(debug):
		print("Computation finished!")

	return dictionary
	

def getFromAPI(LocationName,baseURL):
	'''Get infos from the API passed as baseURL'''
	param={}
	if("geocode" in baseURL):
		param = {'address': str(LocationName),
			'region':'ch',
			'key': GOOGLE_API_KEY}
	else:
		param = {'query': str(LocationName),
				#'keyword':'Switzerland',
				'key': GOOGLE_API_KEY}
    
	#baseURL = 'https://maps.googleapis.com/maps/api/geocode/json' #Get JSON for Geocode
	content = json.loads(requests.get(baseURL, params = param).text)
	
	if('error_message' in content):
		raise Exception()
    
	location = None
	if(len(content['results'])>0):
		location = content['results'][0]['geometry']['location']
		#print("ContentFound:"+str(location))

	return location
	
def getAddress(location,count=1):
	count = count-1
	#print(location)
	'''Returns the address of the club with a tuple'''
	param = {'address': str(location),
			'region':'ch',
			'key': GOOGLE_API_KEY}
    
	baseURL = 'https://maps.googleapis.com/maps/api/geocode/json' #Get JSON for Geocode
	content = json.loads(requests.get(baseURL, params = param).text)
	addressRes = None
	
	if(len(content['results'])>0):
		addressRes = content['results'][0]['formatted_address']
		print("result using geocode")
	else:
		#print("No result using geocode")
	#If no results, try another API to find the postal code and retry.
		param2 = {'query': str(location),
				'key': GOOGLE_API_KEY}    

		baseURL2 = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

		content2 = json.loads(requests.get(baseURL2, params = param2).text)
		if(len(content2['results'])>0):
			addressRes = content2['results'][0]['formatted_address']
			print("result using textsearch")
		
		if(addressRes==None and count>=0):
			addressRes = getAddress(str(location)+", Switzerland",count)
		else:
			#print("No results but : "+str(addressRes))
			return addressRes
    
	return addressRes
	
def saveDictionary(dic, filename):
	'''Save dictionnary as filename (txt)'''
	outfile = open('ClubDataGeo/'+filename+'.txt', 'w' )
	for key, value in sorted( dic.items() ):
		outfile.write( str(key) + '\t' + str(value) + '\n' )
		
def loadDictionary(filename):
	'''Load dictionnary'''
	inp = open('ClubDataGeo/'+filename+'.txt', 'r' )
	dic = {}
	for l in inp:
		line = inp.readline()
		s = line.split("\t")
		if(len(s)>1):
			s[1] = s[1].replace("\n","")
			dic.update({s[0]:s[1]})
		else:
			print(s)
	return dic

def populateDictionary(dic):
    append = {}
    for (key, val) in dic.items():
        good = False
        tmp = ""
        separators = [' ', ';']
        for c in separators:
            if(not good):
                tmp = key.split(c)
                if(len(tmp) == 2 and len(tmp[0]) == 4 and int(tmp[0]) >=1000 and int(tmp[0]) <= 9999): #format <NPA>c<CITY> with <NPA> on 4 digits
                    good=True
        if(good):
            (npa, city) = tmp
            if(not city in dic and not city in append):
                append.update({city:val})
    dic.update(append)
