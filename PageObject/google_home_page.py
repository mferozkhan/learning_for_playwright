from PageObject.base_page import BasePage


class GoogleHomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.search_box = "textarea[name='q']"
        self.search_button = "input[name='btnK']"
        self.feeling_lucky_button = "input[name='btnI']"
        self.gmail_link = "a[href*='mail']"

    def navigate_to_google(self):
        self.goto("https://www.google.com")

    def search_for(self, query):
        self.fill(self.search_box, query)
        self.page.keyboard.press("Enter")

    def click_gmail_link(self):
        self.click(self.gmail_link)