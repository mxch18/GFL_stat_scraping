from selenium.webdriver.common.by import By
from myPage import MyPage
from seasonPage import SeasonPage


class HomePage(MyPage):
    def __init__(self, url, webdriver):
        super().__init__(url, webdriver)

    def get_seasons(self):
        season_pages = []  # list of SeasonPage object
        season_links = self.driver.find_elements(
            By.XPATH, '//table/tbody/tr/td/a[@href]')
        for link in season_links:
            season_pages.append(
                SeasonPage(
                    link.get_attribute('href'),
                    self.driver
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
