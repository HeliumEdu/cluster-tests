__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.5.1"

import unittest

from utils.seleniumtestcase import SeleniumTestCase


class TestSeleniumPages(SeleniumTestCase):
    def setUp(self):
        super().setUp()

        self.info = self.get_info()

    def test_tour(self):
        self.driver.get(self.app_host)
        self.assertEqual("{} | {}".format(self.info['name'], self.info['tagline']), self.driver.title)


if __name__ == '__main__':
    unittest.main()
