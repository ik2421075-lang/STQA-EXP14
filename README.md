# COVID-19 Information and Awareness Portal

### Software Testing & Quality Assurance (STQA) Mini-Project — Experiment 14
**Course:** BE Computer Engineering (Semester 7)  
**Evaluator:** Bhushan Gholap Sir  
**Project Team:**  
- Payal Sahare (Roll No. 115)  
- Lavanya Pillai (Roll No. 105)  
- Gauri Rajput (Roll No. 110)  

---

## 1. Project Overview & Objective

The **COVID-19 Information and Awareness Portal** is a complete, responsive, full-featured web application designed to educate citizens, facilitate COVID-19 diagnostic test registration, track laboratory test reports, monitor real-time state-wise testing statistics, and enable authenticated community discussion.

The application has been engineered to comply with the **IEEE 829-aligned STQA Test Plan & Bug Taxonomy Document**, featuring robust client-side regular expression (Regex) validation and stable DOM identifiers for automated **Selenium WebDriver** testing.

---

## 2. Mandatory Technology Stack

This application is built with **zero external dependencies**, requiring no database setup, no package managers, and no runtime frameworks:

- **HTML5:** Semantic document structure, accessible ARIA attributes, structured form inputs.
- **CSS3:** Custom healthcare-inspired styling (white and light blue color palette, deep navy headings, responsive grid and flexbox layouts, printable PDF report view).
- **Vanilla JavaScript (ES6):** Client-side routing, regex validation engines, session handling, search filtering, dynamic DOM rendering.
- **Browser LocalStorage:** Local persistent data storage for:
  - Registered User Accounts (`covid_portal_users`)
  - Active User Login Sessions (`covid_portal_session`)
  - Diagnostic Test Registrations & Lab Reports (`covid_portal_test_records`)
  - State-wise Surveillance Testing Statistics (`covid_portal_state_stats`)
  - Community Feedback & Discussion Comments (`covid_portal_comments`)
- **Python Built-in HTTP Server:** Single-command local web server (`python -m http.server 8000`).

---

## 3. Quick Start & Execution Instructions

### Step 1: Start the Local HTTP Server
Open your terminal / command prompt in the project root directory and execute:

```bash
python -m http.server 8000
```

### Step 2: Open in Web Browser
Open any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox) and navigate to:

```
http://localhost:8000
```

*Note: The website can also be launched directly by opening `index.html` in any web browser.*

---

## 4. Website Modules & Functional Specifications

### A. Home & Hero Portal
- **Live National Helpline Banner:** National toll-free helpline `1075` and Health Ministry phone `+91-11-23978046`.
- **Navigation Bar:** Responsive sticky navbar with quick links, active link scroll highlighting, mobile hamburger menu, and auth badges.
- **Hero Banner:** Action buttons for booking diagnostic tests, checking reports, and symptom assessment.
- **Milestone Counters:** 54,000+ tests conducted, 98.8% recovery rate, 2.2 Billion+ doses administered.

### B. Medical Information & Symptoms Module
- **Etiology & Transmission:** Detailed scientific information on SARS-CoV-2 transmission vectors (droplets, aerosols, fomites).
- **Categorized Symptoms:**
  - *Most Common:* High fever, persistent dry cough, fatigue, loss of taste or smell.
  - *Less Common:* Sore throat, headache, muscle aches, gastrointestinal distress.
  - *Critical Red Flags:* Shortness of breath (dyspnea), persistent chest pressure, hypoxia ($SpO_2 < 94\%$) with emergency dial alerts.
- **Interactive Symptom Risk Checker:** Checkbox self-assessment that evaluates risk tier (Low, Moderate, Emergency) and recommends immediate actions.

### C. Portal Search Engine (Module C)
- Real-time client-side search indexed across all portal resources.
- Filters keywords such as `fever`, `RT-PCR`, `vaccine`, `mask`, `helpline`, and `booster`.
- Highlights result matches with quick navigation jump buttons.
- Shows a helpful "No matching information found" fallback for unknown search queries.

### D. User Registration & Authentication (MOD-01)
- **Registration Form (`#register-modal`):**
  - Name, Email, Password, and Confirm Password fields.
  - Email format validation using regular expressions.
  - Enforces minimum 6-character password security.
  - Prevents duplicate registration for already existing emails.
  - Persists accounts to LocalStorage (`covid_portal_users`).
