from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

def retrieve_phone_code():
    # Placeholder: return a dummy phone code for testing purposes
    return "1234"

class UrbanRoutesPage:
    # Addresses
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    # Tariff and call button
    supportive_plan_card = (By.XPATH, '//div[contains(text(), "Supportive")]')
    supportive_plan_card_parent = (By.XPATH, '//div[contains(text(), "Supportive")]//..')
    active_plan_card = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')
    call_taxi_button = (By.XPATH, '//button[contains(text(), "Call a taxi")]')
    # Phone number
    phone_number_control = (By.XPATH, '//div[@class="np-button"]//div[contains(text(), "Phone number")]')
    phone_number_input = (By.ID, 'phone')
    phone_number_code_input = (By.ID, 'code')
    phone_number_next_button = (By.CSS_SELECTOR, '.full')
    phone_number_confirm_button = (By.XPATH, '//button[contains(text(), "Confirm")]')
    phone_number = (By.CLASS_NAME, 'np-text')
    # Payments
    payment_method_select = (By.XPATH, '//div[@class="pp-button filled"]//div[contains(text(), "Payment method")]')
    add_card_control = (By.XPATH, '//div[contains(text(), "Add card")]')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.XPATH, '//input[@class="card-input" and @id="code"]')
    card_credentials_confirm_button = (By.XPATH, '//button[contains(text(), "Link")]')
    close_button_payment_method = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    current_payment_method = (By.CLASS_NAME, 'pp-value-text')
    # Options
    message_for_driver = (By.ID, 'comment')
    option_switches = (By.CLASS_NAME, 'switch')
    option_switches_inputs = (By.CLASS_NAME, 'switch-input')
    add_enumerable_option = (By.CLASS_NAME, 'counter-plus')
    amount_of_enumerable_option = (By.CLASS_NAME, 'counter-value')
    # Order
    order_car_button = (By.CLASS_NAME, 'smart-button-wrapper')
    order_popup = (By.CLASS_NAME, 'order-body')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        from_field = WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(self.from_field))
        from_field.send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_call_taxi_button(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.call_taxi_button))
        self.driver.find_element(*self.call_taxi_button).click()

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.click_call_taxi_button()

    def select_supportive_plan(self):
        if self.driver.find_element(*self.supportive_plan_card_parent).get_attribute("class") != "tcard active":
            card = WebDriverWait(self.driver, 3).until(
                expected_conditions.visibility_of_element_located(self.supportive_plan_card))
            self.driver.execute_script("arguments[0].scrollIntoView();", card)
            card.click()

    def get_current_selected_plan(self):
        return self.driver.find_element(*self.active_plan_card).text

    def set_phone(self, number):
        self.driver.find_element(*self.phone_number_control).click()
        self.driver.find_element(*self.phone_number_input).send_keys(number)
        self.driver.find_element(*self.phone_number_next_button).click()
        code = retrieve_phone_code()
        self.driver.find_element(*self.phone_number_code_input).send_keys(code)
        self.driver.find_element(*self.phone_number_confirm_button).click()

    def get_phone(self):
        return self.driver.find_element(*self.phone_number).text

    def set_card(self, card_number, code):
        self.driver.find_element(*self.payment_method_select).click()
        time.sleep(2)
        self.driver.find_element(*self.add_card_control).click()
        self.driver.find_element(*self.card_number_input).send_keys(card_number)
        self.driver.find_element(*self.card_code_input).send_keys(code)
        self.driver.find_element(*self.card_credentials_confirm_button).click()
        self.driver.find_element(*self.close_button_payment_method).click()

    def get_current_payment_method(self):
        return self.driver.find_element(*self.current_payment_method).text

    def set_message_for_driver(self, message):
        self.driver.find_element(*self.message_for_driver).send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_for_driver).get_property('value')

    def click_blanket_and_handkerchiefs_option(self):
        switches = self.driver.find_elements(*self.option_switches)
        switches[0].click()
        self.get_blanket_and_handkerchiefs_option_checked()

    def get_blanket_and_handkerchiefs_option_checked(self):
        switches = self.driver.find_elements(*self.option_switches_inputs)
        return switches[0].get_property('checked')

    def add_ice_cream(self, amount: int):
        option_add_controls = self.driver.find_elements(*self.add_enumerable_option)
        self.driver.execute_script("arguments[0].scrollIntoView();", option_add_controls[0])
        for count in range(amount):
            option_add_controls[0].click()

    def get_amount_of_ice_cream(self):
        return int(self.driver.find_elements(*self.amount_of_enumerable_option)[0].text)

    def click_order_taxi_button(self):
        self.driver.find_element(*self.order_car_button).click()

    def is_order_taxi_popup(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.order_popup))
        return self.driver.find_element(*self.order_popup).is_displayed()

