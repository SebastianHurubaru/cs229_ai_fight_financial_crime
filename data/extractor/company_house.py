from util.config import *
from data.extractor.RESTClient import *
from util.mongodb import *

import json

log = logging.getLogger('company_house')

search_criterias = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
max_records = 10000
page_size = 100

restClient = RESTClient(API_KEYS, TIMEOUT, BASE_URL)

def getCompanyProfile(company_number):

    response = restClient.doRequest('/company/' + company_number, None)
    return response

def getCompanyPersonsWithSignificantControl(company_number):

    response = restClient.doRequest('/company/' + company_number + '/persons-with-significant-control', None)
    return response

def getCompanyOfficers(company_number):

    response = restClient.doRequest('/company/' + company_number + '/officers', None)
    return response

def getOfficerAppointments(appointment_link):

    response = restClient.doRequest(appointment_link, None)
    return response


def searchCompanies(search_string):

    company_numbers = []

    for page_index in range(int(max_records/page_size)):

        params = {'q': search_string, 'items_per_page': page_size, 'start_index': page_index*page_size}

        response = restClient.doRequest('/search/companies', params)

        for company in response["items"]:
            company_numbers.append(company["company_number"])

    return company_numbers


def getCompanyHouseData():

    processedCompanyItems = 0
    for search_criteria in search_criterias:

        company_numbers = searchCompanies(search_criteria)
        for company_number in company_numbers:

            # skip if company already in our database
            if findCompany(company_number) == True:
                continue

            # process company profile
            company_profile = getCompanyProfile(company_number)
            insertCompany(company_profile)

            # process company's officers
            company_officers = getCompanyOfficers(company_number)
            insertCompanyOfficers(company_profile, company_officers.get("items", []))

            # process officer appointments
            for officer in company_officers.get("items", []):
                officer_appointments = getOfficerAppointments(officer["links"]["officer"]["appointments"])
                insertOfficerAppointments(officer["links"]["officer"]["appointments"], officer_appointments.get("items", []))

            # process company's persons with significant control
            company_pscs = getCompanyPersonsWithSignificantControl(company_number)
            insertCompanyPersonsWithSignificantControl(company_profile, company_pscs.get("items", []))

            processedCompanyItems += 1

            log.debug('Processed so far {} companies!'.format(processedCompanyItems))

            if processedCompanyItems % 100 == 0:
                log.info('Processed so far {} companies!'.format(processedCompanyItems))


    log.info('Finished processing {} companies!'.format(processedCompanyItems))

# get the data
getCompanyHouseData()