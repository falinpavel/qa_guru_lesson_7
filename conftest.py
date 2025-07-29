import pytest
from selene.support.shared import browser
from selenium import webdriver

from const import TMP_DIR


@pytest.fixture(scope='function', autouse=True)
def driver_configuration():
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    prefs = {
        "download.default_directory": TMP_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=options)
    browser.config.driver = driver
    browser.config.base_url = 'https://www.online-convert.com/ru'
    yield
    browser.quit()
