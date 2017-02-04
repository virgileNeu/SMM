from ResidentAdvisor_scrapping import mergeClubData
import pandas as pd

encoding = "utf-8"
filename = "ClubData\RA.csv"

ClubDataFrame = mergeClubData(encoding)
ClubDataFrame = ClubDataFrame[['ClubName','Address','EventName','Date','LineUp']]
ClubDataFrame.columns=['place','address','event','date','artists']
ClubDataFrame.to_csv(filename,encoding = encoding)