"""Base class for DentalHub."""

from pathlib import Path

from RPA.Browser.Selenium import Selenium
from t_page_object.base_app import BaseApp
from t_page_object.selenium_manager import SeleniumManager

from t_pom_dentalhub.pages import (
    DashboardPage,
    EligibilityCheckResultsPage,
    EligibilitySelectedInsurancePage,
    LoginPage,
    MultiFactorAuthenticationPage,
    PatientInsurancePage,
    PractitionerLocationPage,
    ServiceHistoryPage,
)


class TDentalHub(BaseApp):
    """Main application class managing pages and providing direct access to Selenium."""

    browser: Selenium = None
    login_page: LoginPage = LoginPage()
    dashboard_page: DashboardPage = DashboardPage()
    patient_insurance_page: PatientInsurancePage = PatientInsurancePage()
    practitioner_location_page: PractitionerLocationPage = PractitionerLocationPage()
    eligibility_selected_insurance_page: EligibilitySelectedInsurancePage = EligibilitySelectedInsurancePage()
    eligibility_check_results_page: EligibilityCheckResultsPage = EligibilityCheckResultsPage()
    service_history_page: ServiceHistoryPage = ServiceHistoryPage()
    multi_factor_authentication_page: MultiFactorAuthenticationPage = MultiFactorAuthenticationPage()
    wait_time: int = 15
    download_directory: str = str(Path().cwd() / Path("temp"))

    def __init__(self, **config) -> None:
        """Initilise DentalHub class with default configuration."""
        super().__init__(**config)
        self.browser = SeleniumManager.get_instance()
