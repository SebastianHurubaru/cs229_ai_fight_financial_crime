import pandas as pd
import numpy as np
from util.mongodb import *
from util.config import *

if __name__ == "__main__":

    log = logging.getLogger('country_collection')

    mongodb_connection = MongoDBWrapper('cs229')

    # Get all countries sorted in ascending order
    countries = mongodb_connection.db.country.find({}, {'name': 1, '_id': 0}).sort([('name', 1)])
    countries = [country['name'] for country in countries]

    # Create the inputs and labels dataframes
    # input_df = pd.DataFrame([], columns=['company_number'] + countries).set_index('company_number', drop=True)
    inputs = []


    # Convert the countries to numpy array to ease some work
    countries_array = np.asarray(countries)

    # Get all company numbers sorted in ascending order
    company_numbers = mongodb_connection.db.company.find({}, {'company_number': 1, '_id': 0})
    company_numbers = [company['company_number'] for company in company_numbers]

    # For each company get the associated officers
    for index, company_number in enumerate(company_numbers):

        company_input = np.zeros(np.shape(countries))

        company_officer_appointments = mongodb_connection.db.officer_appointments.find({'appointed_to.company_number': company_number})
        if company_officer_appointments is not None:
            for officer in company_officer_appointments:

                # default the country to UK
                officer_country = "United Kingdom"

                # use first the 'country_of_residence' as country source
                if 'country_of_residence' in officer:
                    officer_country = officer['country_of_residence']
                elif 'address' in officer and 'country' in officer['address']:
                    officer_country = officer['address']['country']

                company_input[np.argwhere(countries_array == officer_country)] += 1

        else:
            pass
            # all values will be 0 if no officers


        inputs.append([company_number] + list(company_input))

        if index % 50 == 0:
            log.info('Processed {} companies'.format(index))

    log.info('Finished processing {} total of companies'.format(index))

    input_df = pd.DataFrame(inputs, columns=['company_number'] + countries).set_index('company_number', drop=True)
    input_df.to_csv('../input/features_all.csv', index=True, header=True)

    log.info("Finished extracting features out of the database")