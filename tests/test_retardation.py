from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SelExceptions


class retardationTest():
    def __init__(self, wbdrv):
        self.driver = wbdrv

    def go_to_page(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    # initiate Firefox
    print("Starting browser...")
    browser = webdriver.Firefox()
    print("Browser started")

    retard = retardationTest(browser)
    retard.go_to_page('https://stats.gfl.info/')
    retard.close()
