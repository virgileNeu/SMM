#!/usr/bin/env python
# coding=utf-8
# Author: Alexandre Connat ©

############################################################
######### CREATE A LIST OF SWISS MUSIC FESTIVALS ###########
############################################################

############################################################
########### DO PLENTY OF OTHER STUFF AS WELL ! #############
############################################################

import requests
import bs4
import re
import csv


# LOOKUP_TABLE_MONTHS = {
#     u'Juin\xa016': '06',
#     u'Juin\xa015': '06',
#     u'Juin\xa014': '06',
#     u'Juin\xa013': '06',
#     u'Juin\xa012': '06',
#     u'Juin\xa011': '06',
#     u'Juil.\xa016': '07',
#     u'Juil.\xa015': '07',
#     u'Juil.\xa014': '07',
#     u'Juil.\xa013': '07',
#     u'Juil.\xa012': '07',
#     u'Juil.\xa011': '07',
# }




def getSwissFestivals():

    SWISS_FESTIVALS = []

    URL = 'http://www.routedesfestivals.com/liste-des-festivals-pour-suisse-3.html'

    req = requests.get(URL)
    txt = req.text.encode('utf-8')

    soup = bs4.BeautifulSoup(txt, 'html5lib')

    for listFest in soup.findAll('li', {'class': 'elemList'}):
        for liTag in listFest.findAll('li'):
            for aTag in liTag.findAll('a', {'class': 'nameList'}):
                name = aTag.contents[0].encode('utf-8')
                link = aTag['href'].encode('utf-8')
                ID = re.findall('-(\d*).html', link)[0].encode('utf-8')
                festival = {}
                festival['name'] = name
                festival['link'] = link
                festival['ID'] = ID
                SWISS_FESTIVALS.append(festival)

    return SWISS_FESTIVALS


def cleanMusicFestivals(swissFestivals):

    NON_MUSIC_FESTIVAL = ['LES CREATIVES', 'MONTREUX COMEDY FESTIVAL', '1066',
                          'POESIE EN ARROSOIR', 'CHAP EN RIRE', 'FESTIRIRE',
                          'FESTIVAL DECOUVRIRE', 'MORGES SOUS RIRE']

    for f in swissFestivals:
        if f['name'] in NON_MUSIC_FESTIVAL:
            swissFestivals.remove(f)

    # swissFestivals.remove('LES CREATIVES')
    # swissFestivals.remove('MONTREUX COMEDY FESTIVAL')
    # swissFestivals.remove('BELLUARD BOLLWERK INTERNATIONAL') # + Music
    # swissFestivals.remove('FESTIVAL DE LA BATIE') # + Music
    # swissFestivals.remove('POESIE EN ARROSOIR')
    # swissFestivals.remove('MORGES SOUS RIRE')
    # swissFestivals.remove('BOUGE TA PLANETE')
    # swissFestivals.remove('LAUSANNE UNDERGROUND FILM & MUSIC FESTIVAL (LUFF)') # + Music
    # swissFestivals.remove('CHAP EN RIRE')
    # swissFestivals.remove('FESTIRIRE')
    # swissFestivals.remove('FESTIVAL DECOUVRIRE')
    # swissFestivals.remove('CULTURESCAPES')
    # swissFestivals.remove('ESPLANADE')
    # swissFestivals.remove('POLYMANGA') # Rock???

    # ATTENTION : Au Bord de L'eau SIERRE

    return swissFestivals


def getArchiveDatesForFestival(festival):

    BASE_URL = 'http://www.routedesfestivals.com/'
    URL = BASE_URL + festival

    req = requests.get(URL)
    txt = req.text.encode('utf-8')
    soup = bs4.BeautifulSoup(txt, 'html5lib')

    archiveDates = []

    for selectTag in soup.findAll('select', {'id': 'archive'}):
        for optionTag in selectTag.findAll('option'):
            year = optionTag.contents[0].encode('utf-8')
            archiveDates.append(year)

    return archiveDates


def getConcertsForFestivalAtDate(festivalId, year):

    BASE_URL = 'http://www.routedesfestivals.com/ajax/archives.php'
    params = {
        'id': festivalId,
        'year': year,
    }
    req = requests.get(BASE_URL, params=params)
    txt = req.text.encode('utf-8')
    soup = bs4.BeautifulSoup(txt, 'html5lib')

    events = []

    for ulTag in soup.findAll('ul', {'class': 'liste_concerts'}):
        for liTag in ulTag.findAll('li'):
            try:
                day = liTag.find('b', {'class': 'jour'}).contents[0]
                month = liTag.find('b', {'class': 'mois'}).contents[0]
                month = month.split(u'\xa0')[0]
                # month = LOOKUP_TABLE_MONTHS[month]
                # hour = liTag.find('b', {'class': 'heure'}).contents[0]
                artist = liTag.find('a', {'class': 'artiste'}).contents[0]
                place = liTag.findAll('a', {'class': 'lieu'})[1].contents[0]
                event = {}
                event['date'] = '%s-%s-%s' % (year, month, day)
                # event['hour'] = hour
                event['artist'] = artist
                event['place'] = place
                events.append(event)
            except:
                print '*** ERROR *** while parsing festival ' + str(festivalId) + ' ('+str(year)+')'
                print '** AT LINE **' + str(liTag.prettify().encode('utf-8'))

    return events




if __name__ == '__main__':

    swissFestivals = getSwissFestivals()
    cleanMusicFestivals(swissFestivals)

    for f in swissFestivals:
        f['name'] = f['name'].replace('/', '-')
        print f['name'] + ' : '
        f['archive_dates'] = getArchiveDatesForFestival(f['link'])

        FOLDER_NAME = 'RouteDesFestivalsData'
        # Open CSV file to write:
        csvfile = open(FOLDER_NAME+'/'+f['name']+'.csv', 'w')
        fieldnames = ['festival', 'location', 'date', 'artist']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for year in f['archive_dates']:
            print '-- ' + year + ':'
            for concert in getConcertsForFestivalAtDate(festivalId=f['ID'], year=year):
                print ('---- festival=%s, location=%s, date=%s, artist=%s' % (f['name'], concert['place'], concert['date'], concert['artist'])).encode('utf-8')
                writer.writerow({'festival': f['name'].encode('utf-8'), 'location': concert['place'].encode('utf-8'), 'date': concert['date'].encode('utf-8'), 'artist': concert['artist'].encode('utf-8')})
            print '--------'

        print '--------'
