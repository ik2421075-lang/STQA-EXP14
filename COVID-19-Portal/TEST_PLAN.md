# IEEE 829 Test Plan — COVID-19 Information & Awareness Portal

**Project:** Quality Assurance & Automated Testing of COVID-19 Awareness Portal  
**Course:** BE Computer Engineering (Semester 7) — Software Testing & Quality Assurance (STQA)  
**Experiment:** Experiment 14  
**Evaluator:** Bhushan Gholap Sir  
**Project Team:**  
- Payal Sahare (Roll No. 115)  
- Lavanya Pillai (Roll No. 105)  
- Gauri Rajput (Roll No. 110)  
**Document Identifier:** TP-STQA-EXP14-V1.0  
**Date:** November 2026  

---

## 1. Introduction & Executive Summary

This document specifies the concise, IEEE 829-aligned **Test Plan** for the **COVID-19 Information and Awareness Portal**. The platform provides epidemiological updates, symptom guidance, prevention protocols, diagnostic test registration, report search, state-wise analytics, and community discussions.

The quality assurance initiative applies **Python 3.11**, **Selenium WebDriver 4**, and **Google Chrome** to automate functional regression testing across all modules, verifying strict regular-expression input validations, session encapsulation, and responsive cross-viewport layouts.

---

## 2. Platform Architecture & Test Environment

### 2.1 Hardware Requirements
- **Processor:** Intel Core i3 / i5 or AMD Ryzen 5 or higher
- **RAM:** Minimum 4 GB (8 GB recommended)
- **Disk Storage:** Minimum 1 GB available storage
- **Display Resolution:** 1366 × 768 (Standard laptop baseline)

### 2.2 Software & Platform Specifications
- **Operating System:** Microsoft Windows 10 / Windows 11
- **Target Browser:** Google Chrome v129+ with matching ChromeDriver / Selenium Manager
- **Test Automation Layer:** Python 3.11 with Selenium WebDriver 4 (`selenium>=4.20.0`), `unittest`, `pytest`
- **Frontend Stack:** HTML5, CSS3, Vanilla JavaScript (ES6)
- **Data Persistence:** Browser LocalStorage (`covid_portal_users`, `covid_portal_session`, `covid_portal_test_records`, `covid_portal_comments`, `covid_portal_state_stats`)
- **Web Server:** Python built-in HTTP server (`python -m http.server 8000`)

---

## 3. Scope of Testing

### 3.1 Features to be Tested (In Scope)
- **MOD-01: User Registration & Login:** Sign-up validation, password length/confirmation, duplicate email prevention, credential authentication, session persistence, logout, admin portal.
- **MOD-02: Regular Expression Input Validation:** Email regex (`^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$`), 10-digit mobile (`^[6-9][0-9]{9}$`), DOB (`^(19|20)[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$`), Aadhaar, PAN, Voter ID, and future slot date-time.
- **MOD-03: COVID-19 Test Registration:** Booking RT-PCR, Rapid Antigen, and Antibody tests, mandatory field enforcement, date boundary checks, order ID generation.
- **MOD-04: Search & Patient Test Report:** Searching by phone or order number, displaying NABL-accredited diagnostic report card, unknown record handling.
- **MOD-05: State-Wise Testing Dashboard:** Surveillance metrics across 8 states, dynamic count synchronization.
- **MOD-06: Comments & Discussion:** Restricting comments to logged-in users, empty comment rejection, HTML/script escaping (XSS mitigation), author-only comment deletion.
- **MOD-07: Responsiveness & Navigation:** Navbar links, target section routing, modal ESC dismissal, mobile hamburger navigation at 480px.

### 3.2 Features Not to be Tested (Out of Scope)
- Third-party payment gateways (Stripe/PayPal).
- External SMS/Email gateway delivery.
- Multi-thousand concurrent user stress/load testing (evaluation target is single-user desktop/lab browser).
- Browsers other than Google Chrome.

---

## 4. Test Strategy & Methodology

```
               +------------------------------------------------+
               |        STQA Test Methodology Framework         |
               +------------------------------------------------+
                                       |
        +------------------------------+------------------------------+
        |                              |                              |
+-------v-------+              +-------v-------+              +-------v-------+
|  Automated    |              |  Regex Form   |              |  Exploratory  |
|  Functional & |              |  Validation   |              |  Testing &    |
|  Regression   |              |  (BVA & EP)   |              |  Risk Charter |
+-------+-------+              +-------+-------+              +-------+-------+
        |                              |                              |
        v                              v                              v
Selenium WebDriver              Equivalence Classes &          Timeboxed tours
Chrome Headless/GUI             Regex Pattern Matching         Edge cases, XSS
38 Automated Tests              Boundary Value Analysis        Viewport resize
```

