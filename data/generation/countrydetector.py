#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 22:26:02 2019

@author: francoischesnay
"""

from util.config import *
import numpy as np
import collections
import json

log = logging.getLogger(__name__)

def countryDetector(unidentifiedCountryName):
    """ check the name and convert it in normalized name of country"""
        
    def initializeCountryConverter():
        """Initlize the global variables required for the conversion"""
        
        global officialCountriesDict
        global invertedofficialCountriesDict
        global countryName2ISOCodeDict
        global signatureOfficialCountriesDict
        global AdditionalCountryNameDict
        global signatureNameCountryNameDict
        
        countryName2ISOCodeDict = dict()
        signatureOfficialCountriesDict = dict()
        signatureNameCountryNameDict = dict()
        
        officialCountriesDict = json.load(open((ROOT_DIR + '/data/input/official_countries_dict.json')))
    
    
        invertedofficialCountriesDict=dict()
        
        for k, v in officialCountriesDict.items():
            invertedofficialCountriesDict[v]=k
    
        # create an inverse dictionnary from the names used for a country to the unique country code
        countryName2ISOCodeDict = dict()
        signatureOfficialCountriesDict = dict()
        signatureNameCountryNameDict = dict()

        # create a dictionary taking a chain of characters] and creating it signature 
        # the dictionary is based on invertedofficialCountriesDict
        for k, v in officialCountriesDict.items():
            countryName2ISOCodeDict[v]=k
            signatureOfficialCountriesDict[v] = computeVectorOfNumberOfLetters(v)
    
        # Adding extra county name commonly used in our database 
        # from possible county name : ISO name
        AdditionalCountryNameDict = json.load(open(ROOT_DIR + '/data/input/additional_country_name_dict.json'))

        for k, v in countryName2ISOCodeDict.items():
            signatureNameCountryNameDict[k] = computeVectorOfNumberOfLetters(k)


        for k, v in AdditionalCountryNameDict.items():
            signatureNameCountryNameDict[k] = computeVectorOfNumberOfLetters(k)


    # Helper functions

    def computeVectorOfNumberOfLetters(word):
        # transform word in lower case
        word=word.lower()
        # create a numpy array vector initialized at zero to count the letter of
        # the word
        countLetters=np.zeros(26)
         # create a string representing the alphabet in lower case
        alphabet =  ''.join(['%c' % x for x in range(97, 97+26)])
        # count the letters and save into a numpy array of size 26
        for i in range(len(alphabet)):
            #print(alphabet[i])
            countLetters[i] = word.count(alphabet[i])
        return countLetters


    def computeCost(vectorLettersA, vectorLettersB):
        """Compute cost between two vectors using squared Euclidian distance"""
        # takes two vectors of size 26 as input
        # return the euclidian distance between the two vectors
        return np.sum((vectorLettersA - vectorLettersB)**2)


    def findClosetCountryNames(unidentifiedCountryName, signatureOfficialCountriesDict, numberTopN=2):
            orderedSignatureOfficialCountriesDict = \
                collections.OrderedDict(sorted(signatureOfficialCountriesDict.items(), key=lambda t: t[0]))
            cost = []
            # create unordered list to store the results
            OfficialCountries2CostDict = dict()
            OfficialCountries2NegativeCostDict = dict()
            #
            signatureUnidentifiedCountryName = computeVectorOfNumberOfLetters(unidentifiedCountryName)

            for k, v in orderedSignatureOfficialCountriesDict.items():
                cost.append(computeCost(signatureUnidentifiedCountryName, v))
                OfficialCountries2CostDict[k] = computeCost(signatureUnidentifiedCountryName, v)
                OfficialCountries2NegativeCostDict[k] = -computeCost(signatureUnidentifiedCountryName, v)

            return collections.Counter(OfficialCountries2NegativeCostDict).most_common(numberTopN)

    # Check whether initialization is required
    try:
        if officialCountriesDict["AF"] == "Afghanistan":
            pass
    except:
        initializeCountryConverter()

    # Compute the closest country
    closest = findClosetCountryNames(unidentifiedCountryName, signatureNameCountryNameDict, numberTopN=1)
    try:
        closestToPrint = officialCountriesDict[countryName2ISOCodeDict[closest[0][0]]]
    except:
        closestToPrint = officialCountriesDict[AdditionalCountryNameDict[closest[0][0]]]

    # Return name of the closest country
    return closestToPrint
