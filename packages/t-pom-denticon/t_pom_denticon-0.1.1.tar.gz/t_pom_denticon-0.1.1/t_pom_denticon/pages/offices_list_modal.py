"""Generic Office List Modal page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement

from t_pom_denticon.elements.select_element import SelectElement


class OfficesListModal(BasePage):
    """Page class containing elements specific to Office List Modal interface."""

    url = "https://az2.denticon.com/"
    select_office_location = SelectElement('//select[@id="availabelist"]')
    button_to_right = ButtonElement('//input[@id="btnRight"]')
    selected_office_location = SelectElement('//select[@id="selectedlist"]')
    button_to_left = ButtonElement('//input[@id="btnLeft"]')
    apply_button = ButtonElement('//button[text()="apply"]')

    verification_element = select_office_location
