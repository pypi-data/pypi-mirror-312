"""Generic Retrieve DPS Report page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.iframe_element import IFrameElement

from t_pom_denticon.elements.datetime_element import DateTimeElement


class RetrieveDpsReportPage(BasePage):
    """Page class containing elements specific to a Retrieve DPS Report interface."""

    url = "https://az2.denticon.com/ASPX/NewReports.aspx?RptName=Insurance Reports"

    table_iframe = IFrameElement('//iframe[@id="MVCReportsIFrame"]', timeout=3)
    dps_report_card_input = ButtonElement('//label[@for="rbDPSEligibility"]')
    select_excel_format = ButtonElement('//label[@for="rbPrintFormatExcel"]')
    select_office_group = ButtonElement('//label[@for="rbOffice"]')
    open_office_modal = ButtonElement('//button[@data-target="#offices"]')
    dt_patient_start_date = DateTimeElement('//input[@id="dtPatCreatedStartDate"]')
    dt_patient_end_date = DateTimeElement('//input[@id="dtPatCreatedEndDate"]')
    print_and_preview_button = ButtonElement('//button[text()=" Print / Preview"]')
    report_iframe = IFrameElement('//iframe[@id="RptTopFrame"]', timeout=40)
    download_button = ButtonElement('//img[@id="ExcelIconImg"]')

    verification_element = table_iframe
