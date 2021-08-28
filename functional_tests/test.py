"""Selenium test module."""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class LoginSeleniumTests(StaticLiveServerTestCase):
    """SeleniumTests class."""

    fixtures = ["functional_tests/users.json"]

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        """Tear down class"""
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
        assert "Mon compte -- Pur beurre" in self.browser.title

    def test_login_logout(self):
        """Test user Bill login and log out."""
        self.browser.get("%s%s" % (self.live_server_url, "/auth/accounts/login/"))

        # User Bill want to log in:
        username_input = self.browser.find_element_by_name("email")
        username_input.send_keys("bill@bool.com")
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys("poufpouf")
        self.browser.find_element_by_xpath('//button[@value="Log-in"]').click()

        # and now, he want to log out:
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("Log-out").click()
        assert "Page d'accueil -- Pur beurre" in self.browser.title


class TitleSeleniumTests(StaticLiveServerTestCase):
    """SeleniumTests class."""

    fixtures = ["functional_tests/products.json"]

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        """Tear down class"""
        cls.browser.quit()
        super().tearDownClass()

    def test_index_title(self):
        """Test Index title is 'Page d'accueil'."""
        self.browser.get(self.live_server_url)
        assert "Page d'accueil -- Pur beurre" in self.browser.title

    def test_results_title(self):
        """Test Results title is 'Subtituts'."""
        self.browser.get(self.live_server_url + "/results/Coca-cola/")
        assert "Substituts -- Pur beurre" in self.browser.title

    def test_product_title(self):
        """Test Product title is 'Information détaillée'."""
        self.browser.get(self.live_server_url + "/product/Coca-cola/")
        assert "Information détaillée -- Pur beurre" in self.browser.title

    def test_favorites_redirect_to_login(self):
        """Test favorites redirect to login with no user connected."""
        self.browser.get(self.live_server_url + "/favorites/")
        assert "Login -- Pur beurre" in self.browser.title
