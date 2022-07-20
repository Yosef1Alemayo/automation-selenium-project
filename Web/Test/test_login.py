import allure
import pytest
from Web.Base.base import Base
from Web.Pages.login_page import Login_Page
from Web.Utils.utils import Utils

@pytest.mark.usefixtures('set_up')
@pytest.mark.parametrize('browser', ['chrome', 'firefox'])
class Test_Login(Base):

    @allure.description('Login Successfully, This is The PreCondition for User Profile Tests')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    def test_login_successfully(self):
        driver = self.driver
        login = Login_Page(driver)
        login.login_page()
        login.enter_email('Yosef@gmail.com')
        login.enter_password('123456')
        login.login_button()
        login.accept_alert()
        driver.forward()
        login.click_profile_link()
        Utils(driver).assertion('YOUR INFORMATION', login.login_validation_message())

    @allure.description('Login When The Values in The Fields Are Invalid')
    @pytest.mark.regression
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_fields_all_the_options(self):
        driver = self.driver
        login = Login_Page(driver)
        login.login_page()
        emails = ['Fasil', 'Yosef@', 'Miki@.com', '!!!!']
        passwords = ['5', '10', '100', '', '1115555']

        for i in range(len(emails)):
            for j in range(len(passwords)):
                login.enter_email(emails[i])
                login.enter_password(passwords[j])
                login.login_button()
                """ All The Email Format Messages In The input """
                # Message 1:
                if "חסר '@' " in login.js_email():
                    Utils(driver).assertion(login.js_email(),
                                            f"אני רוצה לכלול '@' בכתובת האימייל. ב-'{emails[i]}' חסר '@'.")
                # Message 2:
                elif "אינו מלא" in login.js_email():
                    Utils(driver).assertion(login.js_email(), f"יש להזין חלק ואחריו '@'. השדה '{emails[i]}' אינו מלא.")
                # Message 3:
                elif "שגוי" in login.js_email():
                    invalid_email = emails[i]
                    for letter in range(len(invalid_email)):
                        if invalid_email[letter] == '@':
                            text_for_assertion = invalid_email[letter+1:]
                            Utils(driver).assertion(login.js_email(), f"נעשה שימוש "
                                                                      f"ב-'.' במיקום שגוי ב-'{text_for_assertion}'.")

                """ All The Password Format Messages In the input"""
                # Message 1:
                if len(passwords[j]) in range(2, 4):
                    Utils(driver).assertion(login.js_password(), f'Please lengthen this text to 4 characters '
                                                                 f'or more (you are currently '
                                                                 f'using {len(passwords[j])} characters).')
                elif len(passwords[j]) == 1:
                    Utils(driver).assertion(login.js_password(), 'Please lengthen this text to 4 characters or more'
                                                                 ' (you are currently using 1 character).')

    @allure.description('Login Incorrectly When The Email is Correct and The Password is Incorrect')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_user_exist_and_incorrect_password(self):
        driver = self.driver
        login = Login_Page(driver)
        compare = Utils(driver)
        login.login_page()
        login.enter_email('Yosef@gmail.com')
        login.enter_password('walla-com')
        login.login_button()
        compare.assertion(login.email_or_password_error(), 'password or email incorrect')

    @allure.description('Login Incorrectly When The Email is Incorrect and The Password is Incorrect')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_user_not_exist_and_incorrect_password(self):
        driver = self.driver
        login = Login_Page(driver)
        compare = Utils(driver)
        login.login_page()
        login.enter_email('Yossss@gmail.com')
        login.enter_password('walla-com')
        login.login_button()
        compare.assertion(login.no_user_error_message(), 'no user found')

    @allure.description('Searching Correctly')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    def test_search_correctly(self):
        city = 'Paris'
        driver = self.driver
        login = Login_Page(driver)
        login.login_page()
        search = Utils(driver)
        search.searching(city)
        search.assertion(search.city_name_correctly(), f'Discover {city}')

    @allure.description('Searching Incorrectly')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    def test_search_incorrectly(self):
        city = 'Israel'
        driver = self.driver
        login = Login_Page(driver)
        login.login_page()
        search = Utils(driver)
        search.searching(city)
        search.assertion(search.city_name_incorrectly(), 'No City Found')

    @allure.description('Navigate From Login Page To All The Pages In The Website')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.sanity
    def test_nav_bar_links(self):
        driver = self.driver
        login = Login_Page(driver)
        login.login_page()
        x = Utils(driver)
        x.click_navbar_links('Login')

    @allure.description('Verify All The Text In The page')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_ui(self):
        driver = self.driver
        login = Login_Page(driver)
        login.login_page()
        login.ui()
        compare = Utils(driver)
        compare.assertion(login.ui(), "Login\nRegister\nAbout us\nTripYoetz\nNew here ?\nTo"
                                      " register please click the link below\nRegister\nLogin\n"
                                      "LOGIN\nMarcos Bazbih\n24 years old, Ashdod\nTikva Yosef"
                                      "\n26 years old, Natanya\nAvi Admaso\n26 years old, Ashdod"
                                      "\nWho are we?\nTripYoetz\nLearn more\ncopyright © | 2022"
                                      " TripYoetz | all right reserved.")

    @allure.description('Accessibility Test')
    @allure.severity(allure.severity_level.NORMAL)
    def test_accessibility(self):
        driver = self.driver
        login = Login_Page(driver)
        utils = Utils(driver)
        login.login_page()
        driver.implicitly_wait(20)
        utils.click_colors()
