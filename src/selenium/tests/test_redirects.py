__copyright__ = "Copyright (c) 2018 Helium Edu"
__license__ = "MIT"
__version__ = "1.6.4"


import os
import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils.seleniumtestcase import SeleniumTestCase


class TestSeleniumRedirects(SeleniumTestCase):
    def test_support_redirect(self):
        # UserVoice has shutdown their free service, commenting out test until another solution is used
        pass
        # info = self.get_info()

        # self.driver.get(os.path.join(self.app_host, 'support'))
        # The /support URL redirects to an external portal
        # WebDriverWait(self.driver, 10).until(
        #     EC.title_is("Support for Helium")
        # )
        # self.assertEquals(info['support_url'], self.driver.current_url.strip('/'))

    def test_contact_redirect(self):
        # UserVoice has shutdown their free service, commenting out test until another solution is used
        pass
        # info = self.get_info()

        # self.driver.get(os.path.join(self.app_host, 'contact'))
        # The /support URL redirects to an external portal
        # WebDriverWait(self.driver, 10).until(
        #     EC.title_is("Support for Helium")
        # )
        # self.assertEquals(info['support_url'], self.driver.current_url.strip('/'))


if __name__ == '__main__':
    unittest.main()
