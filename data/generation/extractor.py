from util.config import *

from data.generation.snorkel_processing import *
from snorkel.labeling import labeling_function, LabelModel, PandasLFApplier
from data.generation.countrydetector import *
import argparse
from sklearn.model_selection import train_test_split
from tqdm import tqdm

log = logging.getLogger(__name__)

# load the mixed and regions dictionaries
mixed_countries = json.load(open(ROOT_DIR + '/data/input/mixed_countries_regions_dict.json'))
regions = json.load(open(ROOT_DIR + '/data/input/regions_dict.json'))

def getDataFromSource(source, existing_company_numbers, existing_countries, extraction_type):

    """
    For a given data source (MongoDB) get all the countries and companies available

    :param source: MongoDB database
    :param existing_company_numbers: list of companies to append the data from the given source to
    :param existing_countries: list of countries to append the data from the given source to
    :param extraction_type: type of features extraction: full countries/regions/mix

    :return:
        source_company_numbers - list of company numbers from the source concatenated to existing_company_numbers
        countries - list of countries from the given source concatenated to existing_countries
    """
    source_db_connection = MongoDBWrapper(source)

    # Get all countries sorted in ascending order, append it to the existing list and remove duplicates
    source_countries = source_db_connection.db.country.find({}, {'name': 1, '_id': 0}).sort([('name', 1)])

    new_countries = []
    for country in source_countries:

        country_name, country_iso_code = countryDetector(country['name'])

        if extraction_type == 'mixed':
            country_name = mixed_countries[country_iso_code]
        elif extraction_type == 'regions':
            country_name = regions[country_iso_code]

        new_countries.append(country_name)

    source_countries = list(set(new_countries))
    countries = list(set(existing_countries + source_countries))

    # Get all company numbers sorted in ascending order and append it to the existing list
    source_company_numbers = source_db_connection.db.company.find({}, {'company_number': 1, '_id': 0})
    source_company_numbers = existing_company_numbers + [company['company_number'] for company in source_company_numbers]

    return source_company_numbers, countries

"""

    Program to extract the features from different MongoDB databases
    
"""


if __name__ == "__main__":

    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-of", "--output_file", help="output csv file to save the inputs(generation) and label", type=str,
                        default=ROOT_DIR + '/data/input/data.csv')
    parser.add_argument("-tp", "--test_percentage", help="how much of the data to be saved as test", type=float,
                        default=0.05)
    parser.add_argument("-s", "--sources", help="list of data sources", type=str, nargs='+',
                        default=['cs229', 'cs229_troika', 'cs229_uk_blacklist', 'cs229_non_uk_blacklist'])
    parser.add_argument("-t", "--type", help="Type of feature extraction", type=str, choices=['full', 'regions', 'mixed'],
                        default='full')
    args = parser.parse_args()

    company_numbers = []
    countries = []

    for source in args.sources:
        company_numbers, countries = getDataFromSource(source, company_numbers, countries, args.type)

    # Sort the country names alphabetically
    countries.sort()

    # Create the inputs and labels dataframes
    inputs = []
    labels = []

    # Convert the countries to numpy array to ease some work
    countries_array = np.asarray(countries)
    n_countries = np.shape(countries_array)[0]

    log.info(f"Start extracting features for {len(company_numbers)} companies")

    # For each company get the associated officers
    for company_number in tqdm(company_numbers):

        # Extracting the generation
        company_input = np.zeros((2 * n_countries,))
        source_db_connection = db_connection
        if troika_db_connection.findCompany(company_number) is True:
            source_db_connection = troika_db_connection

        company_officer_appointments = source_db_connection.db.officer_appointments.find(
            {'appointed_to.company_number': company_number},
            {'country_of_residence': 1, 'address.country': 1, 'identification': 1, '_id': 0})
        if company_officer_appointments is not None:
            for officer in company_officer_appointments:

                # default the country to UK
                officer_country = "United Kingdom"

                # use first the 'country_of_residence' as country source
                if 'country_of_residence' in officer:
                    officer_country = officer['country_of_residence']
                elif 'address' in officer and 'country' in officer['address']:
                    officer_country = officer['address']['country']

                officer_country, officer_country_iso_code = countryDetector(officer_country)

                if args.type == 'mixed':
                    officer_country = mixed_countries[officer_country_iso_code]
                elif args.type == 'regions':
                    officer_country = regions[officer_country_iso_code]

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

    log.info(f"Finished extracting {len(inputs[0])} features for {len(company_numbers)} companies")

    log.info(f"Start generating labels using snorkel for {len(inputs)} companies")

    # Use snorkel to generate the labels programmatically
    df = pd.DataFrame(inputs, columns=['company_number'] + countries + countries).set_index('company_number', drop=True)

    df = generate_labels_with_snorkel(df)

    # save the generation and labels in two different files for training and test
    df_train, df_test = train_test_split(df, test_size=args.test_percentage)
    df_train.to_csv(args.output_file.replace('.csv', '_train_dev.csv'), index=True, header=True)
    df_test.to_csv(args.output_file.replace('.csv', '_test.csv'), index=True, header=True)

    log.info("Finished extracting generation/labels out of the database")

