"""Generic base class for web app."""
from RPA.Browser.Selenium import Selenium
from t_page_object.base_app import BaseApp
from t_page_object.selenium_manager import SeleniumManager

from t_pom_denticon.pages.login_page import LoginPage
from t_pom_denticon.pages.offices_list_modal import OfficesListModal
from t_pom_denticon.pages.patient_notes_page import PatientNotesPage
from t_pom_denticon.pages.patient_overview_info_page import PatientOverviewInfoPage
from t_pom_denticon.pages.primary_patient_info_page import PrimaryPatientInformationPage
from t_pom_denticon.pages.report_viewer import ReportViewerPage
from t_pom_denticon.pages.retrieve_dps_report_page import RetrieveDpsReportPage
from t_pom_denticon.pages.retrieve_smart_assist_report_page import RetrieveSmartAssistReportPage
from t_pom_denticon.pages.secondary_patient_info_page import SecondaryPatientInformationPage
from t_pom_denticon.pages.update_payer_info import UpdatePayerInformation


class TDenticon(BaseApp):
    """Main application class managing pages and providing direct access to Selenium."""

    browser: Selenium = None
    login_page: LoginPage = LoginPage()
    retrieve_smart_assist_report_page: RetrieveSmartAssistReportPage = RetrieveSmartAssistReportPage()
    offices_list_modal_page: OfficesListModal = OfficesListModal()
    retrieve_dps_report_page: RetrieveDpsReportPage = RetrieveDpsReportPage()
    report_viewer_page: ReportViewerPage = ReportViewerPage()
    update_payer_information_page: UpdatePayerInformation = UpdatePayerInformation()
    patient_information_page: PatientOverviewInfoPage = PatientOverviewInfoPage()
    primary_patient_information_page: PrimaryPatientInformationPage = PrimaryPatientInformationPage()
    secondary_patient_information_page: SecondaryPatientInformationPage = SecondaryPatientInformationPage()
    patient_notes_page: PatientNotesPage = PatientNotesPage()

    def __init__(self, **config) -> None:
        """Initilise DentiCon class with default configuration."""
        super().__init__(**config)
        self.browser = SeleniumManager.get_instance()
