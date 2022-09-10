from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SelExceptions
import re

# set headless to 1
options = FirefoxOptions()
options.headless = True
# initiate Firefox
browser = webdriver.Firefox(options=options)

# go to home page
home_page = 'https://stats.gfl.info/'
browser.get(home_page)

try:
    # get access all years from GFL 1 & 2
    leagues = {'gfl': {}, 'gfl2': {}}
    tabElmt = browser.find_elements(By.XPATH, '//table/tbody/tr/td/a[@href]')
    for element in tabElmt:
        league_year = re.findall(
            r"gfl[0-9]*/[0-9]+", element.get_attribute('href'))[0]
except SelExceptions.NoSuchElementException:
    raise
finally:
    browser.quit()
