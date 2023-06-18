import time
from csv import DictReader
import allure
import pytest

from pages.AccountPage import AccountPage
from pages.LoginPage import LoginPage


def get_cookies_values(file):
    with open(file, encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
    return list_of_dicts


@allure.feature("UI Login Tests")
class TestLoginPage:
    @allure.title("Test that Login Page is opened")
    def test_open_login_page(self, browser, base_url):
        lp = LoginPage(browser)
        lp.open_page(base_url)
        lp.go_to_login_link()
        assert browser.title == "Log In | Binance"
        time.sleep(2)

    @pytest.mark.a
    @allure.title("Test that account for authorized user is opened")
    def test_login_as_user(self, browser, base_url):
        """Add relevant cookies to file for authorized user to bypass Captcha"""
        ap = AccountPage(browser)
        ap.open_page(base_url)
        cookies = get_cookies_values("tests/tests_ui/testnet_cookies.csv")
        for i in cookies:
            browser.add_cookie(i)
        browser.refresh()
        ap.is_present(ap.BTN_BUY_LONG)
        # assert ap.verify_buy_button_is_visible().text() == "Buy/Long"
