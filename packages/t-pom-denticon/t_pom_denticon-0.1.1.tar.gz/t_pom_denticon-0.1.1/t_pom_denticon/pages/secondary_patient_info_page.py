"""Generic Secondary Patient Information Page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.iframe_element import IFrameElement
from t_page_object.elements.input_element import InputElement

from t_pom_denticon.elements.text_element import TextElement


class SecondaryPatientInformationPage(BasePage):
    """Page class containing elements specific to a Secondary Patient Information Page interface."""

    url = "https://az2.denticon.com/aspx/Patients/AdvancedEditPatientInsurance.aspx?planType=D&insType=S"

    edit_insurance_iframe = IFrameElement('//iframe[@id="EditPatientInsuranceIframe"]')
    sec_pat_sub_id = InputElement('//input[@id="subIdValue"]')
    sec_pat_group = TextElement('//span[@id="showCarrierGroup"]')
    sec_cancel_ins = ButtonElement('//button[@id="btnCancelInsPlan"]')
    sec_modal_close = ButtonElement('//div[@class="modal-footer"]//button[text()="OK"]')

    verification_element = edit_insurance_iframe
