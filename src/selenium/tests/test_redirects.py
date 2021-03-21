import os
import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.seleniumtestcase import SeleniumTestCase

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2021, Helium Edu'
__version__ = '1.4.49'


class TestSeleniumRedirects(SeleniumTestCase):
    def test_support_redirect(self):
        info = self.get_info()

        self.driver.get(os.path.join(self.app_host, 'support'))
        # The /support URL redirects to an external portal
        WebDriverWait(self.driver, 10).until(
            EC.title_is("Support for Helium")
        )
        self.assertEquals(info['support_url'], self.driver.current_url.strip('/'))

    def test_contact_redirect(self):
        info = self.get_info()

        self.driver.get(os.path.join(self.app_host, 'contact'))
        # The /support URL redirects to an external portal
        WebDriverWait(self.driver, 10).until(
            EC.title_is("Support for Helium")
        )
        self.assertEquals(info['support_url'], self.driver.current_url.strip('/'))


if __name__ == '__main__':
    unittest.main()
