from util.mongodb import *

log = logging.getLogger(__name__)

mongodb_connection = MongoDBWrapper('cs229')

log.info("Start creating the db.country collection")

# Extract both country_of_residence and address.country fields
countries_of_residence = mongodb_connection.db.officer_appointments.distinct("country_of_residence")
address_countries = mongodb_connection.db.officer_appointments.distinct("address.country")

# Join both lists and keep only the unique values
countries = countries_of_residence
countries.extend(address_country for address_country in address_countries if address_country not in countries_of_residence)

# Create a document with just the name field out of the country names
countries = [{'name': country} for country in countries]

# Create db.country collection
try:
    mongodb_connection.db.country.insert_many(countries)

except Exception as e:
    log.error('Exception occurred: {}'.format(e))
    exit(-1)

log.info("Successfully created the db.country collection")