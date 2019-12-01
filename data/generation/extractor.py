from util.config import *

from data.generation.snorkel_processing import *
from snorkel.labeling import labeling_function, LabelModel, PandasLFApplier
from data.generation.countrydetector import *
import argparse
from sklearn.model_selection import train_test_split
from tqdm import tqdm

log = logging.getLogger(__name__)

if __name__ == "__main__":

    log = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-of", "--output_file", help="output csv file to save the inputs(generation) and label", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/data.csv')
    parser.add_argument("-tp", "--test_percentage", help="how much of the data to be saved as test", type=float,
                        default='0.05')
    args = parser.parse_args()

    countries = db_connection.db.country.find({}, {'name': 1, '_id': 0}).sort([('name', 1)])
    countries = list(set([countryDetector(country['name']) for country in countries]))

    troika_countries = troika_db_connection.db.country.find({}, {'name': 1, '_id': 0}).sort([('name', 1)])
    troika_countries = list(set([countryDetector(country['name']) for country in troika_countries]))

    countries = list(set(countries + troika_countries))
    countries.sort()

    # Create the inputs and labels dataframes
    inputs = []
    labels = []

    # Convert the countries to numpy array to ease some work
    countries_array = np.asarray(countries)
    n_countries = np.shape(countries_array)[0]

    # Get all company numbers sorted in ascending order
    company_numbers = db_connection.db.company.find({}, {'company_number': 1, '_id': 0})
    troika_company_numbers = troika_db_connection.db.company.find({}, {'company_number': 1, '_id': 0})

    company_numbers = [company['company_number'] for company in company_numbers] + [troika_company['company_number'] for troika_company in troika_company_numbers]

    log.info(f"Start extracting features for {len(company_numbers)} companies")
    pass

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

    # Use snorkel to generate the labels programatically
    df = pd.DataFrame(inputs, columns=['company_number'] + countries + countries).set_index('company_number', drop=True)

    df = generate_labels_with_snorkel(df)

    # save the generation and labels in two different files for training and test
    df_train, df_test = train_test_split(df, test_size=args.test_percentage)
    df_train.to_csv(args.output_file.replace('.csv', '_train_dev.csv'), index=True, header=True)
    df_test.to_csv(args.output_file.replace('.csv', '_test.csv'), index=True, header=True)

    log.info("Finished extracting generation/labels out of the database")

