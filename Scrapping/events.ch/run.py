import sys
from events_utils import *

# Main function to be called with the terminal
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        sys.exit("ERROR : not enough arguments. Give at least the start date yyyy-mm-dd")
    startDate = sys.argv[1]
    print("startDate: " + startDate)
    filename = "EventsCh.csv"
    if(len(sys.argv) > 2):
        filename = sys.argv[2]
    print("resulting file: " + filename)
    endDate = None
    if(len(sys.argv) > 3):
        endDate = sys.argv[3]
        print("endDate: " + endDate)
    maxPage = None
    if(len(sys.argv) > 4):
        maxPage = int(sys.argv[4])
        print("maxPage: " + str(maxPage))
    
    getEventsBetweenDate(startDate, endDate, maxPage)
    aggregate("EventsChData/", filename)
    
