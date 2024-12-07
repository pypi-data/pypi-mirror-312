"""Page for patient insurance form."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement


class PatientInsurancePage(BasePage):
    """Page class containing elements specific to a patient insurance interface."""

    url = "https://app.dentalhub.com/app/login"
    subscriber_id_input = InputElement("//input[@id='subscriberId_Front']")
    first_name_input = InputElement("//input[@id='firstName_Back']")
    last_name_input = InputElement("//input[@id='lastName_Back']")
    date_of_birth_input = InputElement("//input[@id='dateOfBirth_Back']")
    procedure_date_input = InputElement("//input[@id='procedureDate_Back']")

    patient_relationship_button = ButtonElement('//*[@id="relationshipCode"]')
    patient_relationship_input = InputElement('//*[@id="relationshipCode"]/div/div/div[3]/input')
    patient_relationship_result_button = ButtonElement("//span[contains(@class, 'ng-option-label')]")

    payer_input = InputElement('//input[@id="insurerId"]')
    payer_result = ButtonElement("//div[contains(@class, 'ng-option ng-option-child')]")

    continue_button = ButtonElement('//button[normalize-space(text())="Continue"]')
    verification_element = subscriber_id_input
