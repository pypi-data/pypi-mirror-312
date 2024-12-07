# T-Pom-dentalhub

> **A Python package for interacting with DentalHub portal
            and their elements .**

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage Example](#usage-example)
- [API Documentation](#api-documentation)
- [License](#license)

## Overview
This package provides various modules and classes for interacting with dentalhub portal.
            
There are also usable web elements that have commonly used methods built in.

## Installation
```bash
pip install t-pom-dentalhub
```

## Usage Example
For detailed examples, please refer to our
            [quick start page](https://www.notion.so/thoughtfulautomation/T-DentalHub-14cf43a78fa48056b8a9c21f7003f32a).

### 
## API Documentation

---

## Consts
### Module: `t_pom_dentalhub.consts`

_Configuration module for DentalHub._

- **Class:** `CONSTS`
  > Container for any const you require for default on your automation.

---

## Elements
### Module: `t_pom_dentalhub.elements`

_Module for all web app elements._

### Module: `t_pom_dentalhub.elements.table_element`

_Table element module._

- **Class:** `TableElement`
  > Class for table elements.
  - **Method:** `get_summary_table_data`
  - **Method:** `get_table_data`


### Module: `t_pom_dentalhub.elements.text_element`

_Text element module._

- **Class:** `TextElement`
  > Class for input element model.

---

## Pages

### Module: `t_pom_dentalhub.pages`

_Page modules for DentalHub._

### Module: `t_pom_dentalhub.pages.login_page`

_Login page for DentalHub._

- **Class:** `LoginPage`
  > Page class containing elements specific to login on DentalHub.

### Module: `t_pom_dentalhub.pages.dashboard_page`

_Dashboard page for Dentalhub._

- **Class:** `DashboardPage`
  > Page class containing elements specific to a dashboard interface.


### Module: `t_pom_dentalhub.pages.patient_insurance_page`

_Patient insurance form._

- **Class:** `PatientInsurancePage`
  > Page class containing elements specific to a patient insurance interface.

### Module: `t_pom_dentalhub.pages.practitioner_location_page`

_Practitioner location page._

- **Class:** `PractitionerLocationPage`
  > Page class containing elements specific to a practitioner and location interface.

### Module: `t_pom_dentalhub.pages.eligibility_selected_insurance_page`

_Page to selected insurance interface._

- **Class:** `EligibilitySelectedInsurancePage`
  > Page class containing elements specific to selected insurance interface.

### Module: `t_pom_dentalhub.pages.eligibility_check_results_page`

_Page to check the results of eligibility._

- **Class:** `EligibilityCheckResultsPage`
  > Page class containing elements specific to eligibility check result interface.

### Module: `t_pom_dentalhub.pages.service_history_page`

_Service history page._

- **Class:** `ServiceHistoryPage`
  > Page class containing elements specific to service history interface.

### Module: `t_pom_dentalhub.pages.multi_factor_authentication_page`

_Multi Factor Authentication Page._

- **Class:** `MultiFactorAuthenticationPage`
  > Page class containing multi factor authentication.

---

## t_pom_dentalhub
### Module: `t_pom_dentalhub.t_pom_dentalhub`

_Base class for DentalHub._

- **Class:** `TDentalHub`
  > Main application class managing pages and providing direct access to Selenium.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.