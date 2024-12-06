"""Generic Retrieve Smart Assistant Report page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.iframe_element import IFrameElement

from t_pom_denticon.elements.datetime_element import DateTimeElement
from t_pom_denticon.elements.select_element import SelectElement


class RetrieveSmartAssistReportPage(BasePage):
    """Page class containing elements specific to a Retrieve Smart Assistant Report interface."""

    url = "https://az2.denticon.com/ASPX/NewReports.aspx?RptName=Appointment Reports"
    table_iframe = IFrameElement('//iframe[@id="MVCReportsIFrame"]', timeout=3)
    smart_assist_report_card_input = ButtonElement('//label[@id="rbSmartAssistReportCardLabel"]')
    select_excel_format = ButtonElement('//label[@for="printformat2"]')
    dt_select_month = SelectElement('//select[@class="ui-datepicker-month"]')
    dt_start_date = DateTimeElement('//input[@id="dtStartDate"]')
    dt_end_date = DateTimeElement('//input[@id="dtEndDate"]')
    open_office_modal = ButtonElement('//button[@data-target="#offices"]')
    print_and_preview_button = ButtonElement('//button[text()=" Print / Preview"]')
    report_iframe = IFrameElement('//iframe[@id="RptTopFrame"]', timeout=40)
    download_button = ButtonElement('//img[@id="ExcelIconImg"]')

    verification_element = table_iframe
