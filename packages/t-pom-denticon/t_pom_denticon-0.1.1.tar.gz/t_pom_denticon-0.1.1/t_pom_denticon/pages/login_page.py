"""Generic login page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.input_element import InputElement


class LoginPage(BasePage):
    """Page class containing elements specific to a login interface."""

    url = "https://az2.denticon.com/aspx/home/login.aspx?STO=1"
    user_id_input = InputElement("//input[@name='username']")
    continue_button = ButtonElement("//a[@id='btnLogin']")
    password_input = InputElement("//input[@name='txtPassword']")
    sign_in_button = ButtonElement("//a[@id='aLogin']")
    verification_element = user_id_input
