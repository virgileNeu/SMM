#!/usr/bin/env python
# coding=utf-8
# Author: Alexandre Connat ©

import pandas as pd
import csv
import os
import re
import glob
import requests
import time
import json

IN_FOLDER_NAME = 'RDF-Data-Per-Festival'

df = None

file_list = os.listdir(IN_FOLDER_NAME)
file_list.remove('.DS_Store')
for csv_file in file_list:
    if (df is None):
        df = pd.read_csv(IN_FOLDER_NAME + '/' + csv_file)
    else:
        df = df.append(pd.read_csv(IN_FOLDER_NAME + '/' + csv_file), ignore_index=True)

date2 = []

for date in df['date']:
    d = date
    d = d.replace('Jan.', '01')
    d = d.replace('Fev.', '02')
    d = d.replace('Mar.', '03')
    d = d.replace('Avr.', '04')
    d = d.replace('Mai', '05')
    d = d.replace('Juin', '06')
    d = d.replace('Juil.', '07')
    d = d.replace('Aout', '08')
    d = d.replace('Sep.', '09')
    d = d.replace('Oct.', '10')
    d = d.replace('Nov.', '11')
    d = d.replace('Dec.', '12')
    date2.append(d)

# We first replace all the months in the dates, by numbers
df['date'] = date2

# MAXI_LOCATION_DICO = {}
# MAXI_LOCATION_DICO['Ivry sur Seine'] = (48.813055, 2.38822)
# MAXI_LOCATION_DICO['Tavannes'] = (47.2200764, 7.198525999999999)
# MAXI_LOCATION_DICO['Moutier'] = (47.2782749, 7.371665600000001)
# MAXI_LOCATION_DICO['Hermance'] = (46.3006983, 6.2449688)
# MAXI_LOCATION_DICO['Ferney Voltaire'] = (46.25763200000001, 6.108669)
# MAXI_LOCATION_DICO['Rognes'] = (43.663327, 5.347199)
# MAXI_LOCATION_DICO['Lucerne'] = (47.05016819999999, 8.309307199999999)
# MAXI_LOCATION_DICO['Puidoux'] = (46.4988452, 6.7691772)
# MAXI_LOCATION_DICO['Plan les Ouates'] = (46.1668075, 6.1145793)
# MAXI_LOCATION_DICO['Motiers'] = (46.9111044, 6.6113106)
# MAXI_LOCATION_DICO['Denens'] = (46.51844, 6.45656)
# MAXI_LOCATION_DICO['Cluses'] = (46.06039, 6.580582)
# MAXI_LOCATION_DICO['Oyonnax'] = (46.257773, 5.655335)
# MAXI_LOCATION_DICO['Mendrisio'] = (45.8713339, 8.984132899999999)
# MAXI_LOCATION_DICO['Lugano'] = (46.0036778, 8.951051999999999)
# MAXI_LOCATION_DICO['Bernex'] = (46.1771419, 6.0764849)
# MAXI_LOCATION_DICO['Lucelle'] = (47.421278, 7.246146)
# MAXI_LOCATION_DICO['Thun'] = (46.7579868, 7.6279881)
# MAXI_LOCATION_DICO['Chenes Bougeries'] = (46.1983939, 6.1851258)
# MAXI_LOCATION_DICO['Chene Bourg'] = (46.19735, 6.19731)
# MAXI_LOCATION_DICO['Gunzgen'] = (47.3134764, 7.843830499999999)
# MAXI_LOCATION_DICO['Etziken'] = (47.1876571, 7.6484107)
# MAXI_LOCATION_DICO['Begnins'] = (46.4408426, 6.2477524)
# MAXI_LOCATION_DICO['Lyss'] = (47.0746504, 7.3077022)
# MAXI_LOCATION_DICO['Luzerne (Luzern)'] = (47.05016819999999, 8.309307199999999)
# MAXI_LOCATION_DICO['Lumnezia'] = (46.71766, 9.17366)
# MAXI_LOCATION_DICO['Collonge Bellerive'] = (46.2514024, 6.2022904)
# MAXI_LOCATION_DICO['Saint Sulpice'] = (46.51011399999999, 6.558195100000001)
# MAXI_LOCATION_DICO['Emosson'] = (46.0831928, 6.9141892)
# MAXI_LOCATION_DICO['Pleigne'] = (47.4072829, 7.289801499999998)
# MAXI_LOCATION_DICO['Annecy Le Vieux'] = (45.9192139, 6.141949899999999)
#
# def getCoordinatesForLocation(location):
#     try:
#         return MAXI_LOCATION_DICO[location]
#     except KeyError:
#         coordinates = getGeocodeForLocation(location)
#         MAXI_LOCATION_DICO[location] = coordinates
#         return coordinates
#
# def getGeocodeForLocation(location):
#
#     URL = 'https://maps.google.ch/maps/api/geocode/json?address=' + location + '&key=AIzaSyD-Dzk5qOu2dRSx_wQdJGBdveo_FQujhR0'
#     #AIzaSyBHFQP-QhcaV7CG7o7-FLacHtlE0YI_E1E
#
#     try:
#         req = requests.get(URL)
#     except:
#         print 'Unable to connect to Google Servers'
#         return
#
#     content = json.loads(req.text)
#
#     if content['status'] == 'ZERO_RESULTS':
#         print 'Unable to find coordinates for ' + location
#         return
#     elif content['status'] == "OK":
#         latitude = content['results'][0]['geometry']['location']['lat']
#         longitude = content['results'][0]['geometry']['location']['lng']
#         return (latitude, longitude)
#     else:
#         print 'FATAL: Exiting.'
#         return


