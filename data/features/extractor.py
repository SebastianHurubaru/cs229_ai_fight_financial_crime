import numpy as np
from util.mongodb import *
from util.config import *
import argparse


def dump_to_csv(values, columns, index_column_name, csv_file):
    df = pd.DataFrame(values, columns=columns).set_index(index_column_name, drop=True)
    df.to_csv(csv_file, index=True, header=True)

if __name__ == "__main__":

    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-ff", "--features_file", help="csv file to save the inputs(features)", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/features.csv')
    parser.add_argument("-lf", "--labels_file", help="csv file to save the labels(outputs)", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/labels.csv')
    parser.add_argument("-t", "--type", help="which files to be produced: features/labels/both", type=str,
                        default='labels')
    parser.add_argument("-tp", "--test_percentage", help="how much of the data to be saved as test", type=float,
                        default='0.05')
    args = parser.parse_args()

    mongodb_connection = MongoDBWrapper('cs229')

    # Get all countries sorted in ascending order
    countries = mongodb_connection.db.country.find({}, {'name': 1, '_id': 0}).sort([('name', 1)])
    countries = [country['name'] for country in countries]

    # Create the inputs and labels dataframes
    inputs = []
    labels = []

    # Convert the countries to numpy array to ease some work
    countries_array = np.asarray(countries)
    n_countries = np.shape(countries_array)[0]

    # Get all company numbers sorted in ascending order
    company_numbers = mongodb_connection.db.company.find({}, {'company_number': 1, '_id': 0})
    company_numbers = [company['company_number'] for company in company_numbers]

    # For each company get the associated officers
    for index, company_number in enumerate(company_numbers):

        if args.type == 'both' or args.type == 'features':

            # Extracting the features
            company_input = np.zeros((2 * n_countries, ))

            company_officer_appointments = mongodb_connection.db.officer_appointments.find({'appointed_to.company_number': company_number}, {'country_of_residence': 1, 'address.country': 1, 'identification': 1, '_id': 0})
            if company_officer_appointments is not None:
                for officer in company_officer_appointments:

                    # default the country to UK
                    officer_country = "United Kingdom"

                    # use first the 'country_of_residence' as country source
                    if 'country_of_residence' in officer:
                        officer_country = officer['country_of_residence']
                    elif 'address' in officer and 'country' in officer['address']:
                        officer_country = officer['address']['country']

                    # are we a corporate officer or a person
                    if 'identification' in officer:
                        # corporations are the 2nd half of the data
                        company_input[np.argwhere(countries_array == officer_country) + n_countries] += 1
                    else:
                        # individuals are the 1st half of the data
                        company_input[np.argwhere(countries_array == officer_country)] += 1
            else:
                pass
                # all values will be 0 if no officers

            inputs.append([company_number] + list(company_input))

        if args.type == 'both' or args.type == 'labels':

            # Extracting the corresponding labels
            company_label = np.zeros(np.shape(countries_array))
            at_least_one_company_psc = False

            company_pscs = mongodb_connection.db.person_with_significant_control.find({'$text': {"$search": company_number}}, {'kind': 1, '_id': 0})
            if company_pscs is not None:
                for psc in company_pscs:
                    if psc['kind'] != 'individual-person-with-significant-control':
                        at_least_one_company_psc = True
                        break

            else:
                pass
                # will default to 0 if no pscs

            labels.append([company_number, int(at_least_one_company_psc)])

        if index % 100 == 0:
            log.info('Processed {} companies'.format(index))

    log.info('Finished processing {} total of companies'.format(index))

    if args.type == 'both' or args.type == 'features':
        n_examples = len(inputs)

        dump_to_csv(inputs[slice(int((1 - args.test_percentage) * n_examples))], ['company_number'] + countries + countries,
                    'company_number', args.features_file.replace('.csv', '_train_dev.csv'))
        dump_to_csv(inputs[slice(int((1 - args.test_percentage) * n_examples), n_examples)], ['company_number'] + countries + countries,
                    'company_number', args.features_file.replace('.csv', '_test.csv'))

    if args.type == 'both' or args.type == 'labels':
        n_examples = len(labels)
        dump_to_csv(labels[slice(int((1 - args.test_percentage) * n_examples))],
                    ['company_number', 'at_least_one_company_psc'], 'company_number',
                    args.labels_file.replace('.csv', '_train_dev.csv'))
        dump_to_csv(labels[slice(int((1 - args.test_percentage) * n_examples), n_examples)],
                    ['company_number', 'at_least_one_company_psc'], 'company_number',
                    args.labels_file.replace('.csv', '_test.csv'))

    log.info("Finished extracting features/labels out of the database")
