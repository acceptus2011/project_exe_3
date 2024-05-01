from django.test import LiveServerTestCase
from selenium import webdriver

class PurchaseTestCase(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_navigate_site(self):
        self.browser.get('http://localhost:800')
        assert 'Django' in self.browser.title
