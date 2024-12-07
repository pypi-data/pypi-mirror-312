from selenium.webdriver.common.by import By

class RenderTools:
    def __init__(self, driver):
        self.driver = driver

    def inspect_element(self, selector):
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        return element.get_attribute('outerHTML')

    def get_page_source(self):
        return self.driver.page_source

