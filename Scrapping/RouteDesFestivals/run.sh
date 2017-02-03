#!/bin/bash
python scrapRouteDesFestivals.py
echo '[Done] Scrapping'
python separateFestivalsPerDay.py
echo '[Done] Splitting by day'
python createBigGeneralDataframe.py
echo '[Done] Creating general dataframe'
