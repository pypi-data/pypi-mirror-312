# T_pom_envolve 📦

> **A Python package for Envolve POM approach
            when interacting with web pages and their elements.**

## 📑 Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [API Documentation](#api-documentation)
- [License](#license)

## Overview
This package provides Envolve portal Base class, web pages and web elements.
            
There are also usable web elements that have commonly used methods built in.

## Installation
```bash
pip install t-pom-envolve
```

## Usage Example
For detailed examples, please refer to our
            [quick start page](https://www.notion.so/thoughtfulautomation/T-POM-Envolve-150f43a78fa48051acadc531a4675534).

### 
## API Documentation

---

## Elements
### Module: `t_pom_envolve.elements`

_Module for t_envolve specific methods._

### Module: `t_pom_envolve.elements.datetime_element`

_Datetime element module._

- **Class:** `DateTimeElement`
  > Class for Datetime element model.
  - **Method:** `select_date`
    > Inputs a date into a date field.
### Module: `t_pom_envolve.elements.select_element`

_Select element module._

- **Class:** `SelectElement`
  > Class to Select element model.
  - **Method:** `get_selected_option`
    > Gets the selected option.
  - **Method:** `select_options`
    > Selects a list of options from a dropdown menu.
### Module: `t_pom_envolve.elements.table_row_element`

_Table Row element module._

- **Class:** `TableRowElement`
  > Class for TextElement element model.
  - **Method:** `get_row_values`
    > Get Element value.
### Module: `t_pom_envolve.elements.text_element`

_TextElement element module._

- **Class:** `TextElement`
  > Class for TextElement element model.
  - **Method:** `get_element_text`
    > Get Element value.

---

## Exceptions
### Module: `t_pom_envolve.exceptions`

_Module Description: This module defines custom exceptions for use within the application.

These exceptions provide more specific error handling and messaging for various failure scenarios,
improving the robustness and clarity of the code.
_

- **Class:** `MissingPatientInformationException`
  > Invalid Conversation Default Exception .
- **Class:** `PatientNotEligibleException`
  > Patient Not Found Exception.
- **Class:** `PatientNotFoundException`
  > Patient Not Found Exception.
- **Class:** `SessionExpiredException`
  > Session Expire Exception.

---

## Pages
### Module: `t_pom_envolve.pages`

_Page modules for Envolve._

### Module: `t_pom_envolve.pages.login_page`

_Generic login page for web app._

- **Class:** `LoginPage`
  > Page class containing elements specific to a login interface.
### Module: `t_pom_envolve.pages.patient_eligibility_page`

_Generic patient eligibility page for web app._

- **Class:** `PatientEligibilityPage`
  > Page class containing elements specific to a patient eligibility.

---

## T_envolve
### Module: `t_pom_envolve.t_envolve`

_Generic base class for web app._

- **Class:** `TEnvolve`
  > Main application class managing pages and providing direct access to Selenium.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
