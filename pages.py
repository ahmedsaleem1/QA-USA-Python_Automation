from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import data as data_constants
import helpers as helper_funcs


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get(data_constants.URBAN_ROUTES_URL)

    def set_route(self):
        wait = WebDriverWait(self.driver, 10)

        from_input = wait.until(expected_conditions.visibility_of_element_located((By.ID, "from")))
        from_input.clear()
        from_input.send_keys(data_constants.ADDRESS_FROM)
        from_input.send_keys(Keys.RETURN)

        to_input = wait.until(expected_conditions.visibility_of_element_located((By.ID, "to")))
        to_input.clear()
        to_input.send_keys(data_constants.ADDRESS_TO)
        to_input.send_keys(Keys.RETURN)

    def select_plan(self):
        wait = WebDriverWait(self.driver, 10)
        plan = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Supportive')]")))

        if "selected" not in plan.get_attribute("class"):
            plan.click()

    def fill_phone_number(self):
        wait = WebDriverWait(self.driver, 10)
        phone_input = wait.until(expected_conditions.visibility_of_element_located((By.ID, "phone")))
        phone_input.clear()
        phone_input.send_keys(data_constants.PHONE_NUMBER)

        send_button = self.driver.find_element(By.CLASS_NAME, "send-button")
        send_button.click()

        code_input = wait.until(expected_conditions.visibility_of_element_located((By.ID, "code")))
        code = helper_funcs.retrieve_phone_code(self.driver)
        code_input.send_keys(code)

    def fill_card(self):
        wait = WebDriverWait(self.driver, 10)

        card_input = wait.until(expected_conditions.visibility_of_element_located((By.ID, "number")))
        card_input.clear()
        card_input.send_keys(data_constants.CARD_NUMBER)

        code_input = self.driver.find_element(By.ID, "code")
        code_input.send_keys(data_constants.CARD_CODE)
        code_input.send_keys(Keys.TAB)

        link_button = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "button-link")))
        link_button.click()

    def comment_for_driver(self):
        wait = WebDriverWait(self.driver, 10)
        comment_box = wait.until(expected_conditions.visibility_of_element_located((By.ID, "comment")))
        comment_box.send_keys(data_constants.MESSAGE_FOR_DRIVER)

    def order_blanket_and_handkerchiefs(self):
        wait = WebDriverWait(self.driver, 10)
        blanket_toggle = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "blankets")))
        blanket_toggle.click()

        wait.until(lambda d: "selected" in blanket_toggle.get_attribute("class"))

    def order_ice_cream(self, count=2):
        wait = WebDriverWait(self.driver, 10)
        ice_cream_button = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "ice-creams")))

        for _ in range(count):
            ice_cream_button.click()

    def submit_order(self):
        wait = WebDriverWait(self.driver, 10)
        order_button = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "next-button")))
        order_button.click()

        modal = wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "modal")))
        assert modal.is_displayed()
