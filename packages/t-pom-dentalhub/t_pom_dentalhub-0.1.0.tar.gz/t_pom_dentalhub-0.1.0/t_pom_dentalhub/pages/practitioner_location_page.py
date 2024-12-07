"""Practitioner location page."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement


class PractitionerLocationPage(BasePage):
    """Page class containing elements specific to a practitioner and location interface."""

    url = "https://app.dentalhub.com/app/login"
    treatment_location_button = ButtonElement(
        '//ng-select[contains(@placeholder, "Search by Location Name, City, or State")]', wait=False, timeout=5
    )
    treatment_location_result_button = ButtonElement('//div[contains(@class, "font-weight-bold ng-star-inserted")]')

    treating_practitioner_input = InputElement('//input[@id="treatingDentist"]', wait=False, timeout=5)
    treating_practitioner_result_button = ButtonElement("//div[contains(@class, 'ng-option ng-option-selected')]")
    billing_entity_input = InputElement('//input[@id="paymentGroupId"]', wait=False, timeout=5)
    billing_entity_result_button = treating_practitioner_result_button

    continue_button = ButtonElement('//button[normalize-space(text())="Continue"]')
    modal_close_button = ButtonElement('//button[contains(@class, "_pendo-close-guide")]', wait=False, timeout=5)
    verification_element = continue_button
