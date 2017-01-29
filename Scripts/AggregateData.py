import sys
import os
import pandas as pd
import numpy as np

def aggregate(path,outputfile,encoding="utf-8"):
	print("Aggregating events data from folder : "+path)
	df = None
	file_list = sorted(os.listdir(path))
	for csv_file in file_list:
		if (df is None):
			df = pd.read_csv(path + '/' + csv_file,encoding=encoding)
		else:
			tmp = pd.read_csv(path + '/' + csv_file,encoding=encoding)
			df = df.append(tmp, ignore_index=True)

	df.to_csv(outputfile,encoding=encoding)
	print("Aggregation saved to : "+outputfile)

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        sys.exit("ERROR : not enough arguments. Require folder and output file")
    path = sys.argv[1]
    outputfile = sys.argv[2]
    aggregate(path,outputfile,encoding = "utf-8")