OUT_FOLDER_NAME = 'RDF-Data-Per-Day'

grouped_df = df.groupby('date')

for key, item in grouped_df:

    # Open CSV file to write:
    csvfile = open(OUT_FOLDER_NAME+'/'+str(key)+'.csv', 'w')
    fieldnames = ['location', 'event', 'date', 'artist', 'genre']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    nb_events = len(item['date'].values)

    for i in range(nb_events):
        writer.writerow({
            'location': item['location'].values[i],
            'event': item['festival'].values[i],
            'date': item['date'].values[i],
            'artist': item['artist'].values[i],
            'genre': ''
            # 'coordinates': getCoordinatesForLocation(item['location'].values[i])
        })


# Now, some festivals are hosting several artists on the same day, we ought to take care of that:
# We will agreggate all artists playing the same day at the same festival at the same place, in a
# new attribute 'artists' that would represent the 'line-up' of this very place this very day

OUT_FOLDER_NAME_2 = 'RDF-Data-Per-Day-Aggr'

file_list = os.listdir(OUT_FOLDER_NAME)
file_list.remove('.DS_Store')

# Will contain dataframes, one for each day
dfs = []

for csv_file in file_list:
    try:
        df = pd.read_csv(OUT_FOLDER_NAME + '/' + csv_file)
    except:
        pass

    dfs.append(df)



for df in dfs:

    eventGroupedFest = df.groupby(['event', 'location'])

    for key, item in eventGroupedFest:

        festival_name = key[0]
        location = key[1]
        date = item['date'].values[0]
        artists = item['artist'].values
        artists = ', '.join(str(artist) for artist in artists) # str(v) for v in value_list
        artists = '[' + artists
        artists = artists + ']'
        # genre = item['genre'].values[0]
        # coordinates = item['coordinates'].values[0]

        # Open CSV file to write:
        csvfile = open(OUT_FOLDER_NAME_2+'/'+str(date)+'.csv', 'w')
        fieldnames = ['location', 'event', 'date', 'artists', 'genre']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerow({
            'location': location,
            'event': festival_name,
            'date': date,
            'artists': str(artists),
            'genre': ''
            # 'coordinates': coordinates
        })
