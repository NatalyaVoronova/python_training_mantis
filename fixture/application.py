from selenium import webdriver
from fixture.project import ProjectHelper
from fixture.session import SessionHelper


class Application:

    def __init__(self, browser, base_url):
        if browser == 'firefox':
            self.wd = webdriver.Firefox()
        elif browser == 'chrome':
            self.wd = webdriver.Chrome()
        elif browser == 'ie':
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)

        self.wd.implicitly_wait(1)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.base_url = base_url

    def return_to_home_page(self):
        wd = self.wd
        wd.find_element_by_link_text("home page").click()

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def destroy(self):
        self.wd.quit()
