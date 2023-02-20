from selenium import webdriver
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
    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)

    @ deco_quit
    def quit(self, *args, **kwargs):
        super().quit(*args, **kwargs)


if __name__ == '__main__':
    p = MyWebDriver()
    p.get("https://stats.gfl.info/")
    p.quit()
