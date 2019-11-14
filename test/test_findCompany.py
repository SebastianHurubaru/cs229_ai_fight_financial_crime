from unittest import TestCase
from util.mongodb import findCompany

class TestFindCompany(TestCase):

    def test_findCompany(self):

        found1 = findCompany('Does not exist')
        assert found1 == False, "Company 'Does not exist' should not be found"

        found2 = findCompany('07891296')
        assert found2 == True, "Company '07891296' should be found"

