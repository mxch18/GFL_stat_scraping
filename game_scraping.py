from myWebDriver import MyWebDriver
from homePage import HomePage
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--league", help="select gfl and/or gfl2", default=['gfl', 'gfl2'], nargs="*")
    parser.add_argument(
        "-y", "--year", help="select a year", type=int, nargs="*")
    parser.add_argument(
        "-g", "--game", help="select a game, format is the same as game URL")
    parser.add_argument(
        "-o", "--overwrite", help="overwrite existing games", action='store_true')
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
                    game.get_game(args.overwrite)
    finally:
        browser.quit()
