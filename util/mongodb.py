from util.config import *
from pymongo import MongoClient
import urllib.parse

log = logging.getLogger('mongodb')

username = urllib.parse.quote_plus(MONGO_USERNAME)
password = urllib.parse.quote_plus(MONGO_PASSWORD)

client = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))

db = client['cs229']

def findCompany(company_number):

    found = False

    try:

        if db.company.find_one({'company_number': company_number}) != None:
            found = True

    except Exception as e:

        log.error('Looking for company {} has failed. Please check the reason below!'.format(company_number))
        log.error('Exception occurred: {}'.format(e))


    return found

def insertCompany(company):

    try:

        company_id = db.company.insert_one(company).inserted_id
        return company_id

    except Exception as e:

        log.error('Insert of company {} has failed! Please check the reason below!'.format(company["company_number"]))
        log.error('Exception occurred: {}'.format(e))


def insertCompanyOfficers(company, officers):

    if len(officers) == 0:
        return

    try:

        officer_ids = db.officer.insert_many(officers).inserted_ids
        return officer_ids

    except Exception as e:

        log.error('Bulk Insert for company\'s {} officers has failed! Please check the reason below!'.format(company["company_number"]))
        log.error('Exception occurred: {}'.format(e))

def insertOfficerAppointments(officer_link, officer_appointments):

    if len(officer_appointments) == 0:
        return

    try:
        appointment_ids = db.officer_appointments.insert_many(officer_appointments).inserted_ids
        return appointment_ids

    except Exception as e:

        log.error('Bulk Insert for officer\'s {} appointments has failed! Please check the reason below!'.format(officer_link))
        log.error('Exception occurred: {}'.format(e))


def insertCompanyPersonsWithSignificantControl(company, pscs):

    if len(pscs) == 0:
        return

    try:
        psc_ids = db.person_with_significant_control.insert_many(pscs).inserted_ids
        return psc_ids

    except Exception as e:

        log.error('Bulk Insert for company\'s {} persons with significant control has failed! Please check the reason below!'.format(company["company_number"]))
        log.error('Exception occurred: {}'.format(e))



