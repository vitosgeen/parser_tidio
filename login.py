from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import Config

# login to tidio account with your credentials (login, password) 
# arguments: config - configuration object with your credentials
#             reference to the driver object
def login_to_tidio(config, driver):
    # login to tidio account with your credentials (login, password)
    driver.get('https://www.tidio.com/panel/login?redirectTo=inbox%2Fconversations%2Fsolved%2F')

    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))
    sleep(10)
    # check if browser is already logged in (if not, login)
    if 'login' not in driver.current_url:
        print("Already logged in")
        return

    # Wait for the login form to load
    form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app form')))
    driver.save_screenshot('screenshot-login.png')
    # Fill in the login form
    form.find_element(By.CSS_SELECTOR, 'form input[type="email"]').send_keys(config.get_tidio_login())
    form.find_element(By.CSS_SELECTOR, 'form input[type="password"]').send_keys(config.get_tidio_password())
    driver.save_screenshot('screenshot-login-filled.png')
    # focus on the login button
    # form.find_element(By.CSS_SELECTOR, 'form button svg').click()
    driver.save_screenshot('screenshot-show-password.png')
    # Submit the login form by clicking the login button 
    sleep(30)
    # Wait for the button to be clickable
    try:
        login_button = WebDriverWait(form, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'form button[type="submit"]'))
        )
        # Submit the login form by clicking the login button
        login_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")
    sleep(15)

    print("Logged in")