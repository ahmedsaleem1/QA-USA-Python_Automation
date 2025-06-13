from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
import helpers as helper_funcs


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.driver.get(data.URBAN_ROUTES_URL)

    # 🔎 Locators
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    PLAN_SUPPORTIVE = (By.XPATH, "//div[contains(text(),'Supportive')]")
    PHONE_INPUT = (By.ID, "phone")
    SEND_BUTTON = (By.CLASS_NAME, "send-button")
    CODE_INPUT = (By.ID, "code")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    LINK_BUTTON = (By.CLASS_NAME, "button-link")
    COMMENT_BOX = (By.ID, "comment")
    BLANKET_TOGGLE = (By.CLASS_NAME, "blankets")
    ICE_CREAM_BUTTON = (By.CLASS_NAME, "ice-creams")
    ORDER_BUTTON = (By.CLASS_NAME, "next-button")
    MODAL = (By.CLASS_NAME, "modal")

    def set_route(self):
        from_input = self.wait.until(EC.visibility_of_element_located(self.FROM_INPUT))
        from_input.clear()
        from_input.send_keys(data.ADDRESS_FROM + Keys.RETURN)

        to_input = self.wait.until(EC.visibility_of_element_located(self.TO_INPUT))
        to_input.clear()
        to_input.send_keys(data.ADDRESS_TO + Keys.RETURN)

    def select_plan(self):
        plan = self.wait.until(EC.element_to_be_clickable(self.PLAN_SUPPORTIVE))
        if "selected" not in plan.get_attribute("class"):
            plan.click()

    def fill_phone_number(self):
        phone_input = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        phone_input.clear()
        phone_input.send_keys(data.PHONE_NUMBER)

        self.driver.find_element(*self.SEND_BUTTON).click()

        code = helper_funcs.retrieve_phone_code(self.driver)
        code_input = self.wait.until(EC.visibility_of_element_located(self.CODE_INPUT))
        code_input.send_keys(code)

    def fill_card(self):
        card_input = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        card_input.clear()
        card_input.send_keys(data.CARD_NUMBER)

        code_input = self.driver.find_element(*self.CARD_CODE_INPUT)
        code_input.send_keys(data.CARD_CODE)
        code_input.send_keys(Keys.TAB)

        self.wait.until(EC.element_to_be_clickable(self.LINK_BUTTON)).click()

    def comment_for_driver(self):
        comment_box = self.wait.until(EC.visibility_of_element_located(self.COMMENT_BOX))
        comment_box.clear()
        comment_box.send_keys(data.MESSAGE_FOR_DRIVER)

    def order_blanket_and_handkerchiefs(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE))
        toggle.click()
        self.wait.until(lambda d: "selected" in toggle.get_attribute("class"))

    def order_ice_cream(self, count=2):
        ice_cream_button = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_BUTTON))
        for _ in range(count):
            ice_cream_button.click()

    def submit_order(self):
        order_button = self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON))
        order_button.click()

        modal = self.wait.until(EC.visibility_of_element_located(self.MODAL))
        return modal.is_displayed()
