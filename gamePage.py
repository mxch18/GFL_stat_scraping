from myPage import MyPage
from datetime import datetime


class GamePage(MyPage):
    def __init__(self, url, webdrv, date=None, location="", team1="", team2=""):
        super().__init__(url, webdrv)
        self.date = date
        self.location = location
        self.team1 = team1
        self.team2 = team2

    def __str__(self):
        return super().__str__()+f"Date:{self.date}\nLocation:{self.location}\nTeam1:{self.team1}\nTeam2:{self.team2}"
