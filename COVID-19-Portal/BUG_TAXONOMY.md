# Bug Taxonomy & Defect Management Guide

**Course:** BE Computer Engineering (Semester 7) — Software Testing & Quality Assurance (STQA)  
**Project:** COVID-19 Information & Awareness Portal (Experiment 14)  
**Evaluator:** Bhushan Gholap Sir  
**Document Identifier:** BT-STQA-EXP14-V1.0  

---

## 1. Defect Classification by Category

The software testing lifecycle of the COVID-19 Information Website classifies all identified issues into five standardized categories:

```
                          +------------------------------------------------+
                          |           Bug Taxonomy Classification          |
                          +------------------------------------------------+
                                                  |
        +------------------+------------------+---+------------------+------------------+
        |                  |                  |                      |                  |
+-------v-------+  +-------v-------+  +-------v-------+      +-------v-------+  +-------v-------+
|    CAT-FUN    |  |    CAT-VAL    |  |    CAT-UI     |      |    CAT-NAV    |  |    CAT-SEC    |
|  Functional   |  |  Validation   |  |     User      |      | Navigation &  |  |  Security &   |
|    Defects    |  |  & Boundary   |  |   Interface   |      |    Routing    |  |    Session    |
+---------------+  +---------------+  +---------------+      +---------------+  +---------------+
```

### 1.1 CAT-FUN: Functional Defects
Logic failures where application features behave counter to written requirements.
- *Examples:* User registration failing despite valid inputs; login rejecting correct passwords; search report returning the incorrect patient record; state-wise test tally failing to increment after appointment registration.

### 1.2 CAT-VAL: Validation & Boundary Defects
Failures of input form controls or regular expressions to reject malformed, empty, or out-of-boundary data.
- *Examples:* Form accepting an email without an `@` symbol or domain (`anita.example.com`); accepting a 9-digit or 11-digit phone number; accepting past appointment slots; allowing a future date for Date of Birth; accepting malformed PAN or Aadhaar strings.

### 1.3 CAT-UI: User Interface & Layout Defects
Visual anomalies, broken responsive behavior, misaligned form controls, or overlapping UI components.
- *Examples:* Button overflow at 1366 × 768 or 480px viewport width; modal dialogs clipped on mobile screens; missing contrast badges; overlapping table columns in state dashboard.

### 1.4 CAT-NAV: Navigation & Routing Defects
Broken hyperlinks, unresponsive buttons, incorrect jump anchors, or unhandled modal dismissal events.
- *Examples:* Sticky navbar links not scrolling to section anchors; mobile hamburger menu failing to toggle; modal dialog not dismissing upon pressing the `Escape` key.

### 1.5 CAT-SEC: Security & Session Defects
Failures related to data sanitization, unauthorized actions, or session persistence vulnerabilities.
- *Examples:* Cross-Site Scripting (XSS) execution when `<script>alert(1)</script>` is entered in the comment textarea; unauthenticated guest users being able to post comments; users being allowed to delete comments authored by other individuals.

---

## 2. Defect Severity Hierarchy

Severity measures the technical and operational impact of an issue on system integrity and test execution:

| Severity Level | Classification | Impact Description | Concrete Example |
| :--- | :--- | :--- | :--- |
| **S1** | **Blocker / Critical** | Complete system failure, unrecoverable loop, or core test automation blocked with no workaround. | Web server fails to boot; fatal JavaScript syntax error crashes DOM loading; registration modal fails to render. |
| **S2** | **Major** | Core business functionality compromised, incorrect data returned, or regex pattern allows invalid data, but a workaround exists. | Phone number regex accepts 9-digit number; diagnostic report returns wrong patient status; duplicate email registered. |
| **S3** | **Moderate** | Non-critical feature fails, validation messaging is misleading, or cosmetic flaw affects user experience. | Error alert displays generic text instead of specific regex hint; clear search button does not hide immediately. |
| **S4** | **Minor / Trivial** | Minor cosmetic, styling, or documentation issue with zero functional impairment. | 2px alignment gap on mobile view; missing icon tooltip; minor typo in disclaimer. |

---

## 3. Defect Priority Scale

Priority dictates the scheduling urgency of resolving a bug from a project delivery standpoint:

