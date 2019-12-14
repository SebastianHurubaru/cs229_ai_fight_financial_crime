from util.config import *
import argparse

from data.extractor.uk_company_house import UKCompanyHouse

log = logging.getLogger(__name__)


"""
    Program to start data extraction from the UK Companies House 
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="type of extraction: random/troika/uk_blacklist/non_uk_blacklist", type=str, default='troika')
    parser.add_argument("-d", "--depth", help="how deep should we go when searching for troika companies recursively", type=int, default=20)
    parser.add_argument("-if", "--input_file", help="csv input file containing a list of companies",
                        type=str, default= ROOT_DIR + '/data/input/UK_blacklist_companies.csv')
    args = parser.parse_args()

    log.info("Starting {} extraction of UK Company House data".format(args.type))

    if args.type == 'troika':

        company_extractor = UKCompanyHouse(DB_TROIKA)
        # Start from Nordlink LLP which has Cascado AG as officer with a depth of args.depth
        company_extractor.getTroikaCompanyHouseData('OC334012', args.depth)

    elif args.type == 'uk_blacklist':

        company_extractor = UKCompanyHouse(DB_UK_BLACKLIST)
        df = pd.read_csv(args.input_file, header=0, index_col=False)
        for company_name in list(df.iloc[:,0].values):
            # Search for the company and get all it's data with one level of depth
            company_extractor.searchAndGetCompanyHouseData(company_name, args.depth)

    elif args.type == 'non_uk_blacklist':

        company_extractor = UKCompanyHouse(DB_NON_UK_BLACKLIST)
        df = pd.read_csv(args.input_file, header=0, index_col=False, sep=';')
        for officer_name in list(df.iloc[:,0].values):
            # Search for the company and get all it's data with one level of depth
            company_extractor.searchAndGetCompanyHouseDataOfficer(officer_name, args.depth)

    else:

        company_extractor = UKCompanyHouse(DB_MAIN)
        company_extractor.getRandomCompanyHouseData()

