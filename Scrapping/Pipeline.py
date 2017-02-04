import pandas as pd
import numpy as np
import json
import bs4
import requests
import sys as system
system.path.insert(0,'..\\Scripts\\Utils')
from LocationUtils import loadDictionary,saveDictionary

GOOGLE_API_KEY = "AIzaSyBHFQP-QhcaV7CG7o7-FLacHtlE0YI_E1E"

PATH_DIC = "Dictionaries/"	
filename_locality_dic = "LocalityDictionary"
filename_region_dic = "AddressDictionary"
filename_coordinates_dic = "CoordinatesDictionary"
encoding="utf-8"

#Adding location of the "club"
def getCanton(address_info,dictionnaryRegion=None,dictionnaryLocality=None,dictionnaryCoordinates=None,SwissSafety=True):
	'''Returns the location of the club with a tuple (lat,lng)'''

	address_info = str(address_info).replace(";",",")
	region=None
	locality = None
	lat = None
	lng = None
	coordinates = None	
	
	if(dictionnaryRegion != None and (address_info in dictionnaryRegion)):
		region = dictionnaryRegion[address_info]

	if(dictionnaryLocality != None and (address_info in dictionnaryLocality)):
		locality = dictionnaryLocality[address_info]

	if(dictionnaryCoordinates !=None and (address_info in dictionnaryCoordinates)):
		coordinates = dictionnaryCoordinates[address_info]	
		
	if(locality !=None and region!=None and coordinates!=None):
		return region,locality,coordinates

	else:
		if(locality==None): #Try with geoCodeAPI
			baseURL1 = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
			try:
				region,locality,coordinates = getFromAPI(address_info,baseURL1)
			except:
				region,locality,coordinates  = None,None,None

		if(locality==None): #Try with textSearchAPI
			baseURL2 = 'https://maps.googleapis.com/maps/api/geocode/json'
			try:
				region,locality,coordinates  = getFromAPI(address_info,baseURL2)
			except:
				region,locality,coordinates  = None,None,None

		#If nothing found
		if(region==None and locality==None):
			address_comp = list(address_info.split(","))[::-1]

			#timeout
			timeout = 5
			i = 0
			if(len(address_comp)>1):
				for ac in address_comp:
					i+=1
					region,locality,coordinates = getCanton(ac,None,None)
					if(region!=None):
						break
					if(i>timeout):
						break

		if(dictionnaryRegion!=None):
			dictionnaryRegion.update({address_info : region})
		if(dictionnaryLocality!=None):
			dictionnaryLocality.update({address_info : locality})
		if(dictionnaryCoordinates!=None):
			dictionnaryCoordinates.update({address_info : coordinates})
			
	return region, locality, coordinates

def getFromAPI(clubName,baseURL):
	param={}
	if("geocode" in baseURL):
		param = {'address': str(clubName),
				'region':'ch',
				'key': GOOGLE_API_KEY
				}
	else:
		param = {'query': str(clubName),
				#'keyword':'Switzerland',
				'key': GOOGLE_API_KEY
				}

	#baseURL = 'https://maps.googleapis.com/maps/api/geocode/json' #Get JSON for Geocode
	content = json.loads(requests.get(baseURL, params = param).text)
	if('error_message' in content):
		raise Exception()
	coordinates = None
	if(len(content['results'])>0):
		coordinates = content['results'][0]['geometry']['location']
		addr_comp = content['results'][0]['address_components']
		region = None
		locality = None

		for r in addr_comp:
			if("administrative_area_level_1" in str(r)):
				region = r['short_name']
			if("locality" in str(r)):
				locality = r['short_name']	
		
		geocoordinates=None
		if coordinates != None:
			geocoordinates = str((coordinates['lat'], coordinates['lng']))
		
	return region,locality,geocoordinates


def completeGeographicData(dataframe,RegionDic=None,LocalityDic=None,CoordinatesDic=None):
	dataframe['canton'] = None
	dataframe = dataframe[["place" ,"src","address","location","canton","event" ,
							"date","artists","genre","coordinates"]]

	if(RegionDic==None or LocalityDic==None or CoordinatesDic==None):
		RegionDic = {}
		LocalityDic = {}
		CoordinatesDic = {}
		#Getting the dictionaries
		try:
			RegionDic = loadDictionary(filename_region_dic,PATH_DIC,encoding)
			print("loaded "+filename_region_dic)
		except:
			print("Can't find the dictionary of regions.")
			RegionDic={}
		
		try:
			LocalityDic = loadDictionary(filename_locality_dic,PATH_DIC,encoding)
			print("loaded "+filename_locality_dic)
		except:
			print("Can't find the dictionary of localities.")
			LocalityDic={}
		
		try:
			CoordinatesDic = loadDictionary(filename_coordinates_dic,PATH_DIC,encoding)
			print("loaded "+filename_coordinates_dic)
		except:
			print("Can't find the dictionary of coordinates.")
			CoordinatesDic={}

	i = 0
	size = str(dataframe.shape[0])
	print("Retrieving geographic data for "+size+" events..")
	
	for id,row in dataframe.iterrows():

		i+=1
		if(i%1000==0):
			print(str(i)+"/"+size)
			saveDictionary(RegionDic,filename_region_dic,PATH_DIC,encoding)
			saveDictionary(LocalityDic,filename_locality_dic,PATH_DIC,encoding)
			saveDictionary(CoordinatesDic,filename_coordinates_dic,PATH_DIC,encoding)

		place = row.place
		address = row.address
		location = row.location
		region = None
		locality = None
		coordinates = None	
		
		#Replace invalid location
		if(":" in str(location) or "{" in str(location) or "nan" in str(location).lower()):
			location = None

		noneLocation = (location == None or str(location)=="nan")

		if(noneLocation and address!=None):
			region,locality,coordinates = getCanton(address,RegionDic,LocalityDic,CoordinatesDic)

		elif(noneLocation == None and place!=None):
			region,locality,coordinates = getCanton(place,RegionDic,LocalityDic,CoordinatesDic)	
		elif(location != None):
			region,locality,coordinates = getCanton(location,RegionDic,LocalityDic,CoordinatesDic)	

		dataframe.loc[id,"location"] = locality
		dataframe.loc[id,"canton"] = region
		dataframe.loc[id,"coordinates"] = coordinates

		
	saveDictionary(RegionDic,filename_region_dic,PATH_DIC,encoding)
	saveDictionary(LocalityDic,filename_locality_dic,PATH_DIC,encoding)
	saveDictionary(CoordinatesDic,filename_coordinates_dic,PATH_DIC,encoding)
	return dataframe,RegionDic,LocalityDic,CoordinatesDic
