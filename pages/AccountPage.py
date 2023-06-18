from selenium.webdriver.common.by import By

from .BasePage import BasePage


class AccountPage(BasePage):
    BALANCE = (By.CSS_SELECTOR, ".balance")
    BTN_BUY_LONG = (By.XPATH, '//button[text()="Buy/Long"]')

    # def verify_balance_el(self):
    #     return self.is_present(self.BALANCE)
