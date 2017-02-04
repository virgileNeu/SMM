import numpy as np
import pandas as pd
import requests
import bs4
import glob
import json
import sys
import time
import sys
sys.path.insert(0,'..\\..\\Scripts\\Utils')
import ArtistExtractor as AE
from dateutil.parser import parse

def getListOfClubs():
	baseURL = "https://www.residentadvisor.net/"
	clubListURL = "https://www.residentadvisor.net/clubs.aspx"
	content = requests.get(clubListURL).text

	soup = bs4.BeautifulSoup(content, "html5lib")

	clubDF = pd.DataFrame(columns = ["clubID","place","address"])

	for tdTag in soup.findAll('li'):
		for clubs in tdTag.findAll('li'):
			if('class' in clubs.attrs and len(clubs)==2):
				#Parsing infos
				clubID = "null"
				address = "null"
				name = "null"
				for line in clubs:
					if(line.a == None):
						address = line.text
					else:
						name = line.text
						clubID = line.a['href'].split("=")[1]
				#print(str(clubID)+",,"+str(adress)+",,"+str(name))
				df = pd.Series([clubID,name,address],['clubID','place','address'])
				clubDF = clubDF.append(df, ignore_index=True)
				#print(df) 
	return clubDF
	
def getEventsFrom(clubIndex):
    '''Gets dataframe of events for a club'''
    ClubURL = "https://www.residentadvisor.net/club.aspx?id="+str(clubIndex)+""
    content = ""
    DFEvents = pd.DataFrame(columns = ['clubID','eventID','event','date','artists'])
    
    try:
        content = requests.get(ClubURL).text
    except:
        print("Error getting : "+ClubURL)
        return DFEvents
        
    soup = bs4.BeautifulSoup(content, "html5lib")
    
    eventIDList = list() #List of eventsID to be analysed
    
    #Parsing page to get eventIDs
    for sections in soup.findAll('section'):
        for links in sections.findAll('a'):
            if(len(links.attrs)==2 and 'itemprop' in links.attrs):
                link = links['href']
                eventID = link.split('?')[1]
                eventIDList.append(eventID) #Add eventID to list
    
    
    for eid in eventIDList:
        series = getSerieFromEvent(clubIndex,eid)
        DFEvents = DFEvents.append(series,ignore_index=True)
    
    DFEvents.clubID = DFEvents.clubID.astype(int)
    return DFEvents
	
def getSerieFromEvent(clubInd,eventID):
    '''Returns a Serie [EventID,EventName,Date,LineUp] for the eventID passed as argument'''
    EventURL = 'https://www.residentadvisor.net/event.aspx?'+str(eventID)
    content = ""
    
    try:
        content = requests.get(EventURL).text
    except:
        print("Error getting : "+EventURL)
        return None
    
    soup = bs4.BeautifulSoup(content, "html5lib")
    
    day = ''
    date = ''
    lineup = set()
    title = ''
    
    #Get LineUp
    for ul in soup.findAll('ul'):
        for div in ul.findAll('div'):
            if('Line' in div.text):
                for p in div.findAll('p'):
                    if('class' in p.attrs and p['class']!=None):
                        artists = p.text.split(',')
                        for a in artists:
                            splitted = a.split("\n")
                            for arts in splitted:
                                lineup.add(arts)
            
    #Get title and Date of the event
    for meta in soup.findAll('meta'):
        if('property' in meta.attrs ):
            if(meta['property']=='og:title'):
                title = meta['content']
            if(meta['property']=='og:description'):
                datestr = meta['content']
                val = datestr.split(",")
                date = val[1].split("-")[0]
                day = val[0]
    
    lineup = list(lineup)
    data =[int(clubInd), eventID, title,reformatDate(date),lineup]
    S = pd.Series(data,['clubID','eventID','event','date','artists'])

    return S
	
