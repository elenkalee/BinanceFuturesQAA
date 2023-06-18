import os
import random
import time

import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromiumOptions


@allure.step("Waiting for availability {url}")
def wait_url_data(url, timeout=10):
    """Метод ожидания доступности урла"""
    while timeout:
        response = requests.get(url)
        if not response.ok:
            time.sleep(1)
            timeout -= 1
        else:
            if "video" in url:
                return response.content
            else:
                return response.text
    return None


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--executor", action="store", default="selenoid")
    parser.addoption("--bversion", action="store", default="113.0")
    parser.addoption("--vnc", action="store_true", default=False)
    parser.addoption("--logs", action="store_true", default=False)
    parser.addoption("--videos", action="store_true", default=False)
    parser.addoption("--mobile", action="store_true")

    parser.addoption("--driver_folder",
                     default="/Users/elenalee/PycharmProjects/BinanceFuturesQAA/drivers",
                     )
    parser.addoption("--url", action="store", default="https://testnet.binancefuture.com")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
# https://github.com/pytest-dev/pytest/issues/230#issuecomment-402580536
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != "passed":
        item.status = "failed"
    else:
        item.status = "passed"


@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def browser(request):
    url = request.config.getoption("--url")
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bversion")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--videos")
    mobile = request.config.getoption("--mobile")

    if executor == "local":
        options = ChromiumOptions()
        options.add_argument("--headless=new")
        caps = {"goog:chromeOptions": {}}
        driver = webdriver.Chrome(options=options, desired_capabilities=caps)
    else:
        executor_url = f"http://{executor}:4444/wd/hub"

        caps = {
            "browserName": browser,
            "browserVersion": version,
            "name": "agr test",
            "screenResolution": "1280x720",
            "selenoid:options": {
                "enableVNC": vnc,
                "name": os.getenv("BUILD_NUMBER", str(random.randint(9000, 10000))),
                "sessionTimeout": "60s",
                "enableVideo": video,
                "enableLog": False,
                "timeZone": "Europe/Moscow",
                "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"]

            },
            "acceptInsecureCerts": True,
            # 'goog:chromeOptions': {}
        }

        driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps,
            # options=options
        )

        if not mobile:
            driver.maximize_window()

    # if browser == "chrome":
    #     service = ChromiumService(executable_path=f"{driver_folder}/chromedriver")
    #     options = ChromiumOptions()
    #     options.add_argument("--headless=new")
    #     options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #     driver = webdriver.Chrome(service=service, options=options)
    #
    # else:
    #     raise ValueError("Browser is not supported")

    # request.addfinalizer(driver.quit)
    # driver.maximize_window()
    # driver.get(url)
    # driver.implicitly_wait(2)
    # return driver
    def finalizer():
        video_url = f"http://{executor}:8080/video/{driver.session_id}.mp4"

        if request.node.status == "failed":
            if video:
                allure.attach(
                    body=wait_url_data(video_url),
                    name="video_for_" + driver.session_id,
                    attachment_type=allure.attachment_type.MP4,
                )

        if video and wait_url_data(video_url):
            requests.delete(url=video_url)

        driver.quit()

    request.addfinalizer(finalizer)
    return driver
