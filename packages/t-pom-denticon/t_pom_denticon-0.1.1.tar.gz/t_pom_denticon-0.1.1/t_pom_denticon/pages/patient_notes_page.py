"""Generic Patient Notes page for web app."""
from t_page_object.base_page import BasePage
from t_page_object.elements.button_element import ButtonElement
from t_page_object.elements.iframe_element import IFrameElement

from t_pom_denticon.elements.select_element import SelectElement


class PatientNotesPage(BasePage):
    """Page class containing elements specific patient notes interface to upload pdf."""

    url = "https://az2.denticon.com/ASPX/Patients/AdvancedNotes.aspx"

    notes_iframe = IFrameElement('//iframe[@id="NotesIframe"]')
    add_new_note_button = ButtonElement('//button[@id="btnAddNewNotes"]')
    choose_file_button = ButtonElement('//button[@id="chooseFileBtn"]')
    select_upload_file = SelectElement('//select[@id="noteTypeOption"]')
    upload_file_path = '//input[@id="uploadedFile"]'
    save_note_button = ButtonElement('//button[@id="saveNote"]')

    verification_element = notes_iframe
