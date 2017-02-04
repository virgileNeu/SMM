# Events.ch website handler

# Files
## EventsCh.csv:
Contains all the data in a single csv file before the merge with the other data.

## events_utils.py:
Contains all function used in run.py

## run.py:
Script that scrap and aggregate the data. Usage described with -h option :

* a <filename>: aggregate all the extracted data to the file <filename>
* -e <date>: extract data on the website for the given date date.
* -s <start_date> <end_date>: scrap data on the website between start_date and end_date.
* -m <max_pages> : define the maximum amount of subpages scrap per date
* -h: display this help.

# Folders
### EventsChData:
Contains all the extracted data from the website in the form YYYY-MM-DD.csv.

### .old_scripts_not_used:
Contains old script originaly used, not documented.

### .old_visualisation:
Contains a small visualisation using mathplotlib and basemap. Then we found Tableau
