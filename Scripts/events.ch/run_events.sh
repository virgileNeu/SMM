#!/bin/bash

#Collect data from last month to now and regenerate the csv with coordinates
year=$(date +'%Y')
month=$(date +'%m')
day=$(date +'%d')

if [ $month -eq 1 ]; then
    let month=12
    let year-=1
fi
last_month_date=$year'-'$month'-'$day
echo $last_month_date
python3 EventsChDataExtractor.py $last_month_date

python3 aggregate EventsChData EventsCh.csv

python3 expandEventsScript.py EventsCh.csv completeWithCoordinates.csv

