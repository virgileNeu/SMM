#!/usr/bin/env python
# coding=utf-8

##############################################################################
### MERGE ALL 3 DATAFRAMES OF THE 3 MAIN DATA SOURCES (RA, EVENTS.CH, RDF) ###
##############################################################################

import pandas as pd

if __name__ == '__main__':

    RA_DF_NAME = 'ResidentAdvisor/ClubData/RA.csv'
    EVENTS_DF_NAME = 'events.ch/EventsCh.csv'
    RDF_DF_NAME = 'RouteDesFestivals/RDF.csv'

    #ra_df = pd.read_csv(RA_DF_NAME)
    events_df = pd.read_csv(EVENTS_DF_NAME)
    rdf_df = pd.read_csv(RDF_DF_NAME)

    # Add source of origin of the events : [RA, EventsCh, RDF]

    print rdf_df.head(4)
