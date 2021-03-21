import os
import unittest

from utils.seleniumtestcase import SeleniumTestCase

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2021, Helium Edu'
__version__ = '1.4.49'


class TestSeleniumPages(SeleniumTestCase):
    def setUp(self):
        super().setUp()

        self.info = self.get_info()

    def test_tour(self):
        self.driver.get(self.app_host)
        self.assertEquals("{} | {}".format(self.info['name'], self.info['tagline']), self.driver.title)


if __name__ == '__main__':
    unittest.main()
