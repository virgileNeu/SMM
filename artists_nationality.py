#!/usr/bin/env python
# coding=utf-8

import wikipedia
import re
import pycountry
import nltk
from nltk.corpus import stopwords
# nltk.data.path.append('./nltk_data') # In my case, the corpora data are in ~/ (my home Folder /Users/Alexandre)
from nltk.stem.wordnet import WordNetLemmatizer
import string
import pandas as pd

STOP = set(stopwords.words('english'))


def get_pycountry_results(string):

    try: # Country name / code / official_name :
        return pycountry.countries.lookup(string).alpha_2 # Returns the alpha_2 country code ('FR', for France)
    except:
        pass

    try: # Language / language code :
        return pycountry.languages.lookup(string).alpha_2 # Returns the alpha_2 language code ('fr', for French)
    except:
        pass

    try:
        return pycountry.subdivisions.lookup(string).country_code # Returns the code of the parent country ('FR', for Bourgogne)
    except:
        return None

def determine_country(pycountry_results):
    # print pycountry_results
    return max(set(pycountry_results), key=pycountry_results.count)

def get_country_for_sentence(sentence):
    words = re.findall(r'\w+', sentence) # Split in a list of words
    # results = []

    for word in words:
        result = get_pycountry_results(word)
        if result:
            return result
        # if result:
        #     results.append(result)

    # determine_country(results)
    return None

def extract_nationality(artist_name):

    try:
        artist = wikipedia.search(artist_name)[0]
    except IndexError:
        print 'The search yielded no results for ' + artist_name + '...'
        return None

    try:
        page = wikipedia.page(artist)
        description = page.summary
    except wikipedia.exceptions.DisambiguationError as e:
        CHOICE = ''
        for choice in e.options:
            if 'band' in choice:
                CHOICE = choice
            elif 'groupe' in choice:
                CHOICE = choice
            elif 'musician' in choice:
                CHOICE = choice
            elif 'musicien' in choice:
                CHOICE = choice
            elif 'music' in choice:
                CHOICE = choice
            elif 'musique' in choice:
                CHOICE = choice
            elif 'artist' in choice:
                CHOICE = choice
            elif 'singer' in choice:
                CHOICE = choice
            elif 'chant' in choice:
                CHOICE = choice

        if CHOICE != '':
            description = wikipedia.page(CHOICE).summary
        else:
            description = None
            print 'The disambiguation yielded no results for ' + artist_name + '...'
            return None


    stop_free_description = ' '.join([d for d in description.lower().split() if d not in STOP]) # Remove the stopwords
    country = get_country_for_sentence(stop_free_description)

    if not country:
        return None

    if country.lower() == country: # If country is in lowercase, it's a language code
        # print artist_name + ' --> ' + str(pycountry.languages.get(alpha_2=country))
        try:
            return pycountry.languages.get(alpha_2=country).name
        except:
            return country
    else: # It's uppercase
        # print artist_name + ' --> ' + country
        return pycountry.countries.get(alpha_2=country).name

    # TODO: If no results --> Search in French !?


def add_artists_nationality(file_in, file_out):

    # df = pd.read_csv('/Users/Alexandre/Documents/EPFL/SC-MA1/Applied Data Analysis/SMM/ArtistDF_withGenres_ext.csv', encoding='utf-8')
    df = pd.read_csv(file_in)

    #print df['artist'][3].encode('utf-8')
    length = len(df)

    df['nationality'] = ''

    # print 'TOP!'

    for i in range(length):
        if type(df['artist'][i]) != type(0.0):
            artist_name = df['artist'][i].encode('utf-8')
            df['nationality'][i] = extract_nationality(artist_name)
        else:
            df['nationality'][i] = None

    # print df.head(10)
    # print 'TOP!'

    df.to_csv(file_out)


if __name__ == '__main__':

    file_in_name = '/Users/Alexandre/Documents/EPFL/SC-MA1/Applied Data Analysis/SMM/ArtistDF_withGenres_ext.csv'
    file_out_name = '/Users/Alexandre/Documents/EPFL/SC-MA1/Applied Data Analysis/SMM/ArtistDF_withGenres_AndNationalities.csv'

    add_artists_nationality(file_in_name, file_out_name)

    # NAMES = ['Daft Punk', 'Santana', 'Lady Bazar', 'Led Zepelin', 'Sting', 'U2', 'Manu Chao', 'The Prodigy', 'Bruno Mars']
