"""
Test Case Catalog and Metadata Mapping
Defines expected results, IEEE 829 test IDs, affected features, and bug taxonomy defaults for all automated tests.
"""

TEST_METADATA = {
    # 1. Registration Suite
    "test_01_registration_modal_toggle": {
        "id": "TC-REG-01",
        "suite": "Registration",
        "title": "Registration Modal Toggle",
        "feature": "User Onboarding / Modals",
        "expected": "Register button opens modal; close button dismisses modal without errors.",
        "severity": "S3 (Moderate)",
        "priority": "P2 (High)"
    },
    "test_02_registration_empty_fields_validation": {
        "id": "TC-REG-02",
        "suite": "Registration",
        "title": "Registration Empty Fields Validation",
        "feature": "Form Validation (Mandatory Fields)",
        "expected": "Submitting blank registration form displays mandatory fields validation alert.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_03_registration_invalid_email_regex": {
        "id": "TC-REG-03",
        "suite": "Registration",
        "title": "Email Regular Expression Validation",
        "feature": "Regex Input Validation (REQ-07)",
        "expected": "Emails lacking '@' or containing invalid characters ('@@') are rejected.",
        "severity": "S2 (Major)",
        "priority": "P1 (Immediate)"
    },
    "test_04_registration_short_password_validation": {
        "id": "TC-REG-04",
        "suite": "Registration",
        "title": "Minimum Password Length Enforcement",
        "feature": "Account Security / Password Policy",
        "expected": "Passwords shorter than 6 characters are flagged and rejected.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_05_registration_password_mismatch": {
        "id": "TC-REG-05",
        "suite": "Registration",
        "title": "Password Confirmation Check",
        "feature": "Form Validation (Password Confirmation)",
        "expected": "Mismatched password and confirm-password fields trigger validation error.",
        "severity": "S3 (Moderate)",
        "priority": "P2 (High)"
    },
    "test_06_registration_successful_and_auto_transition": {
        "id": "TC-REG-06",
        "suite": "Registration",
        "title": "Valid User Registration Flow",
        "feature": "User Registration & LocalStorage (REQ-01)",
        "expected": "Valid user record is saved in LocalStorage and automatically transitions to login modal.",
        "severity": "S1 (Blocker)",
        "priority": "P1 (Immediate)"
    },
    "test_07_registration_duplicate_email_prevention": {
        "id": "TC-REG-07",
        "suite": "Registration",
        "title": "Duplicate Registration Prevention",
        "feature": "Data Integrity (REQ-14)",
        "expected": "Attempting to register an already existing email is intercepted and blocked.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_08_covid_test_registration_valid_submission": {
        "id": "TC-REG-08",
        "suite": "Registration",
        "title": "COVID-19 Test Registration Booking",
        "feature": "Diagnostic Test Management (MOD-03)",
        "expected": "Valid patient details book test appointment, generate Order ID, and update state total.",
        "severity": "S1 (Blocker)",
        "priority": "P1 (Immediate)"
    },
    "test_09_covid_test_registration_invalid_phone_regex": {
        "id": "TC-REG-09",
        "suite": "Registration",
        "title": "Mobile Number Regex Validation",
        "feature": "Regex Input Validation (REQ-08)",
        "expected": "Phone numbers not starting with 6-9 or not having 10 digits are rejected.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },

    # 2. Login Suite
    "test_01_login_modal_toggle": {
        "id": "TC-LOG-01",
        "suite": "Login",
        "title": "Login Modal Toggle",
        "feature": "User Authentication / Modals",
        "expected": "Login button opens modal; close button dismisses modal.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_02_login_empty_fields_validation": {
        "id": "TC-LOG-02",
        "suite": "Login",
        "title": "Login Empty Input Validation",
        "feature": "Authentication Form Validation",
        "expected": "Submitting empty credentials displays mandatory input error.",
        "severity": "S3 (Moderate)",
        "priority": "P2 (High)"
    },
    "test_03_login_invalid_email_regex": {
        "id": "TC-LOG-03",
        "suite": "Login",
        "title": "Login Email Format Validation",
        "feature": "Authentication / Regex Validation",
        "expected": "Malformed email format on login input is rejected by regex check.",
        "severity": "S3 (Moderate)",
        "priority": "P2 (High)"
    },
    "test_04_login_unregistered_email": {
        "id": "TC-LOG-04",
        "suite": "Login",
        "title": "Unregistered Account Rejection",
        "feature": "Authentication Logic (REQ-03)",
        "expected": "Non-existent user email displays invalid credentials error.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_05_login_wrong_password": {
        "id": "TC-LOG-05",
        "suite": "Login",
        "title": "Incorrect Password Rejection",
        "feature": "Authentication Security (REQ-03)",
        "expected": "Registered user with incorrect password is denied access.",
        "severity": "S2 (Major)",
        "priority": "P1 (Immediate)"
    },
    "test_06_login_successful_and_session_display": {
        "id": "TC-LOG-06",
        "suite": "Login",
        "title": "Valid Login & Session Persistence",
        "feature": "Session Management & Greeting UI (REQ-03)",
        "expected": "Valid login creates LocalStorage session, displays Welcome greeting, and shows Logout button.",
        "severity": "S1 (Blocker)",
        "priority": "P1 (Immediate)"
    },
    "test_07_user_logout_clears_session": {
        "id": "TC-LOG-07",
        "suite": "Login",
        "title": "User Logout & Session Destruction",
        "feature": "Session Destruction / Route Guard",
        "expected": "Logout removes session from LocalStorage and restores logged-out navigation state.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_08_admin_login_verification": {
        "id": "TC-LOG-08",
        "suite": "Login",
        "title": "Admin Authentication Check",
        "feature": "Administrative Portal Access (REQ-03)",
        "expected": "Admin credentials ('admin'/'admin123') authenticate administrative access.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },

    # 3. Search Suite
    "test_01_portal_search_matching_query": {
        "id": "TC-SRC-01",
        "suite": "Search",
        "title": "Portal Knowledge Search Query",
        "feature": "Information Retrieval / Search Module",
        "expected": "Searching 'RT-PCR' retrieves corresponding diagnostic guide and category badge.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_02_portal_search_symptoms_query": {
        "id": "TC-SRC-02",
        "suite": "Search",
        "title": "Symptom Keyword Search Query",
        "feature": "Information Retrieval / Symptoms",
        "expected": "Searching 'fever' retrieves fever clinical indicators topic.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_03_portal_search_unknown_query_fallback": {
        "id": "TC-SRC-03",
        "suite": "Search",
        "title": "Unknown Query Fallback Alert",
        "feature": "Search Fallback Handling",
        "expected": "Searching non-existent query displays 'No Results Found' message gracefully.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_04_portal_search_clear_button": {
        "id": "TC-SRC-04",
        "suite": "Search",
        "title": "Search Input Clear Lifecycle",
        "feature": "Search UI Controls",
        "expected": "Typing displays clear button; clicking it resets input and hides results.",
        "severity": "S4 (Minor)",
        "priority": "P4 (Low)"
    },
    "test_05_portal_search_trending_quick_tags": {
        "id": "TC-SRC-05",
        "suite": "Search",
        "title": "Trending Search Tag Execution",
        "feature": "Search Shortcut Tags",
        "expected": "Clicking quick search tag immediately populates and filters matching topics.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_06_report_search_registered_mobile": {
        "id": "TC-SRC-06",
        "suite": "Search",
        "title": "Patient Report Search by Phone",
        "feature": "Diagnostic Report Retrieval (REQ-05)",
        "expected": "Searching phone '9876543210' displays Anita Sharma's diagnostic lab report card.",
        "severity": "S1 (Blocker)",
        "priority": "P1 (Immediate)"
    },
    "test_07_report_search_by_order_id": {
        "id": "TC-SRC-07",
        "suite": "Search",
        "title": "Patient Report Search by Order ID",
        "feature": "Order ID Tracking (REQ-05)",
        "expected": "Searching 'ORD-1001' retrieves matching laboratory certificate.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_08_report_search_unregistered_mobile_not_found": {
        "id": "TC-SRC-08",
        "suite": "Search",
        "title": "Unregistered Record Search Handling",
        "feature": "Report Search Exception Handling (REQ-06)",
        "expected": "Searching unregistered phone displays 'No Patient Report Found' alert without crash.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },

    # 4. Comments Suite
    "test_01_comments_locked_when_logged_out": {
        "id": "TC-CMT-01",
        "suite": "Comments",
        "title": "Guest Comment Access Restriction",
        "feature": "Access Control / Comments Route Guard",
        "expected": "Guest users see auth required banner and comment form is locked.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_02_comments_unlocked_when_logged_in": {
        "id": "TC-CMT-02",
        "suite": "Comments",
        "title": "Authenticated Comment Form Unlock",
        "feature": "Comments Module Authorization",
        "expected": "Logged in user sees unlocked comment form with their name badge.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_03_comment_empty_validation": {
        "id": "TC-CMT-03",
        "suite": "Comments",
        "title": "Empty Comment Validation",
        "feature": "Comments Form Validation",
        "expected": "Submitting blank comment displays 'Comment cannot be empty' alert.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_04_comment_successful_posting": {
        "id": "TC-CMT-04",
        "suite": "Comments",
        "title": "Valid Comment Posting & Feed Display",
        "feature": "Community Discussion Forum (REQ-12)",
        "expected": "Comment is saved to LocalStorage and displayed with author name and timestamp.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_05_comment_xss_protection_and_escaping": {
        "id": "TC-CMT-05",
        "suite": "Comments",
        "title": "Stored XSS Injection Protection",
        "feature": "Security & Sanitization (CAT-SEC-003)",
        "expected": "Script tags (<script>) are safely HTML-escaped and displayed as plain text.",
        "severity": "S1 (Blocker)",
        "priority": "P1 (Immediate)"
    },
    "test_06_comment_author_deletion": {
        "id": "TC-CMT-06",
        "suite": "Comments",
        "title": "Author-Only Comment Deletion",
        "feature": "Comments Deletion Access Control",
        "expected": "Author sees Delete button and can delete their own posted comment.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_07_comment_non_author_cannot_delete": {
        "id": "TC-CMT-07",
        "suite": "Comments",
        "title": "Non-Author Deletion Restriction",
        "feature": "Authorization Boundaries",
        "expected": "Users cannot view or click delete buttons for comments authored by others.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },

    # 5. Navigation Suite
    "test_01_all_navbar_links_present": {
        "id": "TC-NAV-01",
        "suite": "Navigation",
        "title": "Module Navigation Links Presence",
        "feature": "Top-Level Navigation Bar (CAT-NAV)",
        "expected": "All 9 module navigation links are present and visible with expected labels.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_02_navbar_navigation_targets": {
        "id": "TC-NAV-02",
        "suite": "Navigation",
        "title": "Navbar Section Routing Targets",
        "feature": "Anchor Navigation / Smooth Scrolling",
        "expected": "Clicking navigation links smoothly routes to corresponding section targets.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_03_hero_cta_buttons": {
        "id": "TC-NAV-03",
        "suite": "Navigation",
        "title": "Hero Call-to-Action Buttons",
        "feature": "Hero Section Interactive Controls",
        "expected": "Hero action buttons (Book Test, Track Report, Check Symptoms) are clickable.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_04_mobile_viewport_hamburger_navigation": {
        "id": "TC-NAV-04",
        "suite": "Navigation",
        "title": "Mobile Viewport Hamburger Toggle",
        "feature": "Responsive Design & Mobile Layout (REQ-15)",
        "expected": "At 480px width, hamburger button appears and toggles mobile menu visibility.",
        "severity": "S2 (Major)",
        "priority": "P2 (High)"
    },
    "test_05_modal_escape_key_dismissal": {
        "id": "TC-NAV-05",
        "suite": "Navigation",
        "title": "Keyboard Accessibility (ESC Dismissal)",
        "feature": "Modal Accessibility / Keyboard Navigation",
        "expected": "Pressing the Escape key dismisses active modal dialogs without clicking close.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    },
    "test_06_interactive_symptom_checker": {
        "id": "TC-NAV-06",
        "suite": "Navigation",
        "title": "Interactive Symptom Risk Self-Assessment",
        "feature": "Clinical Manifestations / Risk Checker",
        "expected": "Selecting symptom checkboxes evaluates risk level and renders guidance alert.",
        "severity": "S3 (Moderate)",
        "priority": "P3 (Medium)"
    }
}
