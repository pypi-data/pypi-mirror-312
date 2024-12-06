"""Generic Primary Patient Information Page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.iframe_element import IFrameElement
from t_page_object.elements.input_element import InputElement

from t_pom_denticon.elements.select_element import SelectElement
from t_pom_denticon.elements.text_element import TextElement


class PrimaryPatientInformationPage(BasePage):
    """Page class containing elements specific to a Primary Patient Information Page interface."""

    url = "https://az2.denticon.com/aspx/Patients/AdvancedEditPatientInsurance.aspx?planType=D&insType=P"

    edit_insurance_iframe = IFrameElement('//iframe[@id="EditPatientInsuranceIframe"]')
    prim_pat_sub_id = InputElement('//input[@id="subIdValue"]')
    prim_pat_group = TextElement('//span[@id="showCarrierGroup"]')
    prim_pat_sex = SelectElement('//select[@id="subscriberSexInfoDropdown"]//option[@selected="selected"]')
    prim_pat_dob = InputElement('//input[@id="subBirthDate"]')
    prim_pat_relation = SelectElement('//select[@id="subscriberRelationInfoDropdown"]//option[@selected="selected"]')
    prim_cancel_ins = ButtonElement('//button[@id="btnCancelInsPlan"]')
    prim_modal_close = ButtonElement('//div[@class="modal-footer"]//button[text()="OK"]')

    verification_element = edit_insurance_iframe
