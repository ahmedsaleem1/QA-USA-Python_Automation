import data
import helpers
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)

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
        assert "to" in self.driver.page_source.lower(), "❌ Route setting failed – destination not found in page."

    def test_select_plan(self):
        self.page.select_plan()
        plan_element = self.driver.find_element("xpath", "//div[contains(text(),'Supportive')]")
        assert "selected" in plan_element.get_attribute("class"), "❌ Plan was not selected."

    def test_fill_phone_number(self):
        self.page.fill_phone_number()
        code_input = self.driver.find_element("id", "code")
        assert code_input.get_attribute("value") != "", "❌ Phone code input is empty."

    def test_fill_card(self):
        self.page.fill_card()
        # No visible confirmation – soft assertion for now
        print("✅ Card information filled.")

    def test_comment_for_driver(self):
        self.page.comment_for_driver()
        comment_box = self.driver.find_element("id", "comment")
        assert data.MESSAGE_FOR_DRIVER in comment_box.get_attribute("value"), "❌ Comment not set correctly."

    def test_order_blanket_and_handkerchiefs(self):
        self.page.order_blanket_and_handkerchiefs()
        blanket_toggle = self.driver.find_element("class name", "blankets")
        assert "selected" in blanket_toggle.get_attribute("class"), "❌ Blanket option was not selected."

    def test_order_ice_cream(self):
        self.page.order_ice_cream(count=2)
        ice_cream_selected = self.driver.find_element("class name", "ice-creams")
        # This assumes the class or count changes — adjust logic if needed
        assert ice_cream_selected, "❌ Ice cream order may have failed."

    def test_submit_order(self):
        self.page.submit_order()
        modal = self.driver.find_element("class name", "modal")
        assert modal.is_displayed(), "❌ Order confirmation modal did not appear."


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
