from unittest import TestCase
from util.mongodb import *
from data.generation.countrydetector import *

class TestCountryDetector(TestCase):

    def test_allAvailableCountries_(self):

        mongodb_connection = MongoDBWrapper('cs229')

        testCountries = mongodb_connection.db.country.find({}, {'name': 1, '_id': 0}).sort([('name', 1)])

        convertedCountries = []
        unknownCountries = 0

        for testCountry in testCountries:
            convertedCountry = countryDetector(testCountry['name'])
            if convertedCountry == 'Unknown':
                unknownCountries += 1
            print(f"{testCountry} => {convertedCountry}")
            convertedCountries.append(convertedCountry)

        assert unknownCountries == 42, "Unknown country numbers has changed. Check!"

