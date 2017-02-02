import sys
import os
from events_utils import aggregate

# small function to merge all the small csv
if __name__ == "__main__":
    if(len(sys.argv) < 3):
        sys.exit("ERROR : not enough arguments. Require folder and output file")
    path = sys.argv[1]
    outputfile = sys.argv[2]
    aggregate(path,outputfile,encoding = "utf-8")
