from myWebDriver import MyWebDriver
from homePage import HomePage
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--league", help="select between gfl and gfl2", choices=['gfl', 'gfl2'])
    parser.add_argument("-y", "--year", help="select a year", type=int)
    parser.add_argument(
        "-g", "--game", help="select a game, format is the same as game URL")
    args = parser.parse_args()

    # set headless to 1
    options = FirefoxOptions()
    options.headless = True
    browser = MyWebDriver(options=options)

    try:
        hp = HomePage("https://stats.gfl.info/", browser)
        hp.go_to()

        seasons = hp.get_seasons(args.league, args.year)

        for season in seasons:
            season.go_to()
            if args.game:
                games = [season.get_specific_game(args.game)]
            else:
                games = season.get_games()

            for game in games:
                if game:
                    game.go_to()
                    game.get_game()
    finally:
        browser.quit()
