import requests
import json
import time

from util.config import *

log = logging.getLogger('rest')

class RESTClient:

    def __init__(self, api_keys, timeout, base_url):
        self.api_keys = api_keys
        self.timeout = timeout
        self.base_url = base_url

        self.number_of_max_req = 0
        self.key_idx = 0

        self.timeout = timeout

        self.req_timeout = None

        self.session = requests.Session()
        self.session.auth = (self.api_keys[self.key_idx][0], '')

    def doTimeout(self):
        self.resetSession()
        time.sleep(self.timeout)


    def resetSession(self):
        self.session.close()
        self.session = requests.Session()
        self.getNextApiKey()


    def getNextApiKey(self):

        if self.key_idx == len(self.api_keys):
            self.key_idx = 0

        self.session.auth = (self.api_keys[self.key_idx][0], '')
        self.number_of_max_req = self.api_keys[self.key_idx][1]

        self.key_idx += 1


    def doRequest(self, partial_url, params):

        self.number_of_max_req -= 1

        if self.number_of_max_req <= 0:
            self.getNextApiKey()

        url = self.base_url + partial_url

        try:
            response = self.session.get(url, params=params, timeout=self.req_timeout)
            if not (response.status_code == 200 or response.status_code == 404):
                self.doTimeout()
                response = self.session.get(url, params=params, timeout=self.req_timeout)
        except:
            self.doTimeout()
            response = self.session.get(url, params=params, timeout=self.req_timeout)

        try:
            responseJson = response.json()

        except Exception as e:
            log.error('Parsing the following response to Json failed: {}'.format(response))
            log.error('Exception occurred: {}'.format(e))

        log.debug(responseJson)

        # record could not be found/does not exist
        if response.status_code == 404:
            responseJson = None

        return responseJson
