import logging
from logging import handlers

import locale

import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(thread)s %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    handlers=[
                        handlers.RotatingFileHandler("{0}/{1}.log".format('/mnt/data/pycharm-projects/cs229/logs', 'cs229'), maxBytes=(1048576*5), backupCount=10),
                        logging.StreamHandler()
                    ])

MAX_REQ_FOR_KEY=600

API_KEYS = []

with open('/mnt/data/pycharm-projects/cs229/util/keys.txt', 'r') as file:
    for line in file:
        API_KEYS.append((line[:-1], MAX_REQ_FOR_KEY))


TIMEOUT=300 #seconds
BASE_URL="https://api.companieshouse.gov.uk"

MONGO_USERNAME='admin'
MONGO_PASSWORD='admin'
