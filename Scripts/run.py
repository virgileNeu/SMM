import sys
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import EventsChDataExtractor
import ResidentAdvisor_scrapping
import AggregateData

if __name__ == "__main__":
	print("-----EVENTCH EXTRACTOR-----")
	startDateObject = date(2016,11,22)
	endDateObject = date(2017,1,29)
	
	eventsch_path_folder = "EventsChDataTest/"
	merging_path_folder = "MergingTest/"
	
	outputfile_eventsch = merging_path_folder+"EventsMerged.csv"
	output_file =merging_path_folder+"AllMerged.csv"
	
	maxPage = 1
	#EventsChDataExtractor.getEventsBetween(startDateObject,endDateObject,maxPage,eventsch_path_folder)
	#AggregateData.aggregate(eventsch_path_folder,outputfile_eventsch)
	
	filename = merging_path_folder+"ClubMerged.csv"
	ResidentAdvisor_scrapping.scrap(filename, start=0,end=2,encoding = "utf-8")
	
	AggregateData.aggregate(merging_path_folder,output_file)