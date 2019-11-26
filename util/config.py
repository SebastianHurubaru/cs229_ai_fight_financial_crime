import logging
import logging.config

from logging import handlers

import locale

import pandas as pd

logging.config.fileConfig('/mnt/data/pycharm-projects/cs229/util/logging.conf')

MAX_REQ_FOR_KEY=600

API_KEYS = []

with open('/mnt/data/pycharm-projects/cs229/util/keys.txt', 'r') as file:
    for line in file:
        API_KEYS.append((line[:-1], MAX_REQ_FOR_KEY))


TIMEOUT=70 #seconds
BASE_URL="https://api.companieshouse.gov.uk"

MONGO_USERNAME='admin'
MONGO_PASSWORD='admin'
