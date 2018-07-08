import os
import unittest

from utils.seleniumtestcase import SeleniumTestCase

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.26'


class TestSeleniumPages(SeleniumTestCase):
    def setUp(self):
        super().setUp()

        self.info = self.get_info()

    def test_tour(self):
        self.driver.get(self.app_host)
        self.assertEquals("{} | {}".format(self.info['name'], self.info['tagline']), self.driver.title)

    def test_contact(self):
        self.driver.get(os.path.join(self.app_host, 'contact'))
        # print(self.driver.execute_script("return document.script"))
        self.assertEquals("{} | Contact".format(self.info['name']), self.driver.title)

        # TODO: add an assertion to ensure the JS renders the contact widget properly


if __name__ == '__main__':
    unittest.main()
