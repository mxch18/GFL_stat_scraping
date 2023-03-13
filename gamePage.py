from myPage import MyPage
from datetime import datetime
from selenium.webdriver.common.by import By
import re
from pathlib import Path


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

    def get_game(self):
        directory = './games/' + \
            self.season[0] + '/' + str(self.season[1]) + '/'
        Path(directory).mkdir(parents=True, exist_ok=True)

        filename = self.date.strftime("%Y-%m-%d") + '_' + \
            '(' + self.team1 + ')' + '@' + '(' + self.team2 + ')'
        with open(directory+filename+'.game', 'w') as file_game:
            print(f"{self.team1} vs. {self.team2} on {self.date} in {filename}")
            quarter_tables = self.driver.find_elements(
                By.XPATH, "//a[@name='start']/../following-sibling::table")
            for table in quarter_tables:
                for description in table.find_elements(By.XPATH, "./tbody/tr/td[4]/font"):
                    file_game.write(description.text+'\n')


if __name__ == '__main__':
    from myWebDriver import MyWebDriver

    browser = MyWebDriver()

    gp = GamePage("https://stats.gfl.info/gfl/2022/gbshupr.htm",
                  browser, ('gfl', 2022))
    gp.go_to()
    print(gp)
    gp.get_game()
