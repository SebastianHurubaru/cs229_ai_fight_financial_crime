from unittest import TestCase
from util.mongodb import *

class TestFindCompany(TestCase):

    def test_findCompany(self):

        db = MongoDBWrapper('cs229')

        found1 = db.findCompany('Does not exist')
        assert found1 == False, "Company 'Does not exist' should not be found"

        found2 = db.findCompany('07891296')
        assert found2 == True, "Company '07891296' should be found"

