"""Generic login page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement
from t_page_object.elements.text_element import TextElement


class LoginPage(BasePage):
    """Page class containing elements specific to a login interface."""

    url = "https://pwp.envolvedental.com/PWP/Landing"

    user_name_input = InputElement("//input[@id='UserName']")
    password_input = InputElement("//input[@id='Password']")
    sign_in_button = ButtonElement("//button[@id='LoginBlockButton']")
    is_two_fa_enable = TextElement("//*[contains(@custom-id, 'verifyYourIdentity')]", timeout=60)
    verify_identity_button = ButtonElement("//button[@id='LoginBlockButton']", timeout=60)
    otp_input = InputElement('//input[@id="VerificationCodeTextBox"]', timeout=60)
    submit_button = ButtonElement('//button[@id="SubmitButton"]', timeout=60)
    is_otp_btn_enable = TextElement('//button[@disabled="disabled"]', timeout=60)

    verification_element = user_name_input