- **Login Form (`#login-modal`):**
  - Authenticates registered credentials.
  - Creates and manages active sessions in LocalStorage (`covid_portal_session`).
  - Updates navigation to display `Welcome, <Name>` with a `Logout` button.
  - Automatically unlocks the Community Comments module.
- **Admin Portal (`#admin-modal`):**
  - Administrative login for testing center management (Default: `admin` / `admin123`).

### E. Regular Expression Input Validation Engine (MOD-02)
Form inputs are strictly validated using the regular expressions documented in Section 3.4 of the STQA Test Plan:

| Field | Regular Expression Pattern | Validation Rule & Example |
| :--- | :--- | :--- |
| **Email** | `^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$` | Valid: `anita.sharma@example.com` |
| **Phone Number** | `^[6-9][0-9]{9}$` | Exactly 10 digits starting with 6–9. Valid: `9876543210` |
| **Date of Birth** | `^(19\|20)[0-9]{2}-(0[1-9]\|1[0-2])-(0[1-9]\|[12][0-9]\|3[01])$` | `YYYY-MM-DD` between 1900–2099; future dates rejected. |
| **Aadhaar Number** | `^[2-9][0-9]{11}$` | 12 digits, first digit 2–9. Valid: `234567890123` |
| **PAN Card** | `^[A-Z]{5}[0-9]{4}[A-Z]$` | 5 uppercase letters, 4 digits, 1 uppercase letter. Valid: `ABCDE1234F` |
| **Voter ID** | `^[A-Z]{3}[0-9]{7}$` | 3 uppercase letters, 7 digits. Valid: `ABC1234567` |
| **Slot Date-Time** | `^[0-9]{4}-(0[1-9]\|1[0-2])-(0[1-9]\|[12][0-9]\|3[01])T([01][0-9]\|2[0-3]):[0-5][0-9]$` | Appointment date-time must be scheduled in the future. |

### F. COVID-19 Diagnostic Test Registration (MOD-03)
- Corresponds to `new-user-testing.php` in the test report.
- Collects Patient Name, Phone, DOB, Govt ID Type & Number, State, Address, Test Type (RT-PCR, Rapid Antigen, Antibody), and Slot Date-Time.
- Prevents duplicate appointment bookings on the same date for the same mobile number.
- Generates a unique tracking Order ID (e.g. `ORD-8492`) and immediately updates the State-Wise Testing Dashboard.

### G. Search & Patient Test Report (MOD-04)
- Corresponds to `patient-search-report.php` in the test report.
- Searches by Patient Name, 10-digit Mobile Number (`9876543210`), or Order ID (`ORD-1001`).
- Displays an official NABL-accredited diagnostic report card with clinical findings (Negative/Positive), collection date, and patient demographics.
- Offers **Print Report** and **Download Report (.PDF)** actions.

### H. State-Wise Testing Dashboard (MOD-05)
- Tabular dashboard tracking testing statistics across Maharashtra, Delhi, Uttar Pradesh, Bihar, Karnataka, Tamil Nadu, Gujarat, and West Bengal.
- Synchronized dynamically with test submissions.

### I. Community Comments & Discussion (MOD-06)
- Allows logged-in users to share experiences and ask questions.
- Rejects blank or empty comments.
- **XSS Protection:** Escapes all HTML and script characters (e.g., `<script>alert(1)</script>` or `<b>x</b>`) to prevent malicious script injection.
- Displays author name and formatted timestamp.
- **Author-Only Deletion:** Delete button is rendered only for comments authored by the currently logged-in user.

---

## 5. Stable Element Locators for Selenium WebDriver Automation

All interactive elements have unique, stable IDs and names to ensure compatibility with Selenium test scripts:

