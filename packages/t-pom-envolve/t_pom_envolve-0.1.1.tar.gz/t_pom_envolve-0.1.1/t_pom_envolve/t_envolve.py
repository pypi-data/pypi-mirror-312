"""Generic base class for web app."""
from RPA.Browser.Selenium import Selenium
from t_page_object.base_app import BaseApp
from t_page_object.bot_config import BotConfig
from t_page_object.selenium_manager import SeleniumManager
from pathlib import Path

from t_pom_envolve.pages.login_page import LoginPage
from t_pom_envolve.pages.patient_eligibility_page import PatientEligibilityPage


class TEnvolve(BaseApp):
    """Main application class managing pages and providing direct access to Selenium."""

    browser: Selenium = None
    login_page: LoginPage = LoginPage()
    patient_eligibility_page: PatientEligibilityPage = PatientEligibilityPage()
    wait_time: int = BotConfig.default_timeout
    download_directory: str = str(Path().cwd() / Path("temp"))

    def __init__(self, **config) -> None:
        """Initialise Envolve class with default configuration."""
        super().__init__(**config)
        self.browser = SeleniumManager.get_instance()
