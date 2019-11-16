from util.config import *
from data.extractor.RESTClient import *
from util.mongodb import *
from itertools import permutations
import json
import random

log = logging.getLogger('company_house')

restClient = RESTClient(API_KEYS, TIMEOUT, BASE_URL)

MAX_COMPANY_NUMBERS = 300000

mongodb_connection = MongoDBWrapper('cs229_test')

def generateCompanyNumbers():

    englandAndWales = [''.join(tuples) for tuples in list(permutations('0123456789', 8))]
    englandAndWalesLlps = ['OC' + ''.join(gen_number) for gen_number in list(permutations('0123456789', 6))]

    company_list = englandAndWales + englandAndWalesLlps
    random.shuffle(company_list)

    return company_list

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


def getCompanyHouseData():

    processedCompanyItems = 0

    company_numbers = generateCompanyNumbers()

    for company_number in company_numbers:

        if processedCompanyItems > MAX_COMPANY_NUMBERS:
            log.info("Reached maximum defined number of companies {}".format(MAX_COMPANY_NUMBERS))
            break;

        # skip if company already in our database
        if mongodb_connection.companyDoesNotExist(company_number) == True or mongodb_connection.findCompany(company_number) == True:
            continue

        # process company profile
        company_profile = getCompanyProfile(company_number)
        if company_profile is None:
            mongodb_connection.insertNotExistingCompany(company_number)
            continue

        log.info("Processing company {}".format(company_number))

        # process company's officers
        company_officers = getCompanyOfficers(company_number)
        if company_officers is not None:
            mongodb_connection.insertCompanyOfficers(company_profile, company_officers.get("items", []))

            # process officer appointments
            for officer in company_officers.get("items", []):
                officer_appointments = getOfficerAppointments(officer["links"]["officer"]["appointments"])
                if officer_appointments is not None:
                    mongodb_connection.insertOfficerAppointments(officer["links"]["officer"]["appointments"], officer_appointments.get("items", []))

        # process company's persons with significant control
        company_pscs = getCompanyPersonsWithSignificantControl(company_number)
        if company_pscs is not None:
            mongodb_connection.insertCompanyPersonsWithSignificantControl(company_profile, company_pscs.get("items", []))

        # save company at the end
        mongodb_connection.insertCompany(company_profile)
        processedCompanyItems += 1

        log.debug('Processed so far {} companies!'.format(processedCompanyItems))

        if processedCompanyItems % 100 == 0:
            log.info('Processed so far {} companies!'.format(processedCompanyItems))


    log.info('Finished processing {} companies!'.format(processedCompanyItems))

# get the data
getCompanyHouseData()


