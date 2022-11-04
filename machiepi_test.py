from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SelExceptions
import re
import footballJargon

# set headless to 1
options = FirefoxOptions()
options.headless = True
# initiate Firefox
print("Starting browser...")
browser = webdriver.Firefox(options=options)
print("Browser started")

# go to home page
home_page = 'https://stats.gfl.info/'
print("Going to GFL stats website...")
browser.get(home_page)
print(f"Reached {home_page}")

try:
    # get all years from GFL 1 & 2
    leagues = {'gfl': {}, 'gfl2': {}}
    tabElmt = browser.find_elements(By.XPATH, '//table/tbody/tr/td/a[@href]')

    for element in tabElmt:
        league_year = re.findall(
            r"gfl[0-9]*/[0-9]+", element.get_attribute('href'))[0]

        if league_year:
            ly_split = league_year.split("/")

            leagues[ly_split[0]].update([(ly_split[1], {})])

    for (league, years) in leagues.items():
        for (year, _) in years.items():
            page = home_page+league+'/'+year+'/confstat.htm'
            print(f"Going to {page}...")
            browser.get(page)
            print("Reached")

            tabTeams = browser.find_elements(
                    By.XPATH, '//center/font/a[@href]')

            for team in tabTeams:
                print(
                    f"Found team {team.text} at address {team.get_attribute('href')}"
                    )

                leagues[league][year].update(
                        [(team.text, team.get_attribute('href'))]
                    )
    # here leagues contains all URI to team statistics for every year in both
    # gfl and gfl2
    # leagues['gfl']['2021']['Dresden Monarchs'] =
    #     https://stats.gfl.info/gfl/2021/dm.htm

except SelExceptions.NoSuchElementException:
    raise
finally:
    print("Closing browser...")
    browser.quit()
    print("Closed")
