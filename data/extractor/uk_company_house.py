from util.config import *
from data.extractor.RESTClient import *
from util.mongodb import *
from itertools import permutations
import random

log = logging.getLogger('uk_company_house')

class UKCompanyHouse:

    def __init__(self, db_name, max_company_numbers=300000):

        self.restClient = RESTClient(API_KEYS, TIMEOUT, BASE_URL)
        self.max_company_numbers = max_company_numbers
        self.mongodb_connection = MongoDBWrapper(db_name)


    def generateCompanyNumbers(self, ):

        englandAndWales = [''.join(tuples) for tuples in list(permutations('0123456789', 8))]
        englandAndWalesLlps = ['OC' + ''.join(gen_number) for gen_number in list(permutations('0123456789', 6))]

        company_list = englandAndWales + englandAndWalesLlps
        random.shuffle(company_list)

        return company_list

    def getCompanyProfile(self, company_number):

        response = self.restClient.doRequest('/company/' + company_number, None)
        return response

    def getCompanyPersonsWithSignificantControl(self, company_number):

        response = self.restClient.doRequest('/company/' + company_number + '/persons-with-significant-control', None)
        return response

    def getCompanyOfficers(self, company_number):

        response = self.restClient.doRequest('/company/' + company_number + '/officers', None)
        return response

    def getOfficerAppointments(self, appointment_link):

        response = self.restClient.doRequest(appointment_link, None)
        return response


    def processCompany(self, company_number):

        # process company profile
        company_profile = self.getCompanyProfile(company_number)
        if company_profile is None:
            self.mongodb_connection.insertNotExistingCompany(company_number)
            return False

        log.info("Processing company {}".format(company_number))

        # process company's officers
        company_officers = self.getCompanyOfficers(company_number)
        if company_officers is not None:
            self.mongodb_connection.insertCompanyOfficers(company_profile, company_officers.get("items", []))

            # process officer appointments
            for officer in company_officers.get("items", []):
                officer_appointments = self.getOfficerAppointments(officer["links"]["officer"]["appointments"])
                if officer_appointments is not None:
                    self.mongodb_connection.insertOfficerAppointments(officer["links"]["officer"]["appointments"],
                                                                      officer_appointments.get("items", []))

        # process company's persons with significant control
        company_pscs = self.getCompanyPersonsWithSignificantControl(company_number)
        if company_pscs is not None:
            self.mongodb_connection.insertCompanyPersonsWithSignificantControl(company_profile,
                                                                               company_pscs.get("items", []))

        # save company at the end
        self.mongodb_connection.insertCompany(company_profile)

        return True

    def getRandomCompanyHouseData(self):

        processedCompanyItems = 0

        company_numbers = self.generateCompanyNumbers()

        for company_number in company_numbers:

            if processedCompanyItems > self.max_company_numbers:
                log.info("Reached maximum defined number of companies {}".format(self.max_company_numbers))
                break;

            # skip if company already in our database
            if self.mongodb_connection.companyDoesNotExist(company_number) == True or self.mongodb_connection.findCompany(company_number) == True:
                continue

            # process company profile
            if self.processCompany(company_number) == False:
                continue

            processedCompanyItems += 1

            log.debug('Processed so far {} companies!'.format(processedCompanyItems))

            if processedCompanyItems % 100 == 0:
                log.info('Processed so far {} companies!'.format(processedCompanyItems))

        log.info('Finished processing {} companies!'.format(processedCompanyItems))


    def getTroikaCompany(self, company_number, depth):

        if depth is 0: return

        # save company data if not already processed
        if self.mongodb_connection.findCompany(company_number) is False:
            self.processCompany(company_number)

        # process company's officers
        company_officers = self.getCompanyOfficers(company_number)
        if company_officers is not None:
            for officer in company_officers.get("items", []):
                self.getTroikaOfficers(officer, depth - 1)

    def getTroikaOfficers(self, officer, depth):

        if depth is 0: return

        # get officer appointments
        officer_appointments = self.getOfficerAppointments(officer["links"]["officer"]["appointments"])

        if officer_appointments is not None:
            for appointment in officer_appointments.get("items", []):
                self.getTroikaCompany(appointment['appointed_to']['company_number'], depth)

    def getTroikaCompanyHouseData(self, start_company_number, depth):

        self.getTroikaCompany(start_company_number, depth)

