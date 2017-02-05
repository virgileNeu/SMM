import numpy as np
import pandas as pd
from ast import literal_eval
import sys


def desaggregate(df, verbose):
    cols = list(df.columns)
    cols.remove("artists")
    cols.insert(0, "artist")
    res = pd.DataFrame(columns=cols)
    for (i,r) in df.iterrows():
        for a in literal_eval(r.artists):
            artist = a.strip() #remove ' '
            lst = [artist, r.place, r.src, r.address, r.location, r.canton, r.event, r.date, r.genre, r.coordinates]
            if(verbose):
                print(lst)
            res.loc[res.shape[0]] = lst
    return res

def print_usage():
    print("Usage:")
    print("desaggregate <options> <source dataframe> <file_destination>")
    print("options:")
    print("-e <encoding> : encoding string, 'utf-8', 'ISO-8859-1', default value = ISO-8859-1")
    print("-v : verbose, print the new dataframe in terminal")
    
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print_usage()
        sys.exit("ERROR : not enough arguments.")
    args = sys.argv[1:] #remove script name
    encoding = "ISO-8859-1"
    verbose = False
    while(len(args) > 2):
        if(len(args) > 3 and args[0] == "-e"):
            encoding = args[1]
            args = args[2:]
        elif(args[0] == "-v"):
            verbose = True
            args = args[1:]
        else:
            print_usage()
            sys.exit("ERROR : wrong arguments.")
    file_src = args[0]
    file_dest = args[1]
    try:
        df = pd.read_csv(file_src, encoding=encoding)
    except FileNotFoundError:
        print_usage()
        sys.exit("Error : specify the source file")
    if('Unnamed: 0' in df.columns):
        df = df.drop('Unnamed: 0', 1)
    res = desaggregate(df, verbose)
    
    res.to_csv(file_dest, index=False, encoding=encoding)

