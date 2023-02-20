import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SelExceptions
import re
import json
import functools


class MyWebDriver(webdriver.Firefox):
    def deco_get(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Going to {args[1]}...")
            func(*args, **kwargs)
            print("Reached")
        return wrapper

    def deco_quit(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("Closing browser...")
            func(*args, **kwargs)
            print("Closed")
        return wrapper

    @deco_get
    def my_get(self, *args, **kwargs):
        self.get(*args, **kwargs)

    @deco_quit
    def my_quit(self, *args, **kwargs):
        self.quit(*args, **kwargs)


def get_seasons():
    pass


def get_games():
    pass


if __name__ == '__main__':
    # set headless to 1
    options = FirefoxOptions()
    options.headless = True
    # initiate Firefox
    print("Starting browser...")
    browser = MyWebDriver.Firefox(options=options)
    print("Browser started")

    # go to home page
    home_page = 'https://stats.gfl.info/'
    browser.my_get(home_page)

    links_to_seasons = browser.find_elements(
        By.XPATH, '//table/tbody/tr/td/a[@href]')

    for link in links_to_seasons:
        league = (link.get_attribute('href').split("/"))[0]
        # go to season page
        browser.my_get(home_page+link.get_attribute('href'))
        # select the rows of the table that comes after the header Game Results
        games_rows = browser.find_elements(
            By.XPATH,
            "//h2[text()='Game Results']/following-sibling::table/tbody/tr[@bgcolor='#ffffff']")
        # get all links
        for game in games_rows:
            game.find_element(By.XPATH, "//a[text()='Box Score']")
