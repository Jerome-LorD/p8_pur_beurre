"""Selenium test module."""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumTests(StaticLiveServerTestCase):
    """SeleniumTests class."""

    fixtures = ["functional_tests/users.json", "functional_tests/all-datas.json"]

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(2)
        cls.timeout = 5

    @classmethod
    def tearDownClass(cls):
        """Tear down class."""
        cls.browser.quit()
        super().tearDownClass()

    def test_login_redirect_to_profile(self):
        """Test user login and page redirect to profile."""
        self.browser.get("%s%s" % (self.live_server_url, "/auth/accounts/login/"))

        # User Bill want to log in and consult is profile:
        username_input = self.browser.find_element_by_name("email")
        username_input.send_keys("bill@bool.com")
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys("poufpouf")
        self.browser.find_element_by_xpath('//button[@value="Log-in"]').click()
        self.assertIn("Mon compte -- Pur beurre", self.browser.title)

    def test_research_substitutes_as_logged_user(self):
        """Test research substitutes as logged user."""
        self.browser.get("%s%s" % (self.live_server_url, "/auth/accounts/login/"))

        # User Bill wants to log in:
        username_input = self.browser.find_element_by_name("email")
        username_input.send_keys("bill@bool.com")
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys("poufpouf")
        self.browser.find_element_by_xpath('//button[@value="Log-in"]').click()

        # Bill is looking for a product:
        products_input = self.browser.find_element_by_id("products")
        products_input.send_keys("Coca-Cola")
        products_input.send_keys(Keys.RETURN)
        products_input.submit()
        try:
            results_page = EC.presence_of_element_located((By.ID, "cbox"))
            WebDriverWait(self.browser, self.timeout).until(results_page)
        except TimeoutException:
            print("Timed out waiting for page to load")

        self.assertIn("Substituts -- Pur beurre", self.browser.title)

        # Bill wants to add the substitute to his favorites page:

        # Bill wants to see his favorites page:
        self.browser.find_element_by_id("favorites_page").click()

        # and now, he want to log out:
        self.browser.find_element_by_id("Log-out").click()
        self.assertIn("Page d'accueil -- Pur beurre", self.browser.title)

    def test_index_title(self):
        """Test Index title is 'Page d'accueil'."""
        self.browser.get(self.live_server_url)
        self.assertIn("Page d'accueil -- Pur beurre", self.browser.title)

    def test_results_title(self):
        """Test Results title is 'Subtituts'."""
        self.browser.get(self.live_server_url + "/results/Coca-Cola/")
        self.assertIn("Substituts -- Pur beurre", self.browser.title)

    def test_product_title(self):
        """Test Product title is 'Information détaillée'."""
        self.browser.get(self.live_server_url + "/product/Coca-Cola/")
        self.assertIn("Information détaillée -- Pur beurre", self.browser.title)

    def test_favorites_redirect_to_login(self):
        """Test favorites redirect to login with no user connected."""
        self.browser.get(self.live_server_url + "/favorites/")
        self.assertIn("Login -- Pur beurre", self.browser.title)
