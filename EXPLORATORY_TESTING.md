# Exploratory Testing Charter & Findings Report

**Course:** BE Computer Engineering (Semester 7) — Software Testing & Quality Assurance (STQA)  
**Project:** COVID-19 Information & Awareness Portal (Experiment 14)  
**Evaluator:** Bhushan Gholap Sir  
**Testing Team:** Payal Sahare (115), Lavanya Pillai (105), Gauri Rajput (110)  
**Document Identifier:** ET-STQA-EXP14-V1.0  
**Methodology:** Session-Based Test Management (SBTM) & Heuristic-Driven Exploration  

---

## 1. Overview & Exploratory Framework

While automated regression suites verify that known, specified requirements pass predictably, **exploratory testing** is simultaneous learning, test design, and test execution. It targets unscripted edge cases, subtle timing glitches, unexpected user actions, and boundary vulnerabilities.

### Heuristic Framework Applied: **SFDIPOT**
- **Structure:** HTML5 layout, CSS flexbox/grid containers, modal DOM overlays, LocalStorage keys.
- **Function:** Form validations, regex engines, session management, comment posting, report lookups.
- **Data:** Input strings, edge dates, boundary numbers, malicious script payloads (`<script>`), whitespace strings.
- **Interfaces:** Modal popups, sticky navigation bars, search inputs, responsive hamburger menus.
- **Platform:** Windows 11, Google Chrome v129+, Python 3.11 built-in HTTP server.
- **Operations:** Rapid double-clicking, browser back/refresh buttons, viewport resizing, ESC key dismissal.
- **Time:** Next-day appointment scheduling, session timestamps, async modal transition delays.

---

## 2. Time-Boxed Exploratory Charters

```
+-------------------------------------------------------------------------------------------------+
| Charter 1: Registration Form Regex Stress & Duplicate Ingestion                                 |
+-------------------+-----------------------------------------------------------------------------+
| Timebox           | 45 Minutes                                                                  |
| Mission           | Discover boundary flaws in email regex, password fields, and LocalStorage.  |
| Tours Applied     | Input-Variation Tour, Extreme-Value Tour, Boundary Tour                     |
+-------------------+-----------------------------------------------------------------------------+
```

### Scenarios Explored & Findings:
1. **Case-Insensitive Duplicate Email Check:**
   - *Action:* Registered `test.user@example.com`, then attempted to register `TEST.USER@EXAMPLE.COM`.
   - *Observation:* Correctly blocked. The application normalizes emails using `.toLowerCase()`, preventing case-variant duplicate accounts.
2. **Whitespace-Padded Names:**
   - *Action:* Entered `"   John Doe   "` into full name.
   - *Observation:* Handled properly with `.trim()`. Name was stored cleanly.
3. **Password Minimum Boundary (5 vs 6 characters):**
   - *Action:* Entered 5 characters (`"12345"`). Rejected with `"Password must be at least 6 characters in length."` Entered 6 characters (`"123456"`). Successfully accepted. Boundary strictly respected.
4. **Email Local Part and TLD Variations:**
   - *Action:* Tested `a@b.co` (shortest valid email) $\rightarrow$ Accepted. Tested `a@b` (no TLD) $\rightarrow$ Rejected. Tested `a@@b.com` $\rightarrow$ Rejected. Pattern matches IEEE 829 REQ-07 specification.

---

```
+-------------------------------------------------------------------------------------------------+
| Charter 2: Authentication Session Integrity & Route Guarding                                    |
+-------------------+-----------------------------------------------------------------------------+
| Timebox           | 35 Minutes                                                                  |
| Mission           | Test session lifecycle, browser reload retention, and logout invalidation.   |
| Tours Applied     | Interruption Tour, State-Transition Tour                                    |
+-------------------+-----------------------------------------------------------------------------+
```

### Scenarios Explored & Findings:
1. **Page Reload Session Persistence:**
   - *Action:* Logged in as `anita.sharma@example.com`, verified greeting appeared, then pressed browser `F5` / reload.
   - *Observation:* Session remained intact because credentials were read from `covid_portal_session` in LocalStorage on `DOMContentLoaded`.
2. **Logout Action & Storage Clearance:**
   - *Action:* Clicked `#logout-button`.
   - *Observation:* LocalStorage key `covid_portal_session` was removed immediately, the navigation bar switched to `Login` / `Register`, and the Community Comments module locked automatically.
3. **Modal Backdrop Dismissal:**
   - *Action:* Opened login modal, clicked outside the modal card (on `#login-modal` overlay).
   - *Observation:* Modal smoothly closed without JavaScript errors.

---

```
+-------------------------------------------------------------------------------------------------+
| Charter 3: COVID-19 Test Registration & Date Parsing                                            |
+-------------------+-----------------------------------------------------------------------------+
| Timebox           | 40 Minutes                                                                  |
| Mission           | Probe slot date-time scheduling, DOB constraints, and duplicate appointments|
| Tours Applied     | Boundary Tour, Concurrency Tour                                             |
+-------------------+-----------------------------------------------------------------------------+
```

### Scenarios Explored & Findings:
1. **Past Date-Time Slot Scheduling:**
   - *Action:* Attempted to schedule an RT-PCR test appointment for yesterday's date.
   - *Observation:* Rejection alert displayed: `"Appointment Slot must be scheduled for a future date and time."`
2. **Future Date of Birth:**
   - *Action:* Selected tomorrow's date for Date of Birth (`patient-dob`).
   - *Observation:* Rejection alert displayed: `"Date of Birth cannot be in the future."`
