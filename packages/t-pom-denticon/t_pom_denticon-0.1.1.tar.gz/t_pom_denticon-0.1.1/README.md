# T_pom_denticon 📦

> **A Python package for Denticon POM approach
            when interacting with web pages and their elements.**

## 📑 Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [API Documentation](#api-documentation)
- [License](#license)

## Overview
This package provides Denticon portal Base class, web pages and web elements.
            
There are also usable web elements that have commonly used methods built in.

## Installation
```bash
pip install t-pom-denticon
```

## Usage Example
For detailed examples, please refer to our
            [quick start page](https://www.notion.so/thoughtfulautomation/T-POM-Denticon-14df43a78fa4803ea633e9a0d6e8297f).

### 
## API Documentation

---

## Elements
### Module: `t_pom_denticon.elements`

_Module for all web app elements._

### Module: `t_pom_denticon.elements.datetime_element`

_Datetime element module._

- **Class:** `DateTimeElement`
  > Class for Datetime element model.
  - **Method:** `select_date`
    > Inputs a date into a date field.
### Module: `t_pom_denticon.elements.select_element`

_Select element module._

- **Class:** `SelectElement`
  > Class to Select element model.
  - **Method:** `get_selected_option`
    > Gets the selected option.
  - **Method:** `select_options`
    > Selects a list of options from src.a dropdown menu.
### Module: `t_pom_denticon.elements.table_row_element`

_Table Row element module._

- **Class:** `TableRowElement`
  > Class for TextElement element model.
  - **Method:** `get_row_values`
    > Get Element value.
### Module: `t_pom_denticon.elements.text_element`

_TextElement element module._

- **Class:** `TextElement`
  > Class for TextElement element model.
  - **Method:** `get_element_text`
    > Get Element value.

---

## Pages
### Module: `t_pom_denticon.pages`

_Page modules for Denticon._

### Module: `t_pom_denticon.pages.login_page`

_Generic login page for web app._

- **Class:** `LoginPage`
  > Page class containing elements specific to a login interface.
### Module: `t_pom_denticon.pages.offices_list_modal`

_Generic Office List Modal page for web app._

- **Class:** `OfficesListModal`
  > Page class containing elements specific to Office List Modal interface.
### Module: `t_pom_denticon.pages.patient_notes_page`

_Generic Patient Notes page for web app._

- **Class:** `PatientNotesPage`
  > Page class containing elements specific patient notes interface to upload pdf.
### Module: `t_pom_denticon.pages.patient_overview_info_page`

_Generic Patient Overview Info Page for web app._

- **Class:** `PatientOverviewInfoPage`
  > Page class containing elements specific to a Patient Overview Info Page interface.
### Module: `t_pom_denticon.pages.primary_patient_info_page`

_Generic Primary Patient Information Page for web app._

- **Class:** `PrimaryPatientInformationPage`
  > Page class containing elements specific to a Primary Patient Information Page interface.
### Module: `t_pom_denticon.pages.report_viewer`

_Generic Report Viewer page for web app._

- **Class:** `ReportViewerPage`
  > Page class containing elements specific to a Report Viewer page interface.
### Module: `t_pom_denticon.pages.retrieve_dps_report_page`

_Generic Retrieve DPS Report page for web app._

- **Class:** `RetrieveDpsReportPage`
  > Page class containing elements specific to a Retrieve DPS Report interface.
### Module: `t_pom_denticon.pages.retrieve_smart_assist_report_page`

_Generic Retrieve Smart Assistant Report page for web app._

- **Class:** `RetrieveSmartAssistReportPage`
  > Page class containing elements specific to a Retrieve Smart Assistant Report interface.
### Module: `t_pom_denticon.pages.secondary_patient_info_page`

_Generic Secondary Patient Information Page for web app._

- **Class:** `SecondaryPatientInformationPage`
  > Page class containing elements specific to a Secondary Patient Information Page interface.
### Module: `t_pom_denticon.pages.update_payer_info`

_Generic Update Payer Information for web app._

- **Class:** `UpdatePayerInformation`
  > Page class containing elements specific to Update Payer Information interface.

---

## T_denticon
### Module: `t_pom_denticon.t_denticon`

_Generic base class for web app._

- **Class:** `TDenticon`
  > Main application class managing pages and providing direct access to Selenium.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
