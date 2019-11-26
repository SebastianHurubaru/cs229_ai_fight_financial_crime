from util.config import *
from pymongo import MongoClient
import urllib.parse

log = logging.getLogger(__name__)

class MongoDBWrapper:
    
    def __init__(self, db_name):

        self.username = urllib.parse.quote_plus(MONGO_USERNAME)
        self.password = urllib.parse.quote_plus(MONGO_PASSWORD)

        client = MongoClient('mongodb://%s:%s@127.0.0.1' % (self.username, self.password))

        self.db = client[db_name]


    def findCompany(self, company_number):
    
        found = False
    
        try:
    
            if self.db.company.find_one({'company_number': company_number}) != None:
                found = True
    
        except Exception as e:
    
            log.error('Looking for company {} has failed. Please check the reason below!'.format(company_number))
            log.error('Exception occurred: {}'.format(e))
    
    
        return found
    
    
    def companyDoesNotExist(self, company_number):
    
        found = False
    
        try:
    
            if self.db.company_not_existing.find_one({'company_number': company_number}) != None:
                found = True
    
        except Exception as e:
    
            log.error('Looking for company {} has failed. Please check the reason below!'.format(company_number))
            log.error('Exception occurred: {}'.format(e))
    
    
        return found
    
    
    
    def insertCompany(self, company):
    
        try:
    
            company_id = self.db.company.insert_one(company).inserted_id
            return company_id
    
        except Exception as e:
    
            log.error('Insert of company {} has failed! Please check the reason below!'.format(company["company_number"]))
            log.error('Exception occurred: {}'.format(e))
    
    
    def insertNotExistingCompany(self, company_number):
    
        try:
    
            company_id = self.db.company_not_existing.insert_one({"company_number": company_number}).inserted_id
            return company_id
    
        except Exception as e:
    
            log.error('Insert of company {} has failed! Please check the reason below!'.format(company_number))
            log.error('Exception occurred: {}'.format(e))


    def findOfficer(self, officer):

        found = False

        try:

            if self.db.officer.find_one({'links.officer.appointments': officer['links']['officer']['appointments']}) != None:
                found = True

        except Exception as e:

            log.error('Looking for officer {} has failed. Please check the reason below!'.format(officer['links']['officer']['appointments']))
            log.error('Exception occurred: {}'.format(e))

        return found


    def insertCompanyOfficers(self, company, officers):
    
        if len(officers) == 0:
            return
    
        try:
    
            officer_ids = self.db.officer.insert_many(officers).inserted_ids
            return officer_ids
    
        except Exception as e:
    
            log.error('Bulk Insert for company\'s {} officers has failed! Please check the reason below!'.format(company["company_number"]))
            log.error('Exception occurred: {}'.format(e))
    
    def insertOfficerAppointments(self, officer_link, officer_appointments):
    
        if len(officer_appointments) == 0:
            return
    
        try:
            appointment_ids = self.db.officer_appointments.insert_many(officer_appointments).inserted_ids
            return appointment_ids
    
        except Exception as e:
    
            log.error('Bulk Insert for officer\'s {} appointments has failed! Please check the reason below!'.format(officer_link))
            log.error('Exception occurred: {}'.format(e))
    
    
    def insertCompanyPersonsWithSignificantControl(self, company, pscs):
    
        if len(pscs) == 0:
            return
    
        try:
            psc_ids = self.db.person_with_significant_control.insert_many(pscs).inserted_ids
            return psc_ids
    
        except Exception as e:
    
            log.error('Bulk Insert for company\'s {} persons with significant control has failed! Please check the reason below!'.format(company["company_number"]))
            log.error('Exception occurred: {}'.format(e))



