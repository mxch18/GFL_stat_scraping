from myPage import MyPage


class GamePage(MyPage):
    def __init__(self, url, webdriver, date, location, team1, team2):
        super().__init__(url, webdriver)
        self.date = date
        self.location = location
        self.team1 = team1
        self.team2 = team2
