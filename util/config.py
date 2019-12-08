import logging
import logging.config

from logging import handlers

import locale

import pandas as pd

ROOT_DIR = '/mnt/data/pycharm-projects/cs229'

logging.log_file = ROOT_DIR + '/logs/cs229.log'
logging.config.fileConfig(ROOT_DIR + '/util/logging.conf')

MAX_REQ_FOR_KEY=600

API_KEYS = []

with open(ROOT_DIR + '/util/keys.txt', 'r') as file:
    for line in file:
        API_KEYS.append((line[:-1], MAX_REQ_FOR_KEY))


TIMEOUT=70 #seconds
BASE_URL="https://api.companieshouse.gov.uk"

MONGO_USERNAME='admin'
MONGO_PASSWORD='admin'

DB_MAIN='cs229'
DB_TROIKA='cs229_troika'
DB_UK_BLACKLIST='cs229_uk_blacklist'
DB_NON_UK_BLACKLIST='cs229_non_uk_blacklist'
