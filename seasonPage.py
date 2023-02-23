from myPage import MyPage
from gamePage import GamePage
import re
from selenium.webdriver.common.by import By


class SeasonPage(MyPage):
    def __init__(self, url, webdriver):
        # checking validity of URL
        league_year = re.findall(r"gfl[0-9]*/[0-9]+", url)[0]
        if league_year:
            ly_split = league_year.split("/")
            self.league = ly_split[0]
            self.year = ly_split[1]
            super().__init__(url, webdriver)
        else:
            print(f"Invalid season url: {url}")

    def __str__(self):
        return super().__str__()+f"\nLeague: {self.league}\nYear: {self.year}"

    def get_season_from_list(season_pages_list, league, year):
        # utility function, in case we need a specific season
        for season_page in season_pages_list:
            if season_page.league == league and season_page.year == year:
                return season_page

    def get_games(self):
        game_pages = []  # list of GamePage objects
        game_links = self.driver.find_elements(
            By.XPATH,
            "//h2[text()='Game Results']/following-sibling::table/tbody/tr[@bgcolor='#ffffff']"
        )

        for link in game_links:
            link_to_game = link.find_element(
                By.XPATH, "./td[4]/font/a").get_attribute('href')
            game_pages.append(
                GamePage(
                    link_to_game,
                    self.driver,
                    (self.league, self.year)
                    )
            )

        return game_pages


if __name__ == '__main__':
    from myWebDriver import MyWebDriver

    browser = MyWebDriver()

    sp = SeasonPage("https://stats.gfl.info/gfl/2022/confstat.htm", browser)
    sp.go_to()

    [print(g) for g in sp.get_games()]
