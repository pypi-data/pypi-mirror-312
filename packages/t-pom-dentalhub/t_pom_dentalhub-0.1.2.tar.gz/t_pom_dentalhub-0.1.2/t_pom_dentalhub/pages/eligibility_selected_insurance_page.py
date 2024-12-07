"""Specific page for web app."""
from t_page_object.base_page import BasePage

from t_pom_dentalhub.elements import TextElement


class EligibilitySelectedInsurancePage(BasePage):
    """Page class containing elements specific to selected insurance interface."""

    url = "https://app.dentalhub.com/app/login"
    effective_date = TextElement('//div[@id="selected-insurance-effective-date"]')
    verification_element = effective_date
