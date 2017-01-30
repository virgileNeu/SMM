#!/usr/bin/env python
# coding=utf-8
# Author: Alexandre Connat ©

import pandas as pd
import os
import csv
import re

FOLDER_NAME = 'RDF-Data-Per-Day-Aggr'

file_list = os.listdir(FOLDER_NAME)
file_list.remove('.DS_Store')

df = None # The big general dataframe

for csv_file in file_list:

    try:
        if df is None:
            df = pd.read_csv(FOLDER_NAME + '/' + csv_file)
        else:
            df = df.append(pd.read_csv(FOLDER_NAME + '/' + csv_file), ignore_index=True)
    except:
        pass


# Clean erroneous entries :

df.dropna(axis=0, subset=['date'], inplace=True)

clean_df = pd.DataFrame(columns=df.columns)

j = 0
for i, row in df.iterrows():
    # if bool(re.search("\d{4}-\d{2}-\d{2}", str(row['date']))):
    if str(row['date'])[0].isdigit() and str(row['date'])[1].isdigit() and len(row['date']) == 10:
        # clean_df.append(row, ignore_index=True)
        clean_df.loc[j] = row
        j += 1

clean_df.to_csv('rdf-festivals-complete.csv')
