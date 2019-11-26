from util.config import *
import argparse

from data.extractor.uk_company_house import UKCompanyHouse

log = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="type of extraction: random/troika", type=str, default='troika')
    parser.add_argument("-d", "--depth", help="how deeo should we go when searching for troika companies recursively", type=int, default=20)
    args = parser.parse_args()

    log.info("Starting {} extraction of UK Company House data".format(args.type))

    if args.type is 'troika':

        company_extractor = UKCompanyHouse('cs229_troika')
        # Start from Nordlink LLP which has Cascado AG as officer with a depth of args.depth
        company_extractor.getTroikaCompanyHouseData('OC334012', args.depth)

    else:

        company_extractor = UKCompanyHouse('cs229_test')
        company_extractor.getRandomCompanyHouseData()