3. **Duplicate Booking on Same Date:**
   - *Action:* Booked appointment for phone `9876543210` on `2026-11-20`. Attempted a second booking for the same mobile on the same date.
   - *Observation:* Successfully intercepted with message: `"A COVID-19 test is already registered for this phone number on 2026-11-20. Duplicate registrations on the same date are not permitted."`
4. **State Dashboard Counter Synchronization:**
   - *Action:* Booked a test for the state of `Maharashtra`. Navigated to `#dashboard`.
   - *Observation:* Total test count for Maharashtra incremented by 1 dynamically.

---

```
+-------------------------------------------------------------------------------------------------+
| Charter 4: Search Engine Ingestion & Malformed Queries                                          |
+-------------------+-----------------------------------------------------------------------------+
| Timebox           | 30 Minutes                                                                  |
| Mission           | Test search indexing with SQL injection payloads, symbols, and empty states. |
| Tours Applied     | Security Tour, Garbage-Input Tour                                           |
+-------------------+-----------------------------------------------------------------------------+
```

### Scenarios Explored & Findings:
1. **SQL Injection String Input:**
   - *Action:* Entered `' OR 1=1 --` into portal search and report search.
   - *Observation:* Handled safely. Because data queries run purely in client-side JavaScript via Array `.filter()` and `.find()`, SQL strings are treated as plain text queries. No crashes occurred; search gracefully displayed `"No Results Found"`.
2. **Case Insensitivity & Multi-Word Queries:**
   - *Action:* Searched `"rt-pcr"`, `"RT-PCR"`, and `"rt pcr"`.
   - *Observation:* All variations successfully retrieved the RT-PCR diagnostic booking topic.
3. **Search Clear Button Lifecycle:**
   - *Action:* Typed `"fever"`, verified clear button (`#search-clear`) became visible, clicked it.
   - *Observation:* Input field emptied, clear button re-hid, and results container closed cleanly.

---

```
+-------------------------------------------------------------------------------------------------+
| Charter 5: Comments Module & Security Vulnerability Probe                                       |
+-------------------+-----------------------------------------------------------------------------+
| Timebox           | 45 Minutes                                                                  |
| Mission           | Attempt Stored Cross-Site Scripting (XSS) and unauthorized comment deletion.|
| Tours Applied     | Security & Penetration Tour, User-Role Tour                                 |
+-------------------+-----------------------------------------------------------------------------+
```

### Scenarios Explored & Findings:
1. **Cross-Site Scripting (XSS) Attack Payload:**
   - *Action:* Injected `<script>alert("VULNERABLE")</script><img src="x" onerror="alert(1)">` into comment box.
   - *Observation:* Protected. The function `escapeHtml()` transformed `<` to `&lt;` and `>` to `&gt;`. The payload was rendered safely as visible text. No JavaScript execution occurred.
2. **Comment Deletion Access Control:**
   - *Action:* User `Anita Sharma` posted comment $C_1$. User `Rahul Verma` logged in and viewed the feed.
   - *Observation:* Rahul Verma could NOT see the Delete button for $C_1$. When Anita Sharma logged back in, the Delete button for $C_1$ was visible and operational.
3. **Overlong Comment Stress Test:**
   - *Action:* Pasted a 600-character lorem ipsum string.
   - *Observation:* Rejected with alert: `"Comment cannot exceed 500 characters."`

---

```
+-------------------------------------------------------------------------------------------------+
| Charter 6: Cross-Resolution Responsive Viewport Tour                                            |
+-------------------+-----------------------------------------------------------------------------+
| Timebox           | 30 Minutes                                                                  |
| Mission           | Verify layout stability at 1366px, 1024px, 768px, 480px, and 360px.         |
| Tours Applied     | Supermodel / Responsive Layout Tour                                         |
+-------------------+-----------------------------------------------------------------------------+
```

### Scenarios Explored & Findings:
1. **Desktop Viewport (1366 × 768):**
   - Clean 4-column statistics grid, 2-column hero layout, all navbar links fully visible, forms comfortable with no horizontal scrollbar.
2. **Tablet Viewport (1024 × 768):**
   - Footer reflows into 2 × 2 grid, stat cards adapt smoothly, search bar remains centered.
3. **Mobile Viewport (480 × 800):**
   - Desktop navigation list collapses into mobile slide-down menu.
   - Mobile hamburger button (`#nav-toggle`) renders clearly.
   - Form fields stack into single-column inputs (`1fr`), preventing horizontal clipping.

---

## 3. Summary of Exploratory Observations & Risk Triage

| Observation Area | Potential Risk Identified | Safeguard / Resolution Implemented | Risk Level |
| :--- | :--- | :--- | :--- |
| **XSS Injection** | User comments could execute malicious script tags. | `escapeHtml` utility sanitizes all comment content prior to DOM rendering. | **RESOLVED (Low)** |
| **Duplicate Appointments** | Patients might spam multiple slots on same date. | JavaScript slot comparison enforces single appointment per mobile per day. | **RESOLVED (Low)** |
| **Unauthorized Deletion** | Malicious users could delete community posts. | UI compares logged-in user email against comment author email before rendering delete button. | **RESOLVED (Low)** |
| **Empty Comment Submission** | Accidental click posts blank card. | `novalidate` added to `<form id="comment-post-form">` and trimmed length validation enforced. | **RESOLVED (Low)** |
