"""Login page for DentalHub."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement


class LoginPage(BasePage):
    """Page class containing elements specific to login on DentalHub."""

    url = "https://app.dentalhub.com/app/login"
    login_page_button = ButtonElement("//button[@id='btnOidcLogin']")
    user_email_input = InputElement("//input[@id='signInName']")
    password_input = InputElement("//input[@id='password']")
    login_in_button = ButtonElement("//button[@id='next']")
    verification_element = login_page_button