| Priority | Urgency Level | Target Resolution SLA | Criteria |
| :--- | :--- | :--- | :--- |
| **P1** | **Immediate** | Resolve within current test cycle before further automation can proceed. | Blocks test execution or compromises security (e.g. raw XSS script execution). |
| **P2** | **High** | Must be fixed before the release milestone or laboratory submission. | Core functional defect, registration failure, or broken regex validation rule. |
| **P3** | **Medium** | Fix in scheduled maintenance or secondary iteration. | Non-blocking UI glitch or minor responsiveness issue. |
| **P4** | **Low** | Deferred or fixed if time permits. | Enhancement suggestion or trivial styling variation. |

---

## 4. Defect Lifecycle Workflow

```
       +------------+
       |    NEW     | <--- Bug discovered during automated/exploratory test
       +-----+------+
             |
             v
       +------------+       Out of scope /
       |    OPEN    +-------------------------> [ DEFERRED ]
       +-----+------+       Duplicate
             |
             v
       +------------+
       |  ASSIGNED  | <--- Assigned to development team
       +-----+------+
             |
             v
       +------------+
       |   FIXED    | <--- Code change deployed to test environment
       +-----+------+
             |
             v
       +------------+
       |   RETEST   | <--- Regression suite re-executed
       +--+------+--+
          |      |
Still     |      | Verified
defect    |      | fixed
          v      v
     [ REOPENED ] [ CLOSED ]
```

---

## 5. Actual Defect Log (Discovered During Testing & Fixed)

The following defect entries document actual issues identified during the implementation and execution of the automated test suite, triaged using this taxonomy:

### Defect Entry 1: Comment Form HTML5 Native Validation Interception
- **Defect ID:** DEF-01
- **Taxonomy Code:** CAT-VAL-001
- **Severity:** S3 (Moderate) | **Priority:** P2 (High)
- **Module:** MOD-06 (Comments Module)
- **Description:** When the user clicked "Post Comment" with an empty textarea, the browser displayed a native tooltip due to the `required` attribute on `<textarea>`, preventing the custom JavaScript validation function `handleCommentSubmit` from executing and populating `<div id="comment-msg">`.
- **Root Cause:** Form element `<form id="comment-post-form">` lacked the `novalidate` attribute.
- **Resolution:** Added `novalidate` attribute to `<form id="comment-post-form" novalidate>`.
- **Status:** **CLOSED (Verified via `TestComments.test_03_comment_empty_validation`)**

### Defect Entry 2: Selenium HTML5 Date-Input Keystroke Formatting
- **Defect ID:** DEF-02
- **Taxonomy Code:** CAT-VAL-002
- **Severity:** S3 (Moderate) | **Priority:** P2 (High)
- **Module:** MOD-03 (COVID-19 Test Registration)
- **Description:** Sending string `"1996-05-12"` via Selenium `send_keys` to `<input type="date" id="patient-dob">` failed on Windows Chrome due to OS locale date format differences (`dd-mm-yyyy`), causing the DOM `.value` to remain empty or rejected by the `YYYY-MM-DD` regex.
- **Root Cause:** Browser-level date picker input masking interfered with raw character streaming.
- **Resolution:** Standardized automated test scripts to set the standard ISO date `.value = '1996-05-12'` directly via JavaScript.
- **Status:** **CLOSED (Verified via `TestRegistration.test_08_covid_test_registration_valid_submission`)**

### Defect Entry 3: Unittest Python 3.11 `_Outcome` Attribute Incompatibility
- **Defect ID:** DEF-03
- **Taxonomy Code:** CAT-FUN-003
- **Severity:** S2 (Major) | **Priority:** P1 (Immediate)
- **Module:** Test Automation Framework (`base_test.py`)
- **Description:** In Python 3.11, accessing `self._outcome.errors` in `tearDown` threw `AttributeError: '_Outcome' object has no attribute 'errors'`, preventing the regression suite from completing.
- **Root Cause:** Python 3.11 refactored the private `_Outcome` class structure in the standard library `unittest`.
- **Resolution:** Refactored failure screenshot triggering into `DetailedTestResult.addFailure` and `addError` in `regression_tests.py`, decoupling test lifecycle from private unittest internals.
- **Status:** **CLOSED (Verified via `regression_tests.py` 38/38 run)**
