"""Dashboard page for Dentalhub."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement


class DashboardPage(BasePage):
    """Page class containing elements specific to a dashboard interface."""

    url = "https://app.dentalhub.com/app/login"
    modal_close_button = ButtonElement('//button[contains(@class, "_pendo-close-guide")]', wait=False, timeout=5)
    menu_button = ButtonElement('//div[contains(text(), "Menu")]')
    elegibility_history_button = ButtonElement('//span[@id="EligibilityHistory"]')
    verification_element = menu_button
