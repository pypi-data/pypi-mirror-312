"""Multi Factor Authentication Page."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement


class MultiFactorAuthenticationPage(BasePage):
    """Page class containing multi factor authentication."""

    url = "https://app.dentalhub.com/app/login"
    email_button = ButtonElement('//input[@id="extension_mfaByPhoneOrEmail_email"]', wait=False, timeout=5)
    continue_button = ButtonElement('//button[@id="continue"]')
    send_code_button = ButtonElement('//button[@id="readOnlyEmail_ver_but_send"]')
    verication_code_input = InputElement('//input[@id="readOnlyEmail_ver_input"]')
    verify_code_button = ButtonElement('//button[@id="readOnlyEmail_ver_but_verify"]')
    verification_element = continue_button
