import time

class DynamicContentHandler:
    def __init__(self, browser_driver):
        self.driver = browser_driver

    def wait_for_element(self, selector, timeout=30):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    return element
            except:
                pass
            time.sleep(1)
        raise TimeoutError(f"Element {selector} not found within {timeout} seconds")

