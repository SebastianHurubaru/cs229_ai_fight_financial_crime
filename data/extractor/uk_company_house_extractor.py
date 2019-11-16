from util.config import *
from data.extractor.uk_company_house import UKCompanyHouse


log = logging.getLogger('uk_company_house_extractor')

if __name__ == "__main__":

    random_company_extractor = UKCompanyHouse('cs229_test')
    random_company_extractor.getRandomCompanyHouseData()

