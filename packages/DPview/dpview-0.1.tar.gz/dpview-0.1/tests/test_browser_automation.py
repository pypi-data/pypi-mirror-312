import unittest
from dpview.browser_automation import BrowserAutomation

class TestBrowserAutomation(unittest.TestCase):
    def setUp(self):
        self.browser = BrowserAutomation()

    def test_open_url(self):
        self.browser.open_url('https://www.example.com')
        self.assertIn("Example Domain", self.browser.driver.title)

    def tearDown(self):
        self.browser.close_browser()

if __name__ == "__main__":
    unittest.main()

