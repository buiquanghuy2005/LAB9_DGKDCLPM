from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def element(driver, test_id):
    return WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-test="{test_id}"]'))
    )


def login(driver, username='standard_user', password='secret_sauce'):
    element(driver, 'username').send_keys(username)
    element(driver, 'password').send_keys(password)
    element(driver, 'login-button').click()


def inventory(driver):
    WebDriverWait(driver, 15).until(EC.url_contains('/inventory.html'))
    assert element(driver, 'title').text == 'Products'
    assert len(driver.find_elements(By.CSS_SELECTOR, '.inventory_item')) == 6


def test_TC01_login_valid(driver):
    login(driver)
    inventory(driver)


def test_TC02_login_wrong_password(driver):
    login(driver, password='wrong_password')
    assert 'Username and password do not match' in element(driver, 'error').text
    assert '/inventory.html' not in driver.current_url


def test_TC03_login_locked_user(driver):
    login(driver, username='locked_out_user')
    assert 'Sorry, this user has been locked out.' in element(driver, 'error').text
    assert '/inventory.html' not in driver.current_url


def test_TC04_login_empty_username(driver):
    element(driver, 'password').send_keys('secret_sauce')
    element(driver, 'login-button').click()
    assert 'Username is required' in element(driver, 'error').text


def test_TC05_add_to_cart(driver):
    login(driver)
    inventory(driver)
    element(driver, 'add-to-cart-sauce-labs-backpack').click()
    assert element(driver, 'shopping-cart-badge').text == '1'
    element(driver, 'shopping-cart-link').click()
    items = driver.find_elements(By.CSS_SELECTOR, '.cart_item')
    assert len(items) == 1
    assert items[0].find_element(By.CSS_SELECTOR, '.inventory_item_name').text == 'Sauce Labs Backpack'
    assert items[0].find_element(By.CSS_SELECTOR, '.cart_quantity').text == '1'


def test_TC06_remove_from_cart(driver):
    login(driver)
    inventory(driver)
    element(driver, 'add-to-cart-sauce-labs-backpack').click()
    assert element(driver, 'shopping-cart-badge').text == '1'
    element(driver, 'shopping-cart-link').click()
    element(driver, 'remove-sauce-labs-backpack').click()
    WebDriverWait(driver, 15).until(
        lambda d: not d.find_elements(By.CSS_SELECTOR, '.cart_item')
        and not d.find_elements(By.CSS_SELECTOR, '.shopping_cart_badge')
    )


def test_TC07_sort_price_ascending(driver):
    login(driver)
    inventory(driver)
    Select(element(driver, 'product-sort-container')).select_by_value('lohi')
    def sorted_prices(d):
        prices = [float(e.text.replace('$', '')) for e in d.find_elements(By.CSS_SELECTOR, '.inventory_item_price')]
        return len(prices) == 6 and prices == sorted(prices)
    WebDriverWait(driver, 15).until(sorted_prices)


def test_TC08_logout(driver):
    login(driver)
    inventory(driver)
    driver.find_element(By.ID, 'react-burger-menu-btn').click()
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'logout_sidebar_link'))).click()
    assert element(driver, 'login-button').is_displayed()
    driver.get(driver.current_url.rstrip('/') + '/inventory.html')
    assert element(driver, 'login-button').is_displayed()
    assert 'You can only access' in element(driver, 'error').text
