#!/usr/bin/env python
# coding=utf-8
# Author: Alexandre Connat ©

import requests
import bs4

def getSwissFestivals():

    SWISS_FESTIVALS = []

    URL = 'http://www.routedesfestivals.com/liste-des-festivals-pour-suisse-3.html'

    req = requests.get(URL)
    txt = req.text.encode('utf-8')

    soup = bs4.BeautifulSoup(txt, 'html5lib')


    for listFest in soup.findAll('li', {'class': 'elemList'}):
        for liTag in listFest.findAll('li'):
            for aTag in liTag.findAll('a', {'class': 'nameList'}):
                SWISS_FESTIVALS.append( aTag.contents[0] )

    return SWISS_FESTIVALS

def cleanMusicFestivals(swissFestivals):

    swissFestivals.remove('LES CREATIVES')
    swissFestivals.remove('MONTREUX COMEDY FESTIVAL')
    swissFestivals.remove('BELLUARD BOLLWERK INTERNATIONAL') # + Music
    swissFestivals.remove('FESTIVAL DE LA BATIE') # + Music
    swissFestivals.remove('POESIE EN ARROSOIR')
    swissFestivals.remove('MORGES SOUS RIRE')
    swissFestivals.remove('BOUGE TA PLANETE')
    swissFestivals.remove('LAUSANNE UNDERGROUND FILM & MUSIC FESTIVAL (LUFF)') # + Music
    swissFestivals.remove('CHAP EN RIRE')
    swissFestivals.remove('FESTIRIRE')
    swissFestivals.remove('FESTIVAL DECOUVRIRE')
    swissFestivals.remove('CULTURESCAPES')
    swissFestivals.remove('ESPLANADE')
    swissFestivals.remove('POLYMANGA') # Rock???

    return swissFestivals


if __name__ == '__main__':

    swissFestivals = getSwissFestivals()
    swissFestivals = cleanMusicFestivals(swissFestivals)

    print 'TROUVÉ:'
    print str(len(swissFestivals)) + ' Festivals !'
