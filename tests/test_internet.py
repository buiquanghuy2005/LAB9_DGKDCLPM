import os
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv('BASE_URL', 'https://the-internet.herokuapp.com/').rstrip('/') + '/'


def visit(driver, path):
    driver.get(urljoin(BASE_URL, path))


def visible(driver, selector):
    return WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )


def login(driver, username='tomsmith', password='SuperSecretPassword!'):
    visit(driver, 'login')
    visible(driver, '#username').send_keys(username)
    visible(driver, '#password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()


def test_TC01_login_valid(driver):
    login(driver)
    WebDriverWait(driver, 15).until(EC.url_contains('/secure'))
    assert visible(driver, 'h2').text == 'Secure Area'
    assert 'You logged into a secure area!' in visible(driver, '#flash').text
    assert visible(driver, 'a[href="/logout"]').is_displayed()


def test_TC02_login_wrong_password(driver):
    login(driver, password='WrongPassword123!')
    assert 'Your password is invalid!' in visible(driver, '#flash').text
    assert urlparse(driver.current_url).path == '/login'
    assert visible(driver, '#password').is_displayed()


def test_TC03_login_wrong_username(driver):
    login(driver, username='invalid_user_lab9')
    assert 'Your username is invalid!' in visible(driver, '#flash').text
    assert urlparse(driver.current_url).path == '/login'


def test_TC04_logout(driver):
    login(driver)
    assert 'You logged into a secure area!' in visible(driver, '#flash').text
    visible(driver, 'a[href="/logout"]').click()
    assert 'You logged out of the secure area!' in visible(driver, '#flash').text
    assert urlparse(driver.current_url).path == '/login'
    assert visible(driver, '#username').is_displayed()
    assert visible(driver, '#password').is_displayed()


def test_TC05_checkboxes(driver):
    visit(driver, 'checkboxes')
    boxes = driver.find_elements(By.CSS_SELECTOR, '#checkboxes input[type="checkbox"]')
    assert len(boxes) == 2
    assert not boxes[0].is_selected()
    assert boxes[1].is_selected()
    boxes[0].click()
    boxes[1].click()
    assert boxes[0].is_selected()
    assert not boxes[1].is_selected()


def test_TC06_dropdown(driver):
    visit(driver, 'dropdown')
    dropdown = Select(visible(driver, '#dropdown'))
    dropdown.select_by_value('1')
    assert dropdown.first_selected_option.text == 'Option 1'
    dropdown.select_by_value('2')
    assert dropdown.first_selected_option.get_attribute('value') == '2'
    assert dropdown.first_selected_option.text == 'Option 2'


def test_TC07_add_elements(driver):
    visit(driver, 'add_remove_elements/')
    assert not driver.find_elements(By.CSS_SELECTOR, '#elements button.added-manually')
    button = visible(driver, 'button[onclick="addElement()"]')
    for _ in range(3):
        button.click()
    elements = driver.find_elements(By.CSS_SELECTOR, '#elements button.added-manually')
    assert len(elements) == 3
    assert all(e.text == 'Delete' for e in elements)


def test_TC08_remove_elements(driver):
    visit(driver, 'add_remove_elements/')
    button = visible(driver, 'button[onclick="addElement()"]')
    for _ in range(3):
        button.click()
    assert len(driver.find_elements(By.CSS_SELECTOR, '#elements button.added-manually')) == 3
    for count in (2, 1, 0):
        visible(driver, '#elements button.added-manually').click()
        assert len(driver.find_elements(By.CSS_SELECTOR, '#elements button.added-manually')) == count
