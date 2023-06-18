import allure
import selenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, wait=3):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait)

    def __wait_element(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except selenium.common.exceptions.TimeoutException:
            allure.attach(
                name="screenshot",
                body=self.driver.get_screenshot_as_png()
            )
            raise AssertionError(f"Element {locator} not found.")

    @allure.step
    def open_page(self, base_url):
        self.driver.get(base_url)

    @allure.step
    def click_element(self, locator):
        self.__wait_element(locator).click()

    @allure.step
    def input_field(self, locator, value):
        find_field = self.__wait_element(locator)
        find_field.click()
        find_field.clear()
        find_field.send_keys(value)
        # find_field.send_keys(value)

    @allure.step
    def is_present(self, locator):
        self.__wait_element(locator)
