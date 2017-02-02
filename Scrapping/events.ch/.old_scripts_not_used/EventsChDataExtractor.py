from html.parser import HTMLParser
import urllib.request
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import sys
from events_utils import *

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
