"""Generic Report Viewer page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.iframe_element import IFrameElement


class ReportViewerPage(BasePage):
    """Page class containing elements specific to a Report Viewer page interface."""

    url = "https://az2.denticon.com/"
    report_iframe = IFrameElement('//iframe[@id="RptTopFrame"]', timeout=40)
    download_button = ButtonElement('//img[@id="ExcelIconImg"]')
    verification_element = report_iframe
