import data
import helpers
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Chrome options to enable performance logging
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        # Start Chrome WebDriver
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)

        # Verify server connection
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("✅ Connected to the Urban Routes server")
        else:
            raise Exception("❌ Cannot connect to Urban Routes. Check that the server is running.")

        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        self.page.set_route()

    def test_select_plan(self):
        self.page.select_plan()

    def test_fill_phone_number(self):
        self.page.fill_phone_number()

    def test_fill_card(self):
        self.page.fill_card()

    def test_comment_for_driver(self):
        self.page.comment_for_driver()

    def test_order_blanket_and_handkerchiefs(self):
        self.page.order_blanket_and_handkerchiefs()

    def test_order_ice_cream(self):
        self.page.order_ice_cream(count=2)

    def test_submit_order(self):
        self.page.submit_order()


if __name__ == "__main__":
    TestUrbanRoutes.setup_class()
    test_suite = TestUrbanRoutes()
    try:
        test_suite.test_set_route()
        test_suite.test_select_plan()
        test_suite.test_fill_phone_number()
        test_suite.test_fill_card()
        test_suite.test_comment_for_driver()
        test_suite.test_order_blanket_and_handkerchiefs()
        test_suite.test_order_ice_cream()
        test_suite.test_submit_order()
    finally:
        TestUrbanRoutes.teardown_class()

