from selenium.webdriver.common.by import By
from myPage import MyPage
from seasonPage import SeasonPage
import re


class HomePage(MyPage):
    def __init__(self, url, webdriver):
        super().__init__(url, webdriver)

    def get_seasons(self, league=None, year=None):
        season_pages = []  # list of SeasonPage object
        season_links = self.driver.find_elements(
            By.XPATH, '//table/tbody/tr/td/a[@href]')
        for link in season_links:
            league_year = re.findall(
                r"gfl[0-9]*/[0-9]+", link.get_attribute('href'))[0]
            if league_year:
                ly_split = league_year.split("/")
                link_league = ly_split[0]
                link_year = int(ly_split[1])

                nok_league = league and link_league != league
                nok_year = year and link_year != year

                if nok_league or nok_year:
                    pass
                else:
                    season_pages.append(
                        SeasonPage(
                            link.get_attribute('href'),
                            self.driver,
                            link_league,
                            link_year
                            )
                    )

        return season_pages


if __name__ == '__main__':
    from myWebDriver import MyWebDriver

    browser = MyWebDriver()

    hp = HomePage("https://stats.gfl.info/", browser)
    hp.go_to()
    se = hp.get_seasons()
    for s in se:
        print(s)
