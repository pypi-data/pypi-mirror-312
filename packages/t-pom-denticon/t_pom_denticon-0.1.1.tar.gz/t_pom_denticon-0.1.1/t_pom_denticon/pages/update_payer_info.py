"""Generic Update Payer Information for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement

from t_pom_denticon.elements.datetime_element import DateTimeElement
from t_pom_denticon.elements.select_element import SelectElement


class UpdatePayerInformation(BasePage):
    """Page class containing elements specific to Update Payer Information interface."""

    url = "https://az2.denticon.com/"
    prim_pat_update_status_btn = ButtonElement('//button[@id="btnUpdateStatus"]')
    prim_pat_effective_date = DateTimeElement('//input[@id="subEffectiveDate"]')
    prim_pat_term_date = DateTimeElement('//input[@id="subTermDate"]')
    prim_pat_eligibility_status_dropdown = SelectElement('//select[@id="eligibilityStatDropDown"]')
    prim_pat_status_save_button = ButtonElement('//button[@id="btnUpdateEligbilityStat"]')
    close_button = ButtonElement(
        '//button[@class="btn btn-secondary btn-sm margin-left-5 btn-close-update-elig-stat"]',
    )
    verification_element = prim_pat_update_status_btn
