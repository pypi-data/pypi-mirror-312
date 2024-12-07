"""Generic patient eligibility page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement

from t_pom_envolve.elements.datetime_element import DateTimeElement
from t_pom_envolve.elements.select_element import SelectElement


class PatientEligibilityPage(BasePage):
    """Page class containing elements specific to a patient eligibility."""

    url = "https://pwp.envolvedental.com/PWP/Dental"

    office_location_select = SelectElement('//select[@id="location-select"]', timeout=60)
    provider_select = SelectElement('//select[@id="provider-select"]', timeout=60)
    date_of_service_input = DateTimeElement("//input[@id='DateOfServiceTextBox']", timeout=60)
    subscriber_id_input = InputElement("//input[@id='SubscriberId2TextBox']", timeout=60)
    date_of_birth_input = DateTimeElement("//input[@id='DateOfBirth2TextBox']", timeout=60)
    verify_eligibility_button = ButtonElement("//button[@id='VerifyButton']", timeout=60)
    view_eligibility_report = ButtonElement("//button[@id='ViewEligReportButton']", timeout=60)
    view_patient_history = ButtonElement("//button[@id='ViewPatientHistoryButton']", timeout=60)
    export_button = ButtonElement("//table[@title='Export drop down menu']", timeout=120)
    download_link = ButtonElement("//a[@title='Excel']//parent::div", timeout=120)

    verification_element = office_location_select