def getDataframesOfEvents(clubDF,start=0,end=10000000):
	if(end>=len(clubDF.values)):
		end = len(clubDF.values)
	total = end-start
	i = 0
	print("Creating dataframes of events for each clubs : ")
	
	for d in clubDF.values[start:end]:
		#Get Event Dataframe for this indexOfClub
		indexOfClub = d[0] #
		
		print("Club number : "+str(i+1)+"/"+str(total))
		
		df = getEventsFrom(indexOfClub)
		#Add Columns Name and Adress
		df['place'] = d[1]
		df['address'] = d[2]
		#Reformat Dataframe
		df = df[['clubID','place','address','eventID','event','date','artists']]
		file_name = d[1]
		file_name = file_name.replace(u"/"," ").replace(u"*"," ")
		file_name = d[0]+"-"+file_name
		
	
		
		df = df[['place','address','event','date','artists']]
		#Save as CSV
		try:
			saving_to = 'ClubData/'+file_name+".csv"
			print("Saved dataframe to : "+saving_to)
			df.to_csv(saving_to,sep ='\t', encoding='utf-8')
		except:
			print("ERROR AT INDEX"+str(i)+", index : "+str(indexOfClub)+", file_name = "+str(file_name))
		#console output
		i = i+1
	
	print("Done.")
		
def reformatDate(value):
    #a = ClubDataFrame["Date"]
    d = value
    date = time.strftime('%Y-%m-%d')
    return date

def mergeClubData(encoding = "utf-8"):
	files = []
	files = glob.glob("ClubData/*.csv")
	print("Merging all clubs dataframe together...")
	print("Total : "+str(len(files))+"files")
	ClubDataFrame = pd.read_csv(files[0],sep="\t",encoding=encoding)

	for file in files:
		df= pd.read_csv(file,sep ="\t",encoding=encoding,index_col=0)
		ClubDataFrame = ClubDataFrame.append(df,ignore_index = True)
	
	print("Done.")
	return ClubDataFrame
    

def scrap(filename, start=0,end=1000000,encoding = "utf-8"):
	clubDF = getListOfClubs()
	if(end>len(clubDF.values)):
		end = len(clubDF.values)
	getDataframesOfEvents(clubDF,start,end)
	ClubDataFrame = mergeClubData(encoding)
	ClubDataFrame = ClubDataFrame[['place','address','event','date','artists']]
	ClubDataFrame.to_csv(filename,encoding = encoding)
	print("File saved to : "+filename)
	
def print_usage():
    print("Usage:")
    print("ResidentAdvisor_scrapping <file_destination> <start_index> <end_index>")
    #print("options:")
    #print("-e <encoding> : encoding string, 'utf-8', 'ISO-8859-1', default value = ISO-8859-1")
    #print("-v : verbose, print the new dataframe in terminal")
	
if __name__ == "__main__":
	if(len(sys.argv) < 2):
		print_usage()
		sys.exit("ERROR : You must provide a destination for the file.")
	
	args = sys.argv[1:] #remove script name
	encoding = "ISO-8859-1"
	verbose = False
	
	file_destination = ""
	encoding_ = "utf-8"
	
	if(len(args)>=1):
		file_destination = args[0].strip()
		
		start = 0
		end = 1000000
		
		if(len(args)>1):
			try:
				start = int(args[1])
				if(start<0):
					print("Error : bad start index given. Must be an positive int.")
					sys.exit("ERROR : wrong arguments.")
			except:
				print("Error : bad start index given. Must be an positive int.")
				sys.exit("ERROR : wrong arguments.")
			
			if(len(args)>2):
				try:
					end = int(args[2])
					if(end<0):
						print("Error : bad end index given. Must be an positive int.")
						sys.exit("ERROR : wrong arguments.")
				except:
					print("Error : bad end index given. Must be an positive int.")
					sys.exit("ERROR : wrong arguments.")
	
	print("--------RESIDENT ADVISOR DATA SCRAPPING-------------")
	print("Parameters : \n"+"\tOutput : "+file_destination+"\n\tStart : "+str(start)+"\n\tEnd : "+str(end))
	print("Number of clubs getting scrapped : "+str(end-start))
	print("Begin...")
	scrap(file_destination,start,end,encoding = encoding_)
	
	