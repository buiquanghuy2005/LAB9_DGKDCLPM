import os
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption('--headed', action='store_true', help='Show Chrome window')


@pytest.fixture
def driver(request):
    options = Options()
    if not request.config.getoption('--headed'):
        options.add_argument('--headless=new')
    options.add_argument('--window-size=1440,1000')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-features=PasswordLeakDetection')
    options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False,
    })
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(45)
    request.node.browser = browser
    try:
        browser.get(os.getenv('BASE_URL', 'https://www.saucedemo.com/'))
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    browser = getattr(item, 'browser', None)
    if browser and (report.when == 'call' or (report.when == 'setup' and report.failed)):
        folder = Path('evidence')
        folder.mkdir(exist_ok=True)
        path = folder / f'{item.name}-{report.outcome}.png'
        try:
            browser.save_screenshot(str(path))
        except Exception as error:
            report.sections.append(('Screenshot error', str(error)))
