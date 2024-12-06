"""Generic Patient Overview Info Page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.iframe_element import IFrameElement
from t_page_object.elements.input_element import InputElement

from t_pom_denticon.elements.table_row_element import TableRowElement
from t_pom_denticon.elements.text_element import TextElement


class PatientOverviewInfoPage(BasePage):
    """Page class containing elements specific to a Patient Overview Info Page interface."""

    url = "https://az2.denticon.com/ASPX/Home/AdvancedSearchPatients.aspx?ASPT=True"

    search_patient_iframe = IFrameElement('//iframe[@id="AdvancedSearchPatientsIFrame"]', timeout=3)
    check_pat_radio_button = ButtonElement(
        '//label[@for="patient-id-radio"]',
    )
    check_all_offices_radio_button = ButtonElement(
        '//label[@for="all-office-radio"]',
    )
    search_box = InputElement(
        '//input[@id="pat-search-box"]',
    )
    search_button = ButtonElement(
        '//button[@id="search-button"]',
    )
    flash_alerts_close_modal = ButtonElement(
        '//div[@id="flash-alert-container"]//div[@class="modal-footer"]//button[text()=" Close"]',
    )
    advanced_overview_iframe = IFrameElement('//iframe[@id="AdvancedPatientOverviewIFrame"]', timeout=3)
    carrier_name_row = TableRowElement(
        '//div[normalize-space(text())="Carrier Name"]//ancestor::'
        'div[@class="custom-col-20"]//following-sibling::div',
    )
    pat_type_value = TableRowElement(
        '//div[@class="patient-information-wrapper"]//div'
        '[normalize-space(text())="Type"]//..//following-sibling::div',
    )
    primary_insurance_dental = ButtonElement(
        '//a[@id="editPrimDentalIns"]',
    )
    patient_not_found = TextElement(
        '//td[text()="No matching records found"]',
    )

    verification_element = search_patient_iframe
