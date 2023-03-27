from myPage import MyPage
from datetime import datetime
from selenium.webdriver.common.by import By
import re
from pathlib import Path
from player import Player


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

        info_line = self.driver.find_element(
            By.XPATH, "//center/b/following-sibling::p/font[contains(text(),'Site')]")
        pattern_location = re.compile(r"""
         (?<=Site:).*?(?=•)
        """, re.VERBOSE)

        res = pattern_location.search(info_line.text)
        self.location = res.group().strip()

    def get_game(self):
        directory = './games/' + \
            self.season[0] + '/' + str(self.season[1]) + '/'
        Path(directory).mkdir(parents=True, exist_ok=True)

        filename = self.date.strftime("%Y-%m-%d") + '_' + \
            '(' + self.team1 + ')' + '@' + '(' + self.team2 + ')'
        with open(directory+filename+'.game', 'w') as file_game:
            print(
             f"Saving {self.team1} vs. {self.team2} on {self.date} in {filename}")
            file_game.write(str(self)+'\n')
            file_game.write(
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"+'\n')

            quarter_tables = self.driver.find_elements(
                By.XPATH, "//a[@name='start']/../following-sibling::table")
            for table in quarter_tables:
                for row in table.find_elements(By.XPATH, "./tbody/tr[count(td)=4]"):
                    possession = row.find_element(
                        By.XPATH, "./td[1]").text.upper()

                    down = togo = ''
                    down_togo = row.find_element(By.XPATH, "./td[2]").text
                    if len(down_togo):
                        down, togo = down_togo.split('-')

                    location = row.find_element(By.XPATH, "./td[3]").text
                    if len(location):
                        location = location.split()[1].upper()

                    play = row.find_element(By.XPATH, "./td[4]").text

                    list_to_save = [possession, down, togo, location, play]
                    text_to_save = '$'.join(list_to_save)
                    file_game.write(text_to_save+'\n')
            file_game.write(
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++"+'\n')
            file_game.write(str(self.get_participation_report()))

    def get_participation_report(self):
        participation_report = {}  # {'team': [(Player(), number, isStarter)]}

        # first table is a "normal" table
        first_tables = self.driver.find_elements(
            By.XPATH, "//h3/font[contains(text(),'Participation')]/ancestor::table/../following-sibling::p/table/tbody/tr/td/table")

        for table in first_tables:
            team = table.find_element(
                By.XPATH, "./tbody/tr[1]/td/font").text.rstrip()
            starters_row = table.find_elements(
                By.XPATH, "./tbody/tr[@bgcolor='#ffffff' and count(td)=3]")
            for starter in starters_row:
                pos = starter.find_element(
                    By.XPATH, "./td[1]/font").text.rstrip()
                num = starter.find_element(
                    By.XPATH, "./td[2]/font").text.rstrip()
                name = starter.find_element(
                    By.XPATH, "./td[3]/font").text.rstrip()
                first_name, last_name = name.split('.')
                current_participation = participation_report.get(team, [])
                current_participation.append(
                    (Player(first_name, last_name, position=[pos]),
                     int(num),
                     1)
                )
                participation_report[team] = current_participation

        # second and third tables are just a big string
        next_tables = self.driver.find_elements(
            By.XPATH, "//h3/font[contains(text(),'Participation')]/ancestor::table/../following-sibling::p/table/tbody/tr/td/font")
        pattern_bench = re.compile(r"""
            (?P<number>\d+)
            \-
            (?P<player>[A-Z]\.([a-z]\.)?[A-Za-z\-]+)
        """, re.VERBOSE)
        for table in next_tables:
            team = table.find_element(By.XPATH, "./b").text.rstrip()
            bench_str = table.text
            for res in pattern_bench.finditer(bench_str):
                first_name, last_name = res.group('player').split('.')
                current_participation = participation_report.get(team, [])
                current_participation.append(
                    (Player(first_name, last_name),
                     int(res.group('number')),
                     0)
                )
                participation_report[team] = current_participation

        return participation_report


if __name__ == '__main__':
    from myWebDriver import MyWebDriver

    browser = MyWebDriver()

    gp = GamePage("https://stats.gfl.info/gfl/2022/gbshupr.htm",
                  browser, ('gfl', 2022))
    gp.go_to()
    print(gp)
    gp.get_game()
    print(gp.get_participation_report())
