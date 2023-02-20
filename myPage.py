class MyPage():
    def __init__(self, url, webdriver):
        self.url = url
        self.driver = webdriver

    def go_to(self):
        self.driver.get(self.url)

    def __str__(self):
        return f"URL: {self.url}\nDriver:{self.driver}"
