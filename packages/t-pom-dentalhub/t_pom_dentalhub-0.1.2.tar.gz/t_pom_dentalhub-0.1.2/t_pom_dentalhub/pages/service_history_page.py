"""Service history page."""
from t_page_object.base_page import BasePage

from t_pom_dentalhub.elements import TableElement


class ServiceHistoryPage(BasePage):
    """Page class containing elements specific to service history interface."""

    url = "https://app.dentalhub.com/app/login"
    service_history_table = TableElement('//table[@id="service-results-table"]')
    verification_element = service_history_table
