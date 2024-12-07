"""Page to check the results of eligibility."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement

from t_pom_dentalhub.elements import TextElement


class EligibilityCheckResultsPage(BasePage):
    """Page class containing elements specific to eligibility check result interface."""

    url = "https://app.dentalhub.com/app/login"
    check_if_member_elegible = TextElement('//span[contains(text(), "Member Eligible as")]')
    eligibility_hyperlink_button = ButtonElement('//button[@id="eligibility-link"]')
    service_history_hyperlink_button = ButtonElement('(//button[@id="patient-history-link"])[2]')
    verification_element = check_if_member_elegible
