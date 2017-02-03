import sys
from events_utils import *

def usages():
    print("Function to handle the events.ch website data")
    print("options:")
    print("\t-a <filename>: aggregate all the extracted data to the file <filename>")
    print("\t-e <date>: extract data on the website for the given date date.")
    print("\t-s <start_date> <end_date>: scrap data on the website between start_date and end_date.")
    print("\t-m <max_pages> : define the maximum amount of subpages scrap per date")
    print("\t-h: display this help.")

# Main function to be called with the terminal
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        usages()
        sys.exit("ERROR : not enough arguments.")
    args = sys.argv[1:] #remove the function name from the arg list
    filename=None
    start_date=None
    end_date=None
    max_pages=None
    while(len(args)>0):
        if(args[0] == "-a"):
            if(len(args) > 1):
                filename = args[1]
                args = args[2:]
            else:
                usages()
                sys.exit("Error : need filename argument")
        elif(args[0] == "-e"):
            if(len(args) > 1):
                start_date = args[1]
                args = args[2:]
            else:
                usages()
                sys.exit("Error : need date argument")
        elif(args[0] == "-m"):
            if(len(args) > 1):
                max_pages = args[1]
                args = args[2:]
            else:
                usages()
                sys.exit("Error : need max_pages argument")
        elif(args[0] == "-s"):
            if(len(args) > 2):
                start_date = args[1]
                end_date = args[2]
                args = args[3:]
            else:
                usages()
                sys.exit("Error : need start_date end end_date arguments")
        elif(args[0] == "-h"):
            usages()
            sys.exit()
    
    if(start_date != None):
        print("startDate: " + startDate)
        getEventsBetweenDate(startDate, endDate, maxPage)

    if(filename != None):
        aggregate("EventsChData/", filename)
