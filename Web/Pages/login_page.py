import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from Web.Locators.locators_login_page import Locators_Login_Page
from selenium.webdriver.common.by import By
from Web.Utils.utils import Utils
from selenium.webdriver.support.wait import WebDriverWait as WAIT
from selenium.webdriver.support import expected_conditions as EC

class Login_Page:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.emailBox = Locators_Login_Page.EMAIL_FIELD
        self.passwordBox = Locators_Login_Page.PASSWORD_FIELD
        self.loginButton = Locators_Login_Page.LOGIN_BUTTON
        self.profileLink = Locators_Login_Page.PROFILE_BUTTON
        self.loginValidationMessage = Locators_Login_Page.LOGIN_VALIDATION_MESSAGE
        self.email_Password_error = Locators_Login_Page.ERROR_MESSAGE1
        self.userError = Locators_Login_Page.ERROR_MESSAGE2
        self.showPasswordButton = Locators_Login_Page.SHOW_PASSWORD_BUTTON
        self.UI = Locators_Login_Page.UI

    @allure.step
    @allure.description('Navigate to login page')
    def login_page(self):
        url = 'https://trip-yoetz.herokuapp.com/login'
        self.driver.get(url)
        Utils(self.driver).assertion(url, self.driver.current_url)
        self.driver.implicitly_wait(20)

    @allure.step
    @allure.description('Navigate to user profile after successfully login')
    def click_profile_link(self):
        self.driver.find_element(By.CSS_SELECTOR, self.profileLink).click()
        WAIT(self.driver, 20).until(EC.url_to_be('https://trip-yoetz.herokuapp.com/profile'))
        Utils(self.driver).assertion( 'https://trip-yoetz.herokuapp.com/profile', self.driver.current_url)

    @allure.step
    @allure.description('Show password button - should display text in password input')
    def click_show_password_button(self):
        value = self.driver.find_element(By.NAME, self.passwordBox).get_attribute('type')
        Utils(self.driver).assertion('password', value)
        self.driver.find_element(By.CSS_SELECTOR, self.showPasswordButton).click()
        Utils(self.driver).assertion('text', value)

    @allure.step
    @allure.description('Clear and insert data to email input')
    def enter_email(self, email):
        email_input = self.driver.find_element(By.NAME, self.emailBox)
        email_input.clear()
        email_input.send_keys(email)
        Utils(self.driver).assertion(email, email_input.get_attribute('value'))

    @allure.step
    @allure.description('Clear and insert data to password input')
    def enter_password(self, password):
        password_input = self.driver.find_element(By.NAME, self.passwordBox)
        password_input.clear()
        password_input.send_keys(password)
        Utils(self.driver).assertion(password, password_input.get_attribute('value'))

    @allure.step
    @allure.description('Login button - should return 2 error messages or alert')
    def login_button(self):
        self.driver.find_element(By.XPATH, self.loginButton).click()

    @allure.step
    @allure.description('Alert after login successfully')
    def accept_alert(self):
        WAIT(self.driver, 20).until((EC.alert_is_present()))
        alert = self.driver.switch_to.alert
        alert.accept()
        self.driver.forward()

    @allure.step
    @allure.description('Validation - the message from user profile page after successfully login')
    def login_validation_message(self):
        WAIT(self.driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, self.loginValidationMessage)))
        return self.driver.find_element(By.XPATH, self.loginValidationMessage).get_attribute('innerText')

    @allure.step
    @allure.description('Validation - error messages where email not in the email format')
    def js_email(self):
        return self.driver.find_element(By.NAME, self.emailBox).get_attribute('validationMessage')

    @allure.step
    @allure.description('Validation - error messages where password not in the password format')
    def js_password(self):
        return self.driver.find_element(By.NAME, self.passwordBox).get_attribute('validationMessage')

    @allure.step
    @allure.description('Validation - error message where password is invalid')
    def email_or_password_error(self):
        return self.driver.find_element(By.XPATH, self.email_Password_error).get_attribute('innerText')

    @allure.step
    @allure.description('Validation - error message where email is invalid')
    def no_user_error_message(self):
        return self.driver.find_element(By.XPATH, self.userError).get_attribute('innerText')

    @allure.step
    @allure.description('Validation - returns all the text in page')
    def ui(self):
        return self.driver.find_element(By.XPATH, self.UI).get_attribute('innerText')
