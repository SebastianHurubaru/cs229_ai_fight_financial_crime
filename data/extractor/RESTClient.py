import requests
import json
import time

from util.config import *

log = logging.getLogger(__name__)


class RESTClient:
    """
    Simple implementation of a REST Client

    """

    def __init__(self, api_keys, timeout, base_url):

        """
            Class initializer

            Args:
                  api_keys -- list of API keys to be used
                  timeout -- how much to timeout after an access related error
                  base_url -- base URL from which to start all the requests
        """

        self.api_keys = api_keys
        self.timeout = timeout
        self.base_url = base_url

        self.number_of_max_req = 0
        self.key_idx = 0

        self.calls_to_timeout = 0

        self.timeout = timeout

        self.req_timeout = 60

        self.session = requests.Session()
        self.session.auth = (self.api_keys[self.key_idx][0], '')

    def doTimeout(self):

        """
            Perform timeout. Resets the info counter of API calls done since the last timeout,
             as well as the session

        """

        log.info('Executed {} calls until timeout'.format(self.calls_to_timeout))
        self.calls_to_timeout = 0

        self.resetSession()
        time.sleep(self.timeout)


    def resetSession(self, get_new_api_key=True):

        """
            Resets the session

            Args:
                  get_new_api_key -- whether to use a new API Key
        """
        self.session.close()
        self.session = requests.Session()

        if get_new_api_key == True:
            self.getNextApiKey()


    def getNextApiKey(self):

        """
            Gets a new API key, configured with it's correspondent access rights.
            If all keys are already used, start from the first one.

        """

        self.resetSession(get_new_api_key=False)

        if self.key_idx == len(self.api_keys):
            self.key_idx = 0

        self.session.auth = (self.api_keys[self.key_idx][0], '')
        self.number_of_max_req = self.api_keys[self.key_idx][1]

        self.key_idx += 1


    def doRequest(self, partial_url, params):

        """
            Make the HTTP request.
            If UK Company House service restricted access to the host, do a timeout and continue.

            Args:
                  partial_url -- the URL used together with the base one to form the full request URL
                  params -- map of HTTP request parameters

            Returns:
                responseJson -- the HTTP response in Json format

        """

        self.calls_to_timeout += 1

        self.number_of_max_req -= 1

        if self.number_of_max_req <= 0:
            self.getNextApiKey()

        url = self.base_url + partial_url

        while True:

            try:
                response = self.session.get(url, params=params, timeout=self.req_timeout)
                if not (response.status_code == 200 or response.status_code == 404):
                    log.info(
                        'response.status_code {} received. For current key having still {} requests to do. Sleeping {} seconds ...'.format(
                            response.status_code, self.number_of_max_req, TIMEOUT))
                    self.doTimeout()
                    continue

            except Exception as e:
                log.info('Exception occurred: {}'.format(e))
                log.info('For current key having still {} requests to do. Sleeping {} seconds ...'.format(
                    self.number_of_max_req, TIMEOUT))
                self.doTimeout()
                continue

            break

        try:
            responseJson = response.json()
            log.debug(responseJson)

            # record could not be found/does not exist
            if response.status_code == 404:
                responseJson = None

            return responseJson

        except Exception as e:
            log.error('Parsing the following response to Json failed: {}'.format(response))
            log.error('Exception occurred: {}'.format(e))
            return None

