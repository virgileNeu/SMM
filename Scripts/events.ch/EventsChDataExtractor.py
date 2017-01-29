from html.parser import HTMLParser
import urllib.request
import unidecode
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import sys

# Main function, return a dataframe for a given date with
# columns = location, event, date, artists, genre (can be None)
def getEventsForDate(date, maxPage=None):
    
    ############PARSER########
    # Main page Parser
    class MainHTMLParser(HTMLParser):
        def __init__(self, base_url):
            super( MainHTMLParser, self ).__init__()
            self.data = []
            self.base_url = base_url
            
        def handle_starttag(self, tag, attrs):
            if(tag=='a' and len(attrs)==3):
                href=attrs[1][1]
                subquerry_url = self.base_url + urllib.parse.quote(href)
                subpage = urllib.request.urlopen(subquerry_url).read().decode('utf-8')
                subparser = EventHTMLParser()
                subparser.feed(subpage)
                split = href.split('/')
                (artists, date) = subparser.getData()
                try:
                    currentDate = datetime.strptime(date, "%a %b %d %Y %H:%M:%S GMT%z (%Z)")
                    genres = split[2].split('-')
                    if(not(len(genres) == 1)):
                        genres = [None]
                    location = split[4]
                    festival = split[5]
                    if(len(artists) > 0):
                        self.data.append((location, festival, datetime.strftime(currentDate, "%Y-%m-%d"), artists, genres[0]))
                except:
                    print("page failed :",subquerry_url)
        def getData(self):
            return self.data
    # Subpage Parser
    class EventHTMLParser(HTMLParser):
        def __init__(self):
            super( EventHTMLParser, self ).__init__()
            self.artist_string = ""
            self.date = ""
            self.grab_artists = False
            self.artists = []
        
        def handle_starttag(self, tag, attrs):
            if(tag == 'h2' and len(attrs) == 2 and attrs[1][1] == "event-subtitle"):
                self.grab_artists = True
            if(tag == 'time' and attrs[0][0] == 'datetime' and self.date == ""):
                self.date = attrs[0][1]
            
        def handle_endtag(self, tag):
            self.grab_artists = False

        def handle_data(self, data):
            if(self.grab_artists == True):
                self.artist_string = data
        
        def cleanArtists(self):
            temp = self.artist_string.split(',')
            for s in temp:
                if('(' in s):
                    self.artists.append(s.split('(')[0])
        
        def getData(self):
            self.cleanArtists()
            return (self.artists, self.date)
            
    ########END OF PARSERS##############
    
    (year, month, day) = date.split('-')
    # small date check (1848 = creation of Swiss constitution)
    if(int(year) < 1848 or int(year) > 2020 or int(month) < 0 or int(month) > 12 or int(day) < 0 or int(day) > 31):
        sys.exit("ERROR : incorrect start date")
    data = []
    base_url = u"https://events.ch"
    language = u"en"
    action = u"search"    
    end_search = u"6/cs"
    eventType = u"concerts"
    tempData = []
    page_number = 1
    while(maxPage == None or page_number <= maxPage):
        print("page_number:" + str(page_number))
        querry_url = base_url + '/'+ language + '/' + action + '/' + eventType + '/' + date + '/' + end_search + '/' + str(page_number)
        page = urllib.request.urlopen(querry_url).read().decode('utf-8')
        parser = MainHTMLParser(base_url)
        parser.feed(page)
        tempData = parser.getData()
        for l in tempData:
            (location, festival, date_string, artists, genre) = l
            (currentYear, currentMonth, currentDay) = date_string.split('-')
            if(len(tempData) == 0):
                print("no data")
                return (data, None)
            if(year < currentYear or (year == currentYear and month < currentMonth) or (year == currentYear and month == currentMonth) and day < currentDay):
                return (data, date_string)
            data = data + [(location, festival, date_string, artists, genre)]
        page_number = page_number + 1
    print("max number of pages reach")
    return (data, None)
    
# Get and save the dataframe as a csv file "YYYY-MM-DD.csv"
def getCSVForDates(date, maxPage = None):
    (data, retdate) = getEventsForDate(date, maxPage)
    print(retdate)
    if(len(data) > 0):
        df = pd.DataFrame(data, columns=['location', 'event', 'date', 'artists', 'genre'])
        print("df written for date " + date)
        df.to_csv("EventsChData/"+date + ".csv")
    return retdate

# Return a list of date between a given start_date and a given end_date
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Main function to be called with the terminal
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        sys.exit("ERROR : not enough arguments. Give at least the start date yyyy-mm-dd")
    startDate = sys.argv[1]
    print("startDate: " + startDate)
    endDate = None
    if(len(sys.argv) > 2):
        endDate = sys.argv[2]
        print("endDate: " + endDate)
    maxPage = None
    if(len(sys.argv) > 3):
        maxPage = int(sys.argv[3])
        print("maxPage: " + str(maxPage))
    (startYear, startMonth, startDay) = startDate.split('-')
    if(endDate == None):
        getCSVForDates(startDate, maxPage)
    else:
        (endYear, endMonth, endDay) = endDate.split('-')
        startDateObject = date(int(startYear), int(startMonth), int(startDay))
        endDateObject = date(int(endYear), int(endMonth), int(endDay))
        d = startDateObject
        delta = timedelta(days=1)
        while d <= endDateObject:
            try:
                print("current date: ",d)
                nextDate = getCSVForDates('%04d-%02d-%02d' % (d.year, d.month, d.day), maxPage)
                if(nextDate == None):
                    d += delta
                else:
                    (nextYear, nextMonth, nextDay) = nextDate.split('-')
                    d = date(int(nextYear), int(nextMonth), int(nextDay))
            except KeyboardInterrupt:
                raise # Enable CTRL+C exit
            except:
                print("Exception, starting again date ")
