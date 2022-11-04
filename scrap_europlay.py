from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SelExceptions
import time
import functools


class MyWebDriver(webdriver.Firefox):
    def deco_get(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Going to {args[1]}...")
            func(*args, **kwargs)
            print("Reached")
        return wrapper

    def deco_quit(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("Closing browser...")
            func(*args, **kwargs)
            print("Closed")
        return wrapper

    @deco_get
    def my_get(self, *args, **kwargs):
        self.get(*args, **kwargs)

    @deco_quit
    def my_quit(self, *args, **kwargs):
        self.quit(*args, **kwargs)


if __name__ == '__main__':
    # set headless to 1
    options = FirefoxOptions()
    options.headless = True
    # initiate Firefox
    print("Starting browser...")
    browser = MyWebDriver(options=options)
    print("Browser started")

    browser.implicitly_wait(10)  # seconds

    player_to_find = "M. Achiepi"  # one result
    # player_to_find = "D. Johnson"  # multi results

    # go to EuroPlayers American Football home page
    uri_homepage = 'https://europlayers.com/Default.aspx?SportId=1'
    browser.my_get(uri_homepage)
    # Check if user is logged in
    try:
        user = browser.find_element(
            By.XPATH, "//*[@class='BlockTitleLoggedInAs']")
    except SelExceptions.NoSuchElementException:
        # go to login page
        login_uri = 'https://europlayers.com/Login.aspx'
        browser.my_get(login_uri)

        # put login information
        # //input[@id="Email"]
        print("Inputting email...")
        field_email = browser.find_element(By.XPATH, '//input[@id="Email"]')
        field_email.clear()
        field_email.send_keys('maxens.achiepi@gmx.com')
        time.sleep(1)

        # //input[@id="Password"]
        print("Inputting password...")
        field_password = browser.find_element(
                By.XPATH, '//input[@id="Password"]')
        field_password.clear()
        field_password.send_keys('v42GN7UJMk2Evxw')
        time.sleep(1)

        # //input[@value="Login"]
        browser.find_element(By.XPATH, '//input[@value="Login"]').click()

        user = browser.find_element(
            By.XPATH, "//*[@class='BlockTitleLoggedInAs']")
    finally:
        print(f"Logged in as {user.find_element(By.XPATH, './a[1]').text}")

        # Go to advanced search (looks only for players)
        adv_search_uri = 'https://europlayers.com/SearchPlayerFilter.aspx?SportId=1'
        browser.my_get(adv_search_uri)

        player_to_find_split = player_to_find.split('.')
        surname_to_search = player_to_find_split[1].lstrip()
        letter_to_search = player_to_find_split[0]

        field_player_name = browser.find_element(
            By.XPATH, "//input[@name='Name']")
        field_player_name.clear()
        field_player_name.send_keys(surname_to_search)

        browser.find_element(By.XPATH, "//input[@id='Submit2']").click()

        # loop through all pages
        players_found = []
        while True:
            players_table = browser.find_element(
                By.XPATH, "//table[@class='Europlayers']")

            if len(players_table.find_elements(By.XPATH, "./tbody/tr")) > 1:
                player_found = players_table.find_elements(
                        By.XPATH, f"./tbody/tr[./td[4]/div/a[text()='{surname_to_search}']]/td[3]/div/a[starts-with(.,'{letter_to_search}')]"
                     )
                # //table[@class='Europlayers']/tbody/tr/td[4]/div/a[text()='Johnson' and ancestor::tr/td[3]/div/a[starts-with(.,'H')]]
                # //table[@class='Europlayers']/tbody/tr[./td[4]/div/a[text()='Johnson']]/td[3]/div/a[starts-with(.,'H')]

                if player_found:
                    players_found.extend(player_found)

                try:
                    btn_next = browser.find_element(
                        By.XPATH, "//div[@class='Pagination']/a[text()='Next']")
                    print(
                        f"Going to page {btn_next.get_attribute('href')[-1]}"
                        )
                    btn_next.click()
                except SelExceptions.NoSuchElementException:

                    print("Reached last page of search")

                    if len(players_found) == 1:
                        player_url = players_found[0].get_attribute('href')
                        print(
                            f"Found {player_to_find} at URL {player_url}"
                            )
                        browser.my_get(player_url)

                        # player data
                        player_data = {
                            'nationality': '',
                            'position1': '',
                            'position2': '',
                            'age': '',
                            'height': '',  # only metrics
                            'weight': ''   # only metrics
                        }

                        # list of span's to scrap
                        span_to_scrap = {
                            'nationality': 'ctl00_cphMain_Nationality',
                            'position': 'ctl00_cphMain_Position',
                            'age': 'ctl00_cphMain_Age',
                            'height': 'ctl00_cphMain_Height',
                            'weight': 'ctl00_cphMain_Weight'
                        }

                        for (info, id) in span_to_scrap.items():
                            try:
                                info_scrap = browser.find_element(
                                    By.ID, id).text

                                if info == 'position':  # possible to have 2
                                    info_scrap_split = info_scrap.split(',')
                                    player_data['position1'] = info_scrap_split[0].strip(
                                    )

                                    if len(info_scrap_split) > 1:
                                        player_data['position2'] = info_scrap_split[1].strip(
                                        )

                                elif info == 'height' or info == 'weight':  # remove imperial
                                    player_data[info] = info_scrap.split(
                                        '-')[0].strip()

                                else:
                                    player_data[info] = info_scrap

                            except SelExceptions.NoSuchElementException:
                                continue

                        print(player_data)

                    else:
                        print(
                            f"{player_to_find} not found on Europlayers or found too many times ({len(players_found)})")

                    break

        browser.my_quit()
