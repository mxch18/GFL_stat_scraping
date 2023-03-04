from myPage import MyPage
from datetime import datetime
from selenium.webdriver.common.by import By
import re


class GamePage(MyPage):
    def __init__(self, url, webdrv, season, date=None, location="", team1="", team2=""):
        super().__init__(url, webdrv)
        self.season = season
        self.date = date
        self.location = location
        self.team1 = team1
        self.team2 = team2

    def __str__(self):
        return super().__str__()+f"\nSeason:{self.season}\nDate:{self.date}"\
         f"\nLocation:{self.location}\nTeam1:{self.team1}\nTeam2:{self.team2}"

    def go_to(self):
        super().go_to()
        # fill in the potential blanks with data directly from the page
        # date, location, team1, team2
        page_title = self.driver.find_element(By.XPATH, "//font/h3/font").text

        pattern_game_info = re.compile(r"""
         (?P<team1>.+)
         \svs\s
         (?P<team2>.+)
         \s\(
         (?P<date>\d\d.\d\d.\d\d\d\d)
        """, re.VERBOSE)
        res = pattern_game_info.search(page_title)

        self.team1 = res.group('team1')
        self.team2 = res.group('team2')

        self.date = res.group('date')
        self.date = datetime.strptime(self.date, "%d.%m.%Y")


if __name__ == '__main__':
    from myWebDriver import MyWebDriver

    browser = MyWebDriver()

    gp = GamePage("https://stats.gfl.info/gfl/2022/gbshupr.htm",
                  browser, ('gfl', 2022))
    print(gp)
    gp.go_to()
    print(gp)
