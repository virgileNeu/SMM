# Events.ch website handler

# Files
## EventsCh.csv:
Contains all the data in a single csv file before the merge with the other data.

## events_utils.py:
Contains all function used in run.py

## run.py:
Script that scrap and aggregate the data. Needs to be given the start date in the YYYY-MM-DD form, the file name of the aggregated data file. Can also receive optionally a end date to scrap between two dates, and a max web page to limit the number of page explored per day.

# Folders
### EventsChData:
Contains all the extracted data from the website in the form YYYY-MM-DD.csv.

### .old_scripts_not_used:
Contains old script originaly used, not documented.

### .old_visualisation:
Contains a small visualisation using mathplotlib and basemap. Then we found Tableau
