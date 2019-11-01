import logging
import locale

import pandas as pd

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(thread)s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

MAX_REQ_FOR_KEY=600

API_KEYS= [("0K5Fn3TguQ_1OdFoSuzQREVG7aee1OKSYS5Mj5ns", MAX_REQ_FOR_KEY),
           ("CTdeE4B4nqb3vuip2jWQ4oMbajwC8uvlu-tSNLSs", MAX_REQ_FOR_KEY),
           ("QAABDOuTedqG6Y3sS70242hguHxX8lXJ8bWuXjNs", MAX_REQ_FOR_KEY),
           ("ieGbtv4XnrDE7ZsfrXlVatpW8K7z0S_hsdbpd3Wq", MAX_REQ_FOR_KEY)]

TIMEOUT=300 #seconds
BASE_URL="https://api.companieshouse.gov.uk"

MONGO_USERNAME='admin'
MONGO_PASSWORD='admin'
