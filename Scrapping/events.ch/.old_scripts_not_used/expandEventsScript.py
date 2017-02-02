import numpy as np
import pandas as pd
import sys
sys.path.insert(0, '../Utils/')
import LocationUtils as lu

####### Script of the IPYNB, for comments and execution explanation see the IPYNB ###############

def usage():
    print("Add a coodinates column to the dataframe file given in parameters")
    print("Usage:")
    print("\tpython3 expandEventScript.py <df_source> (<df_dst> <location_dic>)")
    print("parameters:")
    print("\t<df_src> path to source dataframe file")
    print("\t<df_dst> optional path to destination dataframe file, default = completeWithCoordinates.csv")
    print("\t<dic_file> optional path to dictionary dataframe file, default = locationDic.csv")
    
def expand(df_src, df_dst="completeWithCoordinates.csv", dic_file="locationDic"):
    df = pd.read_csv(df_src)
    if('Unnamed: 0' in df.columns):
        df = df.drop('Unnamed: 0', 1)
    dic = lu.loadDictionary(dic_file)
    dic["Palais-des-Congrès"] = (47.134881, 7.248004000000001)
    dic["Il_Caffè"] = (46.9382202, 7.787970900000001)
    dic["Festivalgelände"] = (47.4222173, 9.3395195)
    dic["Festivalgelände-am-Rotten"] = dic["Festivalgelände"]
    dic["Römerareal"] = (47.136266, 7.30622)
    addCoordinatesColumn(df, dic, replace = True, inplace=True)
    lu.saveDictionary(dic, dic_file)
    df.to_csv(df_dst, index=False)
    
def addCoordinatesColumn(df, dictionary=None, location_column_name="location", coordinates_column_name = "coordinates",replace=False, inplace = False, debug=False):
    
    tmp = df.copy()
    if(coordinates_column_name in df.columns):
        if(replace):
            if(inplace):
                df.drop(coordinates_column_name,1, inplace=True)
            else:
                tmp.drop(coordinates_column_name,1, inplace=True)
        else:
            print("column ",coordinates_column_name," already in dataframe.")
            return 
    serie = pd.Series(data = np.nan, index = df.index, dtype = np.dtype)
    for (i,r) in df.iterrows():
        serie[i]= lu.getLocation(df.loc[i,location_column_name], dictionary)[0]
        if(debug and i%128 == 0): 
            print(i)
    if(inplace):
        df.insert(len(df.columns), coordinates_column_name,serie)
    else: 
        tmp.insert(len(tmp.columns), coordinates_column_name,serie)
        return tmp

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        usage()
        sys.exit("ERROR : not enough arguments.")
    if(len(sys.argv) > 4):
        usage()
        sys.exit("ERROR : too many arguments.")
    df_src = sys.argv[1]
    if(len(sys.argv) == 2):
        expand(df_src)
    elif(len(sys.argv) == 3):
        df_dst = sys.argv[2]
        expand(df_src, df_dst=df_dst)
    elif(len(sys.argv) == 4):
        dic_file=sys.argv[3]
        expand(df_src, df_dst=df_dst, dic_file=dic_file)
