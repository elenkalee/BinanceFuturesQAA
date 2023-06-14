from selenium.webdriver.common.by import By

from .BasePage import BasePage


class LoginPage(BasePage):
    LOGIN_LINK = (By.CSS_SELECTOR, "#header_login")
    USERNAME_INPUT = (By.CSS_SELECTOR, "#login_input_email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#login_input_password")
    LOG_IN_BTN = (By.CSS_SELECTOR, "#login_input_login")

    # def open_login_page(self):
    #     self.get_current_url()
    #     self.assert_url("https://testnet.binancefuture.com/en/futures/BTCUSDT")

    def go_to_login_link(self):
        self.click_element(self.LOGIN_LINK)

    def login_as_user(self):
        self.input_field(self.USERNAME_INPUT, "USERNAME")
        self.input_field(self.PASSWORD_INPUT, "PASSWORD")
        self.click_element(self.LOG_IN_BTN)