1. **Automated Functional & Regression Testing:**
   - Modular test scripts organized in `tests/`: `test_registration.py`, `test_login.py`, `test_search.py`, `test_comments.py`, `test_navigation.py`.
   - Coordinated master runner `regression_tests.py` that executes all suites, records execution timings, and produces self-contained HTML reports.
2. **Explicit Waits & Synchronization:**
   - Uses `WebDriverWait` with `expected_conditions` (`visibility_of_element_located`, `element_to_be_clickable`) to eliminate race conditions.
3. **Automated Screenshot on Failure:**
   - Any test failure triggers automatic capture of the browser viewport to `tests/screenshots/<test_name>_<timestamp>.png`.
4. **Equivalence Partitioning & Boundary Value Analysis:**
   - Valid vs. invalid classes for emails, phone numbers, passwords, dates, and government IDs.

---

## 5. Requirements Traceability Matrix (RTM)

| Req ID | Module | Feature Under Test | Automated Test Script | Method / Test ID | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Registration | New user registration | `test_registration.py` | `test_06_registration_successful` | Form accepted, stored in LocalStorage, transitions to login. |
| **REQ-02** | Registration | Validation checks | `test_registration.py` | `test_02_empty_fields`, `test_04_short_pwd` | Mandatory fields flagged; passwords < 6 chars rejected. |
| **REQ-03** | Login | User authentication | `test_login.py` | `test_06_login_successful` | Session created, greeting displayed, logout button active. |
| **REQ-04** | Login | Invalid credentials | `test_login.py` | `test_04_unregistered`, `test_05_wrong_pwd` | Rejection message displayed without crash. |
| **REQ-05** | Report Search| Search registered phone | `test_search.py` | `test_06_report_search_phone` | Diagnostic report card displayed with matching patient details. |
| **REQ-06** | Report Search| Unregistered record | `test_search.py` | `test_08_report_unregistered` | Displays "No Patient Report Found" alert. |
| **REQ-07** | Input Regex | Email format regex | `test_registration.py` | `test_03_invalid_email_regex` | Rejects emails without `@` or with invalid domain. |
| **REQ-08** | Input Regex | Phone number regex | `test_registration.py` | `test_09_invalid_phone_regex` | Rejects numbers < 10 digits or starting with digits < 6. |
| **REQ-09** | Input Regex | Slot date-time regex | `test_registration.py` | `test_08_covid_test_registration` | Validates `YYYY-MM-DDTHH:MM` format and future timing. |
| **REQ-10** | Input Regex | Date of Birth regex | `test_registration.py` | `test_08_covid_test_registration` | Validates `YYYY-MM-DD` between 1900–2099; rejects future dates. |
| **REQ-11** | Input Regex | Govt ID pattern | `test_registration.py` | `test_08_covid_test_registration` | Validates PAN (`ABCDE1234F`), Aadhaar, or Voter ID patterns. |
| **REQ-12** | Comments | Post & XSS safety | `test_comments.py` | `test_04_post`, `test_05_xss` | Comment rendered; `<script>` tags escaped as plain text. |
| **REQ-13** | Dashboard | State statistics | `test_navigation.py` | `test_02_navbar_targets` | State surveillance table rendered and synchronized. |
| **REQ-14** | Data Rules | Duplicate prevention | `test_registration.py` | `test_07_duplicate_email` | Rejects duplicate email sign-ups with clear error. |
| **REQ-15** | UI / Layout | Responsive viewports | `test_navigation.py` | `test_04_mobile_viewport` | Layout scales to 1366px, 1024px, and 480px with hamburger. |
| **REQ-16** | Usability | Navigation & modals | `test_navigation.py` | `test_01_all_links`, `test_05_escape_key` | Links resolve correctly; modals close on ESC key. |

---

## 6. Entry, Suspension, and Exit Criteria

### 6.1 Entry Criteria
- Web application files (`index.html`, `style.css`, `script.js`) available and accessible locally at `http://localhost:8000`.
- Python 3.11 environment with Selenium WebDriver installed (`pip install -r tests/requirements.txt`).
- Chrome browser v129+ installed with operational ChromeDriver.

### 6.2 Suspension Criteria
- Local HTTP server becomes unreachable or crashes during testing.
- Fatal browser session initialization errors preventing WebDriver from launching.
- Critical defect (S1 Blocker) preventing page load or basic DOM interaction.

### 6.3 Exit Criteria
- 100% of planned automated tests (38/38) executed.
- Zero unclassified or unresolved Blocker (S1) or Major (S2) defects.
- All regular expression boundary tests pass.
- HTML and Markdown test execution reports generated.
