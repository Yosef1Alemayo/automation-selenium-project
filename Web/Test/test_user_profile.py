import allure
from Web.Utils.utils import Utils
from Web.Pages.accessibility_page import Accessibility_Page
from Web.coftest import Fixtures
import pytest
from Web.Pages.user_profile_page import User_Profile_Page

@pytest.mark.usefixtures('login_successfully')
@pytest.mark.parametrize('browser', ['chrome'])
class Test_User_Profile(Fixtures):

    @allure.description('Accessibility test on about-us page clicking one color after the other')
    @allure.severity(allure.severity_level.NORMAL)
    def test_accessibility1(self):
        driver = self.driver
        accessibility = Accessibility_Page(driver)
        accessibility.clicking_color(2)
        accessibility.clicking_color(3)
        accessibility.clicking_color(4)
        accessibility.clicking_color(1)

    @allure.description('Accessibility test on about-us page clicking on color and return to default color')
    @allure.severity(allure.severity_level.NORMAL)
    def test_accessibility2(self):
        driver = self.driver
        accessibility = Accessibility_Page(driver)
        accessibility.clicking_color(2)
        accessibility.clicking_color(1)
        accessibility.clicking_color(3)
        accessibility.clicking_color(1)
        accessibility.clicking_color(4)
        accessibility.clicking_color(1)

    @allure.description('Searching correctly')
    @pytest.mark.sanity
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_correctly(self):
        city_name = 'Barcelona'
        driver = self.driver
        search = Utils(driver)
        search.searching(city_name)
        search.assertion(f'Discover {city_name}', search.city_name_correctly())

    @allure.description('Searching incorrectly')
    @pytest.mark.sanity
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_incorrectly(self):
        city_name = '!!!'
        driver = self.driver
        search = Utils(driver)
        search.searching(city_name)
        search.assertion('No City Found', search.city_name_incorrectly())

    def test_update_details(self):
        driver = self.driver
        user = User_Profile_Page(driver)
        pass