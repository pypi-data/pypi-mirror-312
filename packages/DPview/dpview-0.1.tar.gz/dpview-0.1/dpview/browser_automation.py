from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class BrowserAutomation:
    def __init__(self, browser_type='chrome'):
        if browser_type == 'chrome':
            self.driver = webdriver.Chrome()
        elif browser_type == 'firefox':
            self.driver = webdriver.Firefox()
        # Add other browsers as needed

    def open_url(self, url):
        self.driver.get(url)

    def find_element(self, selector):
        return self.driver.find_element(By.CSS_SELECTOR, selector)

    def click_element(self, selector):
        self.find_element(selector).click()

    def input_text(self, selector, text):
        self.find_element(selector).send_keys(text)

    def close_browser(self):
        self.driver.quit()