| Module / Action | DOM Element ID | HTML Tag | Description |
| :--- | :--- | :--- | :--- |
| **Nav: Home** | `nav-home` | `<a>` | Link to `#home` |
| **Nav: Symptoms** | `nav-symptoms` | `<a>` | Link to `#symptoms` |
| **Nav: Book Test** | `nav-test-reg` | `<a>` | Link to `#test-registration` |
| **Nav: Search Report** | `nav-report-search` | `<a>` | Link to `#report-search` |
| **Nav: Login** | `nav-login` | `<button>` | Opens Login Modal |
| **Nav: Register** | `nav-register` | `<button>` | Opens Registration Modal |
| **Auth: Display Name**| `user-display-name` | `<span>` | Displays logged-in greeting |
| **Auth: Logout** | `logout-button` | `<button>` | Logs out current session |
| **Reg: Name** | `register-name` | `<input>` | Full Name input |
| **Reg: Email** | `register-email` | `<input>` | Email input |
| **Reg: Password** | `register-password` | `<input>` | Password input |
| **Reg: Confirm Pass** | `register-confirm-password` | `<input>` | Confirm Password input |
| **Reg: Submit** | `register-submit` | `<button>` | Registration submit button |
| **Reg: Message** | `register-msg` | `<div>` | Alert box for validation messages |
| **Login: Email** | `login-email` | `<input>` | Email login input |
| **Login: Password** | `login-password` | `<input>` | Password login input |
| **Login: Submit** | `login-submit` | `<button>` | Login submit button |
| **Login: Message** | `login-msg` | `<div>` | Alert box for login messages |
| **Test Reg: Name** | `patient-name` | `<input>` | Test patient full name |
| **Test Reg: Phone** | `patient-phone` | `<input>` | 10-digit mobile number |
| **Test Reg: DOB** | `patient-dob` | `<input>` | Date of birth |
| **Test Reg: ID Type** | `govt-id-type` | `<select>` | Govt ID Type dropdown |
| **Test Reg: ID Num** | `govt-id-num` | `<input>` | Govt ID Number |
| **Test Reg: State** | `patient-state` | `<select>` | State selection dropdown |
| **Test Reg: Address** | `patient-address` | `<textarea>`| Patient address |
| **Test Reg: Type** | `test-type` | `<select>` | Diagnostic test type |
| **Test Reg: Slot** | `patient-slot` | `<input>` | Date-time appointment slot |
| **Test Reg: Submit** | `test-reg-submit` | `<button>` | Test registration submit button |
| **Test Reg: Message**| `test-reg-msg` | `<div>` | Success/error message alert |
| **Report: Search In** | `report-search-input` | `<input>` | Mobile / Order ID input |
| **Report: Search Btn**| `report-search-btn` | `<button>` | Search report trigger button |
| **Report: Card** | `report-result-card` | `<div>` | Diagnostic report container |
| **Report: Download** | `download-report-btn` | `<button>` | Download PDF report button |
| **Portal: Search In** | `search-input` | `<input>` | Knowledge base search input |
| **Portal: Search Btn**| `search-button` | `<button>` | Knowledge search button |
| **Portal: Clear Btn** | `search-clear` | `<button>` | Clear search input |
| **Portal: Results** | `search-results` | `<div>` | Search matches container |
| **Comment: Input** | `comment-input` | `<textarea>`| Community comment text |
| **Comment: Submit** | `comment-submit` | `<button>` | Post comment button |
| **Comment: Message** | `comment-msg` | `<div>` | Comment alert box |
| **Comment: List** | `comments-list` | `<div>` | List of community comments |

---

## 6. Pre-Configured Test Data for Evaluation

| User / Test Role | Identifier (Email / Phone / Order) | Password / Govt ID | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **Pre-Registered User** | `anita.sharma@example.com` | `password123` | Login succeeds; unlocks comments module. |
| **Test Report Search (Phone)** | `9876543210` | PAN `ABCDE1234F` | Retrieves Anita Sharma RT-PCR Negative report. |
| **Test Report Search (Order)** | `ORD-1001` | Order ID lookup | Displays Report #ORD-1001 immediately. |
| **Positive Test Record** | `9765432109` | Voter ID `ABC1234567` | Retrieves Priya Patel RT-PCR Positive report. |
| **Negative Search Query** | `9123456780` / `000000` | — | Displays "No Patient Report Found" alert. |
| **Admin Portal** | `admin` | `admin123` | Authenticates administrator access. |

---

## 7. IEEE 829 Bug Taxonomy Classification Reference

This application's error handling maps directly to the test plan's bug taxonomy:
- **CAT-FUN (Functional):** Prevents login with non-existent credentials; rejects unregistered report lookups cleanly.
- **CAT-VAL (Validation & Boundary):** Prevents submissions failing email, phone, DOB, Aadhaar, PAN, Voter ID, and slot date-time regex rules.
- **CAT-UI (User Interface & Layout):** Responsive across standard 1366 × 768 desktop, 1024px tablet, and 480px mobile viewports.
- **CAT-NAV (Navigation & Routing):** Smooth scroll navigation with hash targets and escape key modal dismissal.
- **CAT-SEC (Security & Session):** HTML tag sanitization against XSS scripting in comments; LocalStorage session encapsulation.

---

## 8. Academic Submission Note
*This software was prepared as part of the BE Computer Engineering Semester 7 Software Testing & Quality Assurance mini-project curriculum for Experiment 14.*
