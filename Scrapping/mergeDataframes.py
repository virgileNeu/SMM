#!/usr/bin/env python
# coding=utf-8

##############################################################################
### MERGE ALL 3 DATAFRAMES OF THE 3 MAIN DATA SOURCES (RA, EVENTS.CH, RDF) ###
##############################################################################

import pandas as pd

RA_DF_NAME = 'ResidentAdvisor/ClubData/RA.csv'
EVENTS_DF_NAME = 'events.ch/EventsCh.csv'
RDF_DF_NAME = 'RouteDesFestivals/RDF.csv'

ra_df = pd.read_csv(RA_DF_NAME)
events_df = pd.read_csv(EVENTS_DF_NAME)
rdf_df = pd.read_csv(RDF_DF_NAME)

# Add source of origin of the events :
ra_df['src'] = 'RA'
events_df['src'] = 'EventsCh'
rdf_df['src'] = 'RDF'


half_df = events_df.merge(rdf_df, how='outer')
full_df = half_df.merge(ra_df, how='outer')

full_df['coordinates'] = None

####### To remove after testing #######
sample_df = full_df[full_df.index % 100 == 0]
#######################################

import Pipepline
sample_df_with_coordinates, addressDico, localityDico, coordinatesDico = Pipepline.completeGeographicData(sample_df)
sample_df_with_coordinates.to_csv('sampleDF.csv', encoding='utf-8')
