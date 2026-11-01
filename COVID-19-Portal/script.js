/**
 * COVID-19 Information & Awareness Portal - JavaScript Core Engine
 * STQA Mini Project - Experiment 14
 * Pure Vanilla JavaScript & LocalStorage Data Store
 * Regular Expressions Aligned with IEEE 829 Test Plan (MOD-01 to MOD-07)
 */

// ==========================================
// 1. REGULAR EXPRESSION PATTERNS (IEEE 829)
// ==========================================
const REGEX_RULES = {
  // REQ-07: Email with local part, single @, domain, and TLD of 2+ letters
  email: /^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$/,
  
  // REQ-08: Exactly 10 digits, first digit 6-9
  phone: /^[6-9][0-9]{9}$/,
  
  // REQ-10: Date in YYYY-MM-DD (1900-2099)
  dob: /^(19|20)[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$/,
  
  // REQ-11: Aadhaar (12 digits, starts with 2-9)
  aadhaar: /^[2-9][0-9]{11}$/,
  
  // REQ-11: PAN Card (5 caps, 4 digits, 1 cap)
  pan: /^[A-Z]{5}[0-9]{4}[A-Z]$/,
  
  // REQ-11: Voter ID (3 caps, 7 digits)
  voter: /^[A-Z]{3}[0-9]{7}$/,
  
  // REQ-09: Slot Date-Time (YYYY-MM-DDTHH:MM)
  slotDateTime: /^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]$/
};

// ==========================================
// 2. LOCALSTORAGE KEYS & INITIAL SEED DATA
// ==========================================
const STORAGE_KEYS = {
  USERS: 'covid_portal_users',
  SESSION: 'covid_portal_session',
  TEST_RECORDS: 'covid_portal_test_records',
  COMMENTS: 'covid_portal_comments',
  STATE_STATS: 'covid_portal_state_stats'
};

// Seed baseline records if not already initialized
function initializeDefaultData() {
  // 1. Registered Users
  if (!localStorage.getItem(STORAGE_KEYS.USERS)) {
    const defaultUsers = [
      {
        name: 'Anita Sharma',
        email: 'anita.sharma@example.com',
        password: 'password123',
        registeredAt: '2026-10-15T09:30:00Z'
      },
      {
        name: 'Rahul Verma',
        email: 'rahul.verma@example.com',
        password: 'password123',
        registeredAt: '2026-10-16T11:00:00Z'
      }
    ];
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(defaultUsers));
  }

  // 2. COVID Diagnostic Test Records (Matches REQ-01, REQ-05 baseline data)
  if (!localStorage.getItem(STORAGE_KEYS.TEST_RECORDS)) {
    const defaultTests = [
      {
        orderId: 'ORD-1001',
        name: 'Anita Sharma',
        phone: '9876543210',
        dob: '1998-04-17',
        govtIdType: 'PAN',
        govtIdNum: 'ABCDE1234F',
        state: 'Maharashtra',
        address: '12 MG Road, Pune',
        testType: 'RT-PCR',
        slot: '2026-11-05T10:30',
        status: 'NEGATIVE',
        clinicalResult: 'SARS-CoV-2 RNA Not Detected (Negative)',
        registeredAt: '2026-10-30T10:30:00'
      },
      {
        orderId: 'ORD-1002',
        name: 'Rahul Verma',
        phone: '9812345678',
        dob: '1995-08-22',
        govtIdType: 'Aadhaar',
        govtIdNum: '234567890123',
        state: 'Delhi',
        address: 'Connaught Place, New Delhi',
        testType: 'Rapid Antigen',
        slot: '2026-11-04T14:00',
        status: 'NEGATIVE',
        clinicalResult: 'Rapid Antigen Negative (No viral protein detected)',
        registeredAt: '2026-10-31T09:15:00'
      },
      {
        orderId: 'ORD-1003',
        name: 'Priya Patel',
        phone: '9765432109',
        dob: '2000-02-14',
        govtIdType: 'VoterID',
        govtIdNum: 'ABC1234567',
        state: 'Gujarat',
        address: 'SG Highway, Ahmedabad',
        testType: 'RT-PCR',
        slot: '2026-11-06T11:00',
        status: 'POSITIVE',
        clinicalResult: 'SARS-CoV-2 RNA Detected (Positive - Mild Viral Load)',
        registeredAt: '2026-10-31T15:45:00'
      }
    ];
    localStorage.setItem(STORAGE_KEYS.TEST_RECORDS, JSON.stringify(defaultTests));
  }

  // 3. State-wise Dashboard Statistics Baseline (REQ-13)
  if (!localStorage.getItem(STORAGE_KEYS.STATE_STATS)) {
    const stateStats = [
      { state: 'Maharashtra', totalTests: 18450, positive: 450, recovered: 432 },
      { state: 'Delhi', totalTests: 14200, positive: 380, recovered: 371 },
      { state: 'Uttar Pradesh', totalTests: 12500, positive: 210, recovered: 204 },
      { state: 'Bihar', totalTests: 8900, positive: 145, recovered: 141 },
      { state: 'Karnataka', totalTests: 11200, positive: 260, recovered: 252 },
      { state: 'Tamil Nadu', totalTests: 10400, positive: 220, recovered: 215 },
      { state: 'Gujarat', totalTests: 9800, positive: 195, recovered: 189 },
      { state: 'West Bengal', totalTests: 7600, positive: 160, recovered: 154 }
    ];
    localStorage.setItem(STORAGE_KEYS.STATE_STATS, JSON.stringify(stateStats));
  }

  // 4. Initial Seed Comments (REQ-12)
  if (!localStorage.getItem(STORAGE_KEYS.COMMENTS)) {
    const defaultComments = [
      {
        id: 'cmt-1',
        authorName: 'Anita Sharma',
        authorEmail: 'anita.sharma@example.com',
        content: 'Received my RT-PCR test result within 12 hours. The slot booking workflow was very smooth!',
        date: '31 Oct 2026, 10:45 AM'
      },
      {
        id: 'cmt-2',
        authorName: 'Rahul Verma',
        authorEmail: 'rahul.verma@example.com',
        content: 'Got the Corbevax precautionary booster dose yesterday. Slight arm soreness but feeling completely healthy today.',
        date: '31 Oct 2026, 02:15 PM'
      }
    ];
    localStorage.setItem(STORAGE_KEYS.COMMENTS, JSON.stringify(defaultComments));
  }
}

// ==========================================
// 3. DOM LOAD & INITIALIZATION
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
  initializeDefaultData();
  setupNavigation();
  updateAuthUI();
  renderStateDashboard();
  renderComments();
  setupSearchInputListener();
  setupMinSlotDate();
  initQADashboard();
});

// Setup Mobile Navigation Toggle
function setupNavigation() {
  const toggleBtn = document.getElementById('nav-toggle');
  const mainNav = document.getElementById('main-nav');
  
  if (toggleBtn && mainNav) {
    toggleBtn.addEventListener('click', () => {
      mainNav.classList.toggle('show');
    });

    // Close menu when clicking navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mainNav.classList.remove('show');
      });
    });
  }

  // Set active link on scroll
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    let scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      const navItem = document.querySelector(`.nav-link[href*="${sectionId}"]`);
      if (navItem) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          navItem.classList.add('active');
        } else {
          navItem.classList.remove('active');
        }
      }
    });
  });
}

// Setup minimum slot date to today's date + 1 day
function setupMinSlotDate() {
  const slotInput = document.getElementById('patient-slot');
  if (slotInput) {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(9, 0, 0, 0);
    const yyyy = tomorrow.getFullYear();
    const mm = String(tomorrow.getMonth() + 1).padStart(2, '0');
    const dd = String(tomorrow.getDate()).padStart(2, '0');
    slotInput.min = `${yyyy}-${mm}-${dd}T09:00`;
  }
}

// ==========================================
// 4. USER AUTHENTICATION (MOD-01)
// ==========================================

// Get logged in session
function getCurrentSession() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEYS.SESSION));
  } catch (e) {
    return null;
  }
}

// Update UI based on session state
function updateAuthUI() {
  const session = getCurrentSession();
  const loggedOutActions = document.getElementById('logged-out-actions');
  const loggedInActions = document.getElementById('logged-in-actions');
  const userDisplayName = document.getElementById('user-display-name');
  
  const commentAuthLock = document.getElementById('comment-auth-lock');
  const commentPostForm = document.getElementById('comment-post-form');
  const commentAuthorName = document.getElementById('comment-author-name');

  if (session && session.email) {
    // Logged In
    if (loggedOutActions) loggedOutActions.classList.add('hidden');
    if (loggedInActions) loggedInActions.classList.remove('hidden');
    if (userDisplayName) userDisplayName.textContent = `Welcome, ${session.name}`;
    
    // Unlock Comments
    if (commentAuthLock) commentAuthLock.classList.add('hidden');
    if (commentPostForm) commentPostForm.classList.remove('hidden');
    if (commentAuthorName) commentAuthorName.textContent = session.name;
  } else {
    // Logged Out
    if (loggedOutActions) loggedOutActions.classList.remove('hidden');
    if (loggedInActions) loggedInActions.classList.add('hidden');
    
    // Lock Comments
    if (commentAuthLock) commentAuthLock.classList.remove('hidden');
    if (commentPostForm) commentPostForm.classList.add('hidden');
  }

  // Attach logout handler
  const logoutBtn = document.getElementById('logout-button');
  if (logoutBtn) {
    logoutBtn.onclick = handleUserLogout;
  }
}

// User Registration Handler
function handleUserRegister(e) {
  e.preventDefault();
  const nameInput = document.getElementById('register-name');
  const emailInput = document.getElementById('register-email');
  const passInput = document.getElementById('register-password');
  const confirmPassInput = document.getElementById('register-confirm-password');
  const msgBox = document.getElementById('register-msg');

  const name = nameInput.value.trim();
  const email = emailInput.value.trim().toLowerCase();
  const password = passInput.value;
  const confirmPassword = confirmPassInput.value;

  // Validation Checks
  if (!name || !email || !password || !confirmPassword) {
    showMsg(msgBox, 'All fields are mandatory. Please fill in all fields.', 'danger');
    return;
  }

  if (name.length < 2) {
    showMsg(msgBox, 'Name must contain at least 2 characters.', 'danger');
    return;
  }

  // REQ-07: Email Regex Validation
  if (!REGEX_RULES.email.test(email)) {
    showMsg(msgBox, 'Invalid email format. Must contain "@" and a valid domain (e.g. user@example.com).', 'danger');
    return;
  }

  // Password length requirement
  if (password.length < 6) {
    showMsg(msgBox, 'Password must be at least 6 characters in length.', 'danger');
    return;
  }

  // Password confirmation check
  if (password !== confirmPassword) {
    showMsg(msgBox, 'Passwords do not match. Please verify both passwords.', 'danger');
    return;
  }

  // Check Duplicate Email Registration
  let users = [];
  try {
    users = JSON.parse(localStorage.getItem(STORAGE_KEYS.USERS)) || [];
  } catch (err) {
    users = [];
  }

  const existing = users.find(u => u.email === email);
  if (existing) {
    showMsg(msgBox, 'Email address already registered. Please login or use a different email.', 'danger');
    return;
  }

  // Save new user
  const newUser = {
    name,
    email,
    password,
    registeredAt: new Date().toISOString()
  };
  users.push(newUser);
  localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));

  showMsg(msgBox, 'Registration successful! You can now log in with your credentials.', 'success');
  
  // Clear inputs
  nameInput.value = '';
  emailInput.value = '';
  passInput.value = '';
  confirmPassInput.value = '';

  setTimeout(() => {
    switchModal('register-modal', 'login-modal');
  }, 1200);
}

// User Login Handler
function handleUserLogin(e) {
  e.preventDefault();
  const emailInput = document.getElementById('login-email');
  const passInput = document.getElementById('login-password');
  const msgBox = document.getElementById('login-msg');

  const email = emailInput.value.trim().toLowerCase();
  const password = passInput.value;

  if (!email || !password) {
    showMsg(msgBox, 'Please enter both email and password.', 'danger');
    return;
  }

  // REQ-07 Regex check on login email
  if (!REGEX_RULES.email.test(email)) {
    showMsg(msgBox, 'Invalid email format. Must contain @ and valid domain.', 'danger');
    return;
  }

  let users = [];
  try {
    users = JSON.parse(localStorage.getItem(STORAGE_KEYS.USERS)) || [];
  } catch (err) {
    users = [];
  }

  const user = users.find(u => u.email === email && u.password === password);
  if (!user) {
    showMsg(msgBox, 'Invalid email or password. Please verify your credentials.', 'danger');
    return;
  }

  // Save session to LocalStorage
  const session = {
    name: user.name,
    email: user.email,
    loggedInAt: new Date().toISOString()
  };
  localStorage.setItem(STORAGE_KEYS.SESSION, JSON.stringify(session));

  showMsg(msgBox, `Login successful! Welcome back, ${user.name}.`, 'success');
  
  emailInput.value = '';
  passInput.value = '';

  setTimeout(() => {
    closeModal('login-modal');
    updateAuthUI();
    renderComments();
  }, 800);
}

// User Logout Handler
function handleUserLogout() {
  localStorage.removeItem(STORAGE_KEYS.SESSION);
  updateAuthUI();
  renderComments();
}

// Admin Login Handler (from PDF Page 15 Screenshot 4)
function handleAdminLogin(e) {
  e.preventDefault();
  const userInput = document.getElementById('admin-username');
  const passInput = document.getElementById('admin-password');
  const msgBox = document.getElementById('admin-msg');

  const username = userInput.value.trim();
  const password = passInput.value;

  if (username === 'admin' && password === 'admin123') {
    showMsg(msgBox, 'Admin authentication verified. Access granted.', 'success');
    setTimeout(() => {
      closeModal('admin-modal');
      alert('Welcome Admin! You have full administrative access to state testing dashboards and records.');
    }, 800);
  } else {
    showMsg(msgBox, 'Invalid admin username or password. (Hint: admin / admin123)', 'danger');
  }
}

// ==========================================
// 5. COVID-19 TEST REGISTRATION (MOD-03)
// ==========================================

function updateGovtIdPlaceholder() {
  const type = document.getElementById('govt-id-type').value;
  const numInput = document.getElementById('govt-id-num');
  const hint = document.getElementById('govt-id-hint');

  if (type === 'Aadhaar') {
    numInput.placeholder = '12-digit Aadhaar (e.g. 234567890123)';
    hint.textContent = 'Aadhaar must be 12 digits starting with 2-9.';
  } else if (type === 'PAN') {
    numInput.placeholder = '10-character PAN (e.g. ABCDE1234F)';
    hint.textContent = 'PAN: 5 uppercase letters, 4 digits, 1 uppercase letter.';
  } else if (type === 'VoterID') {
    numInput.placeholder = '10-character Voter ID (e.g. ABC1234567)';
    hint.textContent = 'Voter ID: 3 uppercase letters followed by 7 digits.';
  } else {
    numInput.placeholder = 'Enter ID number according to chosen type';
    hint.textContent = 'Aadhaar (12 digits), PAN (e.g. ABCDE1234F), Voter ID (e.g. ABC1234567).';
  }
}

function clearTestRegMsg() {
  const msgBox = document.getElementById('test-reg-msg');
  if (msgBox) {
    msgBox.className = 'alert-box hidden';
    msgBox.textContent = '';
  }
}

function handleTestRegistration(e) {
  e.preventDefault();
  const msgBox = document.getElementById('test-reg-msg');

  const name = document.getElementById('patient-name').value.trim();
  const phone = document.getElementById('patient-phone').value.trim();
  const dob = document.getElementById('patient-dob').value.trim();
  const idType = document.getElementById('govt-id-type').value;
  const idNum = document.getElementById('govt-id-num').value.trim().toUpperCase();
  const state = document.getElementById('patient-state').value;
  const address = document.getElementById('patient-address').value.trim();
  const testType = document.getElementById('test-type').value;
  const slot = document.getElementById('patient-slot').value.trim();

  // 1. Mandatory Field Checks
  if (!name || !phone || !dob || !idType || !idNum || !state || !address || !testType || !slot) {
    showMsg(msgBox, 'All fields are mandatory. Please complete all personal and testing details.', 'danger');
    return;
  }

  // 2. Name validation
  if (name.length < 2) {
    showMsg(msgBox, 'Patient name must be at least 2 characters long.', 'danger');
    return;
  }

  // 3. REQ-08: Phone number Regex (10 digits, starts with 6-9)
  if (!REGEX_RULES.phone.test(phone)) {
    showMsg(msgBox, 'Invalid Mobile Number: Must be exactly 10 digits starting with 6, 7, 8, or 9.', 'danger');
    return;
  }

  // 4. REQ-10: Date of Birth validation (YYYY-MM-DD, not future date)
  if (!REGEX_RULES.dob.test(dob)) {
    showMsg(msgBox, 'Invalid Date of Birth format. Please select a valid calendar date (YYYY-MM-DD).', 'danger');
    return;
  }
  const dobDate = new Date(dob);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  if (dobDate > today) {
    showMsg(msgBox, 'Date of Birth cannot be in the future.', 'danger');
    return;
  }

  // 5. REQ-11: Government ID validation by type
  if (idType === 'Aadhaar') {
    if (!REGEX_RULES.aadhaar.test(idNum)) {
      showMsg(msgBox, 'Invalid Aadhaar: Must be 12 digits and cannot start with 0 or 1.', 'danger');
      return;
    }
  } else if (idType === 'PAN') {
    if (!REGEX_RULES.pan.test(idNum)) {
      showMsg(msgBox, 'Invalid PAN Card: Must be 5 uppercase letters, 4 digits, and 1 uppercase letter (e.g. ABCDE1234F).', 'danger');
      return;
    }
  } else if (idType === 'VoterID') {
    if (!REGEX_RULES.voter.test(idNum)) {
      showMsg(msgBox, 'Invalid Voter ID: Must be 3 uppercase letters followed by 7 digits (e.g. ABC1234567).', 'danger');
      return;
    }
  }

  // 6. REQ-09: Slot Date-Time Validation (must be future slot)
  if (!REGEX_RULES.slotDateTime.test(slot)) {
    showMsg(msgBox, 'Invalid Appointment Slot format (must be YYYY-MM-DDTHH:MM).', 'danger');
    return;
  }
  const slotDate = new Date(slot);
  const now = new Date();
  if (slotDate <= now) {
    showMsg(msgBox, 'Appointment Slot must be scheduled for a future date and time.', 'danger');
    return;
  }

  // 7. Duplicate Check on mobile + test slot date (REQ-14)
  let testRecords = [];
  try {
    testRecords = JSON.parse(localStorage.getItem(STORAGE_KEYS.TEST_RECORDS)) || [];
  } catch (err) {
    testRecords = [];
  }

  const existingSlot = testRecords.find(t => t.phone === phone && t.slot.split('T')[0] === slot.split('T')[0]);
  if (existingSlot) {
    showMsg(msgBox, `A COVID-19 test is already registered for this phone number on ${slot.split('T')[0]}. Duplicate registrations on the same date are not permitted.`, 'danger');
    return;
  }

  // Generate unique order ID
  const orderId = 'ORD-' + Math.floor(1000 + Math.random() * 9000);

  const newRecord = {
    orderId,
    name,
    phone,
    dob,
    govtIdType: idType,
    govtIdNum: idNum,
    state,
    address,
    testType,
    slot,
    status: 'NEGATIVE', // Standard simulated diagnostic outcome
    clinicalResult: 'SARS-CoV-2 RNA Not Detected (Negative)',
    registeredAt: new Date().toISOString()
  };

  testRecords.unshift(newRecord);
  localStorage.setItem(STORAGE_KEYS.TEST_RECORDS, JSON.stringify(testRecords));

  // Update State Dashboard Total dynamically (REQ-13)
  incrementStateTestCount(state);

  showMsg(msgBox, `Test registered successfully! Your Order ID is: ${orderId}. You can track and download your test report in the Search Report module.`, 'success');

  // Reset form
  document.getElementById('covid-test-form').reset();
  updateGovtIdPlaceholder();
}

// Increment State test tally in LocalStorage
function incrementStateTestCount(stateName) {
  try {
    const stats = JSON.parse(localStorage.getItem(STORAGE_KEYS.STATE_STATS)) || [];
    const item = stats.find(s => s.state.toLowerCase() === stateName.toLowerCase());
    if (item) {
      item.totalTests += 1;
      localStorage.setItem(STORAGE_KEYS.STATE_STATS, JSON.stringify(stats));
      renderStateDashboard();
    }
  } catch (e) {
    console.error('Error updating state stats', e);
  }
}

// ==========================================
// 6. SEARCH & TEST REPORT (MOD-04)
// ==========================================

function handleReportSearch() {
  const queryInput = document.getElementById('report-search-input');
  const query = queryInput.value.trim().toLowerCase();

  const emptyPlaceholder = document.getElementById('report-empty-placeholder');
  const resultCard = document.getElementById('report-result-card');
  const notFoundMsg = document.getElementById('report-not-found-msg');

  if (!query) {
    if (emptyPlaceholder) emptyPlaceholder.classList.remove('hidden');
    if (resultCard) resultCard.classList.add('hidden');
    if (notFoundMsg) notFoundMsg.classList.add('hidden');
    return;
  }

  let testRecords = [];
  try {
    testRecords = JSON.parse(localStorage.getItem(STORAGE_KEYS.TEST_RECORDS)) || [];
  } catch (err) {
    testRecords = [];
  }

  // Search by Patient Name, Phone, or Order ID
  const matched = testRecords.find(t => 
    t.phone.toLowerCase() === query ||
    t.orderId.toLowerCase() === query ||
    t.name.toLowerCase() === query ||
    t.name.toLowerCase().includes(query)
  );

  if (matched) {
    // Populate report card fields
    document.getElementById('report-order-no').textContent = `Order #${matched.orderId}`;
    document.getElementById('report-patient-name').textContent = matched.name;
    document.getElementById('report-patient-phone').textContent = matched.phone;
    document.getElementById('report-patient-dob').textContent = `${matched.dob}`;
    document.getElementById('report-patient-govtid').textContent = `${matched.govtIdType}: ${matched.govtIdNum}`;
    document.getElementById('report-test-type').textContent = matched.testType;
    document.getElementById('report-slot-time').textContent = matched.slot.replace('T', ' ');
    document.getElementById('report-patient-state').textContent = matched.state;
    
    const statusBadge = document.getElementById('report-badge-status');
    const clinicalResult = document.getElementById('report-clinical-result');

    statusBadge.textContent = matched.status;
    clinicalResult.textContent = matched.clinicalResult;

    if (matched.status === 'POSITIVE') {
      statusBadge.className = 'report-badge-status positive';
      clinicalResult.className = 'detail-val text-danger';
    } else {
      statusBadge.className = 'report-badge-status';
      clinicalResult.className = 'detail-val text-success';
    }

    if (emptyPlaceholder) emptyPlaceholder.classList.add('hidden');
    if (notFoundMsg) notFoundMsg.classList.add('hidden');
    if (resultCard) resultCard.classList.remove('hidden');

    console.log('1st Test Pass -- User Available');
  } else {
    if (emptyPlaceholder) emptyPlaceholder.classList.add('hidden');
    if (resultCard) resultCard.classList.add('hidden');
    if (notFoundMsg) notFoundMsg.classList.remove('hidden');

    console.log('Test Fail -- Record Not Found');
  }
}

// Download Mock Report
function downloadReportMock() {
  const patient = document.getElementById('report-patient-name').textContent;
  const order = document.getElementById('report-order-no').textContent;
  alert(`Download Report: Diagnostic Report for ${patient} (${order}) generated in PDF format.`);
}

// ==========================================
// 7. STATE-WISE TESTING DASHBOARD (MOD-05)
// ==========================================

function renderStateDashboard() {
  const tableBody = document.getElementById('state-dashboard-body');
  if (!tableBody) return;

  let stats = [];
  try {
    stats = JSON.parse(localStorage.getItem(STORAGE_KEYS.STATE_STATS)) || [];
  } catch (err) {
    stats = [];
  }

  tableBody.innerHTML = '';
  stats.forEach((item, index) => {
    const row = document.createElement('tr');
    const activeRate = (((item.positive - item.recovered) / item.totalTests) * 100).toFixed(2);
    row.innerHTML = `
      <td>${index + 1}</td>
      <td><strong>${escapeHtml(item.state)}</strong></td>
      <td>${item.totalTests.toLocaleString()}</td>
      <td><span class="badge ${item.positive > 300 ? 'tag-moderate' : 'tag-common'}">${item.positive.toLocaleString()}</span></td>
      <td>${item.recovered.toLocaleString()}</td>
      <td>${activeRate}%</td>
    `;
    tableBody.appendChild(row);
  });
}

// ==========================================
// 8. COMMUNITY COMMENTS MODULE (MOD-06)
// ==========================================

function renderComments() {
  const listContainer = document.getElementById('comments-list');
  const countSpan = document.getElementById('comments-count');
  if (!listContainer) return;

  const session = getCurrentSession();
  let comments = [];
  try {
    comments = JSON.parse(localStorage.getItem(STORAGE_KEYS.COMMENTS)) || [];
  } catch (err) {
    comments = [];
  }

  if (countSpan) countSpan.textContent = comments.length;

  if (comments.length === 0) {
    listContainer.innerHTML = '<p class="text-center" style="color: var(--color-text-light); padding: 1rem;">No community comments posted yet. Be the first to share an update!</p>';
    return;
  }

  listContainer.innerHTML = '';
  comments.forEach(c => {
    const item = document.createElement('div');
    item.className = 'comment-item';
    
    // Only author can delete their comment
    const isAuthor = session && session.email && (session.email.toLowerCase() === c.authorEmail.toLowerCase());
    const deleteButtonHtml = isAuthor 
      ? `<button class="delete-comment-btn" id="delete-comment-${c.id}" onclick="deleteComment('${c.id}')">Delete</button>` 
      : '';

    item.innerHTML = `
      <div class="comment-item-header">
        <div class="comment-meta">
          <span class="comment-author">${escapeHtml(c.authorName)}</span>
          <span class="comment-date">${escapeHtml(c.date)}</span>
        </div>
        ${deleteButtonHtml}
      </div>
      <div class="comment-item-body">
        ${escapeHtml(c.content)}
      </div>
    `;
    listContainer.appendChild(item);
  });
}

function handleCommentSubmit(e) {
  e.preventDefault();
  const session = getCurrentSession();
  const input = document.getElementById('comment-input');
  const msgBox = document.getElementById('comment-msg');

  if (!session || !session.email) {
    showMsg(msgBox, 'You must be logged in to post comments.', 'danger');
    return;
  }

  const content = input.value.trim();

  // Validate empty comment
  if (!content) {
    showMsg(msgBox, 'Comment cannot be empty.', 'danger');
    return;
  }

  if (content.length > 500) {
    showMsg(msgBox, 'Comment cannot exceed 500 characters.', 'danger');
    return;
  }

  let comments = [];
  try {
    comments = JSON.parse(localStorage.getItem(STORAGE_KEYS.COMMENTS)) || [];
  } catch (err) {
    comments = [];
  }

  const now = new Date();
  const dateFormatted = now.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  }) + ', ' + now.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });

  const newComment = {
    id: 'cmt-' + Date.now(),
    authorName: session.name,
    authorEmail: session.email,
    content: content, // HTML is escaped on display to protect against XSS
    date: dateFormatted
  };

  comments.unshift(newComment);
  localStorage.setItem(STORAGE_KEYS.COMMENTS, JSON.stringify(comments));

  input.value = '';
  showMsg(msgBox, 'Your comment has been posted successfully!', 'success');
  renderComments();

  setTimeout(() => {
    if (msgBox) msgBox.classList.add('hidden');
  }, 2000);
}

function deleteComment(commentId) {
  const session = getCurrentSession();
  if (!session || !session.email) {
    alert('Please log in to perform this action.');
    return;
  }

  let comments = [];
  try {
    comments = JSON.parse(localStorage.getItem(STORAGE_KEYS.COMMENTS)) || [];
  } catch (err) {
    comments = [];
  }

  const target = comments.find(c => c.id === commentId);
  if (!target) return;

  if (target.authorEmail.toLowerCase() !== session.email.toLowerCase()) {
    alert('Permission denied. You can only delete comments that you authored.');
    return;
  }

  if (confirm('Are you sure you want to delete this comment?')) {
    comments = comments.filter(c => c.id !== commentId);
    localStorage.setItem(STORAGE_KEYS.COMMENTS, JSON.stringify(comments));
    renderComments();
  }
}

// ==========================================
// 9. PORTAL KNOWLEDGE SEARCH (MODULE C)
// ==========================================

const SEARCH_DATABASE = [
  {
    title: 'Fever & Chills',
    category: 'Symptoms',
    keywords: 'fever chills temperature hot cold shivering high',
    desc: 'High body temperature exceeding 38°C (100.4°F) is among the most common early onset symptoms of SARS-CoV-2 infection.',
    link: '#symptoms'
  },
  {
    title: 'Dry Cough & Sore Throat',
    category: 'Symptoms',
    keywords: 'cough dry throat pain irritated coughing fit',
    desc: 'Continuous persistent dry cough lasting over an hour or three bouts within 24 hours indicates respiratory mucosal involvement.',
    link: '#symptoms'
  },
  {
    title: 'Shortness of Breath (Dyspnea)',
    category: 'Critical Alert',
    keywords: 'breath breathing shortness dyspnea oxygen hypoxia chest pain emergency',
    desc: 'Emergency Red Flag: Shortness of breath or oxygen saturation under 94% requires immediate medical attention. Call 108 or 1075.',
    link: '#symptoms'
  },
  {
    title: 'Face Masks & N95 Respirators',
    category: 'Prevention',
    keywords: 'mask n95 surgical protection covering face hygiene filter',
    desc: 'Multi-layer surgical masks or certified N95 respirators significantly filter respiratory aerosols and droplet transmission.',
    link: '#prevention'
  },
  {
    title: 'Hand Hygiene Protocols',
    category: 'Prevention',
    keywords: 'hand wash handwash soap sanitizer alcohol hygiene rub clean',
    desc: 'Wash hands with soap and water for 20+ seconds or use alcohol-based sanitizer with greater than 70% ethanol/isopropanol content.',
    link: '#prevention'
  },
  {
    title: 'Social Distancing (2 Meters)',
    category: 'Prevention',
    keywords: 'distance distancing space physical 6 feet meters crowd gather',
    desc: 'Maintain at least 6 feet (2 meters) distance from individuals in public spaces to avoid airborne droplet projection.',
    link: '#prevention'
  },
  {
    title: 'RT-PCR Diagnostic Test Booking',
    category: 'Diagnostics',
    keywords: 'rt-pcr rtpcr test booking diagnostic swab lab order slot sample',
    desc: 'Reverse Transcription Polymerase Chain Reaction (RT-PCR) is the Gold Standard molecular diagnostic test for detecting SARS-CoV-2 viral RNA.',
    link: '#test-registration'
  },
  {
    title: 'Rapid Antigen Test (RAT)',
    category: 'Diagnostics',
    keywords: 'rapid antigen rat test point of care 30 minutes quick',
    desc: 'Fast point-of-care test providing results within 30 minutes for symptomatic patients and emergency screenings.',
    link: '#test-registration'
  },
  {
    title: 'Patient Test Report Download',
    category: 'Reports',
    keywords: 'report download result certificate positive negative patient search track',
    desc: 'Retrieve and print verified diagnostic reports by searching registered phone number or test order ID.',
    link: '#report-search'
  },
  {
    title: 'Covishield Vaccine',
    category: 'Vaccination',
    keywords: 'covishield astrazeneca vaccine adenovirus recombinant dose schedule',
    desc: 'Recombinant chimpanzee adenovirus vector vaccine encoding spike protein; recommended 2-dose schedule with 84-day interval.',
    link: '#vaccination'
  },
  {
    title: 'Covaxin (BBV152)',
    category: 'Vaccination',
    keywords: 'covaxin bharat biotech inactivated whole virion vaccine',
    desc: 'Inactivated whole virion formulation generating comprehensive immune response against structural proteins with 28-day spacing.',
    link: '#vaccination'
  },
  {
    title: 'Corbevax & Booster Doses',
    category: 'Vaccination',
    keywords: 'booster corbevax precautionary dose third dose immunity hybrid',
    desc: 'Recombinant protein subunit vaccine approved as primary and heterologous precautionary booster.',
    link: '#vaccination'
  },
  {
    title: 'National Emergency Helplines',
    category: 'Helpline',
    keywords: 'helpline emergency phone number contact call 1075 108 hospital toll free',
    desc: 'National Helpline: 1075 (Toll Free), Health Ministry: +91-11-23978046, Mental Health Support: 08046110007.',
    link: '#site-header'
  }
];

function setupSearchInputListener() {
  const searchInput = document.getElementById('search-input');
  const searchBtn = document.getElementById('search-button');
  const clearBtn = document.getElementById('search-clear');

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      if (clearBtn) {
        if (searchInput.value.trim().length > 0) {
          clearBtn.classList.remove('hidden');
        } else {
          clearBtn.classList.add('hidden');
          const resultsContainer = document.getElementById('search-results');
          if (resultsContainer) resultsContainer.classList.add('hidden');
        }
      }
    });

    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        performPortalSearch();
      }
    });
  }

  if (searchBtn) {
    searchBtn.addEventListener('click', performPortalSearch);
  }

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      searchInput.value = '';
      clearBtn.classList.add('hidden');
      const resultsContainer = document.getElementById('search-results');
      if (resultsContainer) {
        resultsContainer.innerHTML = '';
        resultsContainer.classList.add('hidden');
      }
      searchInput.focus();
    });
  }
}

function quickSearch(keyword) {
  const searchInput = document.getElementById('search-input');
  const clearBtn = document.getElementById('search-clear');
  if (searchInput) {
    searchInput.value = keyword;
    if (clearBtn) clearBtn.classList.remove('hidden');
    performPortalSearch();
    document.getElementById('site-search-section').scrollIntoView({ behavior: 'smooth' });
  }
}

function performPortalSearch() {
  const searchInput = document.getElementById('search-input');
  const resultsContainer = document.getElementById('search-results');
  if (!searchInput || !resultsContainer) return;

  const query = searchInput.value.trim().toLowerCase();

  if (!query) {
    resultsContainer.classList.add('hidden');
    resultsContainer.innerHTML = '';
    return;
  }

  const queryTokens = query.split(/\s+/).filter(Boolean);

  const matched = SEARCH_DATABASE.filter(item => {
    const haystack = (item.title + ' ' + item.category + ' ' + item.keywords + ' ' + item.desc).toLowerCase();
    return queryTokens.every(token => haystack.includes(token));
  });

  resultsContainer.classList.remove('hidden');

  if (matched.length === 0) {
    resultsContainer.innerHTML = `
      <div class="alert-box alert-warning" id="no-results-msg">
        <strong>No Results Found:</strong> No matching information found for "${escapeHtml(query)}". Try searching for "symptoms", "vaccine", "mask", "RT-PCR", or "helpline".
      </div>
    `;
    return;
  }

  let html = `<p style="font-size: 0.875rem; color: var(--color-text-light); margin-bottom: 0.75rem;">Found <strong>${matched.length}</strong> matching topic${matched.length > 1 ? 's' : ''}:</p>`;
  
  matched.forEach(item => {
    html += `
      <div class="search-match-card">
        <div class="search-match-header">
          <span class="search-match-title">${escapeHtml(item.title)}</span>
          <span class="search-badge">${escapeHtml(item.category)}</span>
        </div>
        <p class="search-match-desc">${escapeHtml(item.desc)}</p>
        <div style="margin-top: 0.5rem;">
          <a href="${item.link}" class="btn btn-outline-sm" style="font-size: 0.75rem;" onclick="handleSearchJump('${item.link}')">View Section &rarr;</a>
        </div>
      </div>
    `;
  });

  resultsContainer.innerHTML = html;
}

function handleSearchJump(link) {
  const target = document.querySelector(link);
  if (target) {
    target.scrollIntoView({ behavior: 'smooth' });
  }
}

// ==========================================
// 10. SYMPTOMS INTERACTIVE CHECKER
// ==========================================

function evaluateSymptoms() {
  const fever = document.getElementById('chk-fever')?.checked;
  const cough = document.getElementById('chk-cough')?.checked;
  const fatigue = document.getElementById('chk-fatigue')?.checked;
  const smell = document.getElementById('chk-smell')?.checked;
  const throat = document.getElementById('chk-throat')?.checked;
  const breath = document.getElementById('chk-breath')?.checked;
  const chest = document.getElementById('chk-chest')?.checked;

  const resultBox = document.getElementById('checker-result-box');
  if (!resultBox) return;

  resultBox.classList.remove('hidden');

  // Critical Emergency Red Flags
  if (breath || chest) {
    resultBox.className = 'checker-result alert-danger';
    resultBox.innerHTML = `
      <strong>High Risk - Immediate Medical Attention Required:</strong><br>
      You reported respiratory distress or chest pain. These are critical emergency signs. Please contact an emergency health service immediately at <strong>108</strong> or <strong>1075</strong>, or visit the nearest hospital triage center.
    `;
    return;
  }

  // Moderate Symptoms
  let mildCount = 0;
  if (fever) mildCount++;
  if (cough) mildCount++;
  if (fatigue) mildCount++;
  if (smell) mildCount++;
  if (throat) mildCount++;

  if (mildCount >= 2) {
    resultBox.className = 'checker-result alert-warning';
    resultBox.innerHTML = `
      <strong>Moderate Risk - Testing Recommended:</strong><br>
      You have multiple symptoms associated with COVID-19. We recommend self-isolating in a well-ventilated room and booking an RT-PCR diagnostic test.
      <div style="margin-top: 0.5rem;">
        <a href="#test-registration" class="btn btn-primary-sm">Book RT-PCR Test Now</a>
      </div>
    `;
  } else if (mildCount === 1) {
    resultBox.className = 'checker-result alert-info';
    resultBox.innerHTML = `
      <strong>Low / Mild Risk:</strong><br>
      You have mild isolated symptoms. Continue monitoring your temperature, wear a face mask, practice hand hygiene, and rest.
    `;
  } else {
    resultBox.className = 'checker-result alert-success';
    resultBox.innerHTML = `
      <strong>No Common Symptoms Reported:</strong><br>
      You have not selected symptoms associated with COVID-19. Continue practicing preventive measures, wear masks in crowded areas, and keep vaccinations up to date.
    `;
  }
}

function resetSymptomChecker() {
  const ids = ['chk-fever', 'chk-cough', 'chk-fatigue', 'chk-smell', 'chk-throat', 'chk-breath', 'chk-chest'];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.checked = false;
  });
  const resultBox = document.getElementById('checker-result-box');
  if (resultBox) {
    resultBox.classList.add('hidden');
    resultBox.innerHTML = '';
  }
}

// ==========================================
// 11. MODAL CONTROLLERS & UTILITIES
// ==========================================

function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
    // Clear alerts inside modal
    const alerts = modal.querySelectorAll('.alert-box');
    alerts.forEach(a => {
      a.className = 'alert-box hidden';
      a.textContent = '';
    });
  }
}

function closeModalOnBackdrop(e, modalId) {
  if (e.target.id === modalId) {
    closeModal(modalId);
  }
}

function switchModal(fromId, toId) {
  closeModal(fromId);
  openModal(toId);
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    ['login-modal', 'register-modal', 'admin-modal'].forEach(id => closeModal(id));
  }
});

// Helper: Show Alert Messages
function showMsg(element, message, type) {
  if (!element) return;
  element.className = `alert-box alert-${type}`;
  element.textContent = message;
  element.classList.remove('hidden');
}

// Helper: XSS Protection / HTML Escaping (REQ-12)
function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// ==========================================
// 12. INTEGRATED SELENIUM QA DASHBOARD CONTROLLER
// ==========================================

let qaEventSource = null;
let qaCurrentFilter = 'all';
let qaPollInterval = null;

function initQADashboard() {
  setupSSEConnection();
  loadHistoryList();
  fetchQASnapshot();
}

function setupSSEConnection() {
  if (window.EventSource) {
    try {
      if (qaEventSource) {
        qaEventSource.close();
      }
      qaEventSource = new EventSource('/api/test-events');

      qaEventSource.onopen = () => {
        const pill = document.getElementById('qa-server-status');
        if (pill) {
          pill.innerHTML = '<span class="status-dot online"></span> Server Active';
          pill.className = 'server-status-pill';
        }
      };

      qaEventSource.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data);
          handleQAEvent(data);
        } catch (err) {
          // heartbeat comment or non-json
        }
      };

      qaEventSource.onerror = () => {
        // Fallback to polling if SSE disconnected
        startPollingFallback();
      };
    } catch (e) {
      startPollingFallback();
    }
  } else {
    startPollingFallback();
  }
}

function startPollingFallback() {
  if (!qaPollInterval) {
    qaPollInterval = setInterval(fetchQASnapshot, 1000);
  }
}

function stopPollingFallback() {
  if (qaPollInterval) {
    clearInterval(qaPollInterval);
    qaPollInterval = null;
  }
}

function fetchQASnapshot() {
  fetch('/api/test-status')
    .then(res => res.json())
    .then(data => {
      renderFullQASnapshot(data);
    })
    .catch(() => {
      const pill = document.getElementById('qa-server-status');
      if (pill) {
        pill.innerHTML = '<span class="status-dot" style="background:#e74a3b;"></span> Disconnected';
      }
    });
}

function handleQAEvent(event) {
  const type = event.type;

  if (type === 'init') {
    renderFullQASnapshot(event.snapshot);
  } else if (type === 'suite_start') {
    resetQADashboardUI(event.total, event.suite);
  } else if (type === 'test_start') {
    const curLabel = document.getElementById('qa-current-test-name');
    if (curLabel) {
      curLabel.textContent = `⚡ Executing: ${event.title} (${event.test_id})...`;
    }
    upsertTestRow({
      test_id: event.test_id,
      method: event.method,
      suite: event.suite,
      expected: event.expected,
      actual: 'Executing Selenium browser actions...',
      status: 'RUNNING',
      duration: '...'
    });
  } else if (type === 'test_complete') {
    const rec = event.record;
    upsertTestRow(rec);
    if (event.bug) {
      appendBugCard(event.bug);
    }
    updateProgressFromDOM();
  } else if (type === 'suite_complete') {
    const summary = event.summary;
    renderFullQASnapshot(summary);
    const statusPill = document.getElementById('qa-runner-status');
    if (statusPill) {
      statusPill.textContent = 'STATUS: COMPLETED';
      statusPill.className = 'badge badge-success py-2 px-3 mr-2';
    }
    const curLabel = document.getElementById('qa-current-test-name');
    if (curLabel) {
      curLabel.textContent = `Completed ${summary.total} tests in ${summary.duration} (Pass Rate: ${summary.pass_rate}%)`;
    }
    loadHistoryList();
  }
}

function resetQADashboardUI(total, suiteName) {
  const statusPill = document.getElementById('qa-runner-status');
  if (statusPill) {
    statusPill.textContent = `RUNNING: ${suiteName.toUpperCase()}`;
    statusPill.className = 'badge badge-warning py-2 px-3 mr-2';
  }

  const progressBar = document.getElementById('qa-progress-bar');
  if (progressBar) {
    progressBar.style.width = '0%';
    progressBar.textContent = '0%';
    progressBar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-primary';
  }

  const progressText = document.getElementById('qa-progress-text');
  if (progressText) {
    progressText.textContent = `0 / ${total} Completed (0%)`;
  }

  document.getElementById('qa-metric-total').textContent = total;
  document.getElementById('qa-metric-passed').textContent = '0';
  document.getElementById('qa-metric-failed').textContent = '0';
  document.getElementById('qa-metric-skipped').textContent = '0';
  document.getElementById('qa-metric-rate').textContent = '0.0%';
  document.getElementById('qa-metric-duration').textContent = '0.00s';

  const tbody = document.getElementById('qa-results-body');
  if (tbody) tbody.innerHTML = '';

  const bugsSection = document.getElementById('qa-bugs-section');
  const bugsList = document.getElementById('qa-bugs-list');
  if (bugsSection) bugsSection.classList.add('hidden');
  if (bugsList) bugsList.innerHTML = '';
}

function updateProgressFromDOM() {
  const rows = document.querySelectorAll('#qa-results-body tr[data-status]');
  const totalEl = document.getElementById('qa-metric-total');
  const total = parseInt(totalEl?.textContent || '0', 10);
  
  let passed = 0;
  let failed = 0;
  let skipped = 0;

  rows.forEach(r => {
    const st = r.getAttribute('data-status');
    if (st === 'PASS') passed++;
    else if (st === 'FAIL' || st === 'ERROR') failed++;
    else if (st === 'SKIPPED') skipped++;
  });

  const completed = passed + failed + skipped;
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
  const passRate = completed > 0 ? ((passed / completed) * 100).toFixed(1) : '0.0';

  const progressBar = document.getElementById('qa-progress-bar');
  if (progressBar) {
    progressBar.style.width = `${pct}%`;
    progressBar.textContent = `${pct}%`;
  }

  const progressText = document.getElementById('qa-progress-text');
  if (progressText) {
    progressText.textContent = `${completed} / ${total} Completed (${pct}%)`;
  }

  document.getElementById('qa-metric-passed').textContent = passed;
  document.getElementById('qa-metric-failed').textContent = failed;
  document.getElementById('qa-metric-skipped').textContent = skipped;
  document.getElementById('qa-metric-rate').textContent = `${passRate}%`;
}

function renderFullQASnapshot(data) {
  if (!data) return;

  const total = data.total || 0;
  const passed = data.passed || 0;
  const failed = data.failed || 0;
  const skipped = data.skipped || 0;
  const passRate = data.pass_rate || 0.0;
  const duration = data.duration || '0.00s';

  document.getElementById('qa-metric-total').textContent = total;
  document.getElementById('qa-metric-passed').textContent = passed;
  document.getElementById('qa-metric-failed').textContent = failed;
  document.getElementById('qa-metric-skipped').textContent = skipped;
  document.getElementById('qa-metric-rate').textContent = `${passRate}%`;
  document.getElementById('qa-metric-duration').textContent = duration;

  const statusPill = document.getElementById('qa-runner-status');
  if (statusPill) {
    if (data.is_running) {
      statusPill.textContent = `RUNNING: ${data.suite_name ? data.suite_name.toUpperCase() : 'SUITE'}`;
      statusPill.className = 'badge badge-warning py-2 px-3 mr-2';
    } else {
      statusPill.textContent = 'STATUS: IDLE';
      statusPill.className = 'badge badge-info py-2 px-3 mr-2';
    }
  }

  const curLabel = document.getElementById('qa-current-test-name');
  if (curLabel && data.current_test) {
    curLabel.textContent = data.current_test;
  }

  const completed = passed + failed + skipped;
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
  const progressBar = document.getElementById('qa-progress-bar');
  if (progressBar) {
    progressBar.style.width = `${pct}%`;
    progressBar.textContent = `${pct}%`;
  }

  const progressText = document.getElementById('qa-progress-text');
  if (progressText) {
    progressText.textContent = `${completed} / ${total} Completed (${pct}%)`;
  }

  // Render Records
  const tbody = document.getElementById('qa-results-body');
  if (tbody && data.records && data.records.length > 0) {
    tbody.innerHTML = '';
    data.records.forEach(rec => upsertTestRow(rec));
  }

  // Render Bugs
  const bugsSection = document.getElementById('qa-bugs-section');
  const bugsList = document.getElementById('qa-bugs-list');
  const bugCountSpan = document.getElementById('qa-bug-count');

  if (bugsSection && bugsList) {
    if (data.bugs && data.bugs.length > 0) {
      bugsSection.classList.remove('hidden');
      if (bugCountSpan) bugCountSpan.textContent = data.bugs.length;
      bugsList.innerHTML = '';
      data.bugs.forEach(b => appendBugCard(b));
    } else {
      bugsSection.classList.add('hidden');
      bugsList.innerHTML = '';
      if (bugCountSpan) bugCountSpan.textContent = '0';
    }
  }
}

function upsertTestRow(rec) {
  const tbody = document.getElementById('qa-results-body');
  if (!tbody) return;

  const rowId = `qa-row-${rec.test_id}`;
  let row = document.getElementById(rowId);

  const statusClass = rec.status === 'PASS' ? 'badge-success' :
                      rec.status === 'FAIL' || rec.status === 'ERROR' ? 'badge-danger' :
                      rec.status === 'RUNNING' ? 'badge-warning' : 'badge-secondary';

  const innerHtml = `
    <td><strong>${escapeHtml(rec.test_id)}</strong></td>
    <td>
      <strong>${escapeHtml(rec.title || rec.method)}</strong>
      <small class="d-block text-muted font-monospace">${escapeHtml(rec.suite || '')} &bull; ${escapeHtml(rec.method || '')}</small>
    </td>
    <td><small>${escapeHtml(rec.expected || '')}</small></td>
    <td><small class="${rec.status === 'FAIL' ? 'text-danger font-weight-bold' : ''}">${escapeHtml(rec.actual || '')}</small></td>
    <td><span class="badge ${statusClass}">${escapeHtml(rec.status)}</span></td>
    <td><small>${escapeHtml(rec.duration || '')}</small></td>
  `;

  if (!row) {
    row = document.createElement('tr');
    row.id = rowId;
    tbody.appendChild(row);
  }

  row.setAttribute('data-status', rec.status);
  row.innerHTML = innerHtml;

  // Apply current filter visibility
  if (qaCurrentFilter !== 'all' && rec.status !== qaCurrentFilter) {
    row.style.display = 'none';
  } else {
    row.style.display = '';
  }
}

function appendBugCard(bug) {
  const bugsList = document.getElementById('qa-bugs-list');
  const bugsSection = document.getElementById('qa-bugs-section');
  if (!bugsList) return;

  if (bugsSection) bugsSection.classList.remove('hidden');

  const card = document.createElement('div');
  card.className = 'qa-bug-card';
  card.innerHTML = `
    <div class="qa-bug-header">
      <span class="qa-bug-title">${escapeHtml(bug.bug_id)}: ${escapeHtml(bug.method)} (${escapeHtml(bug.test_id)})</span>
      <div>
        <span class="badge badge-danger mr-1">${escapeHtml(bug.severity || 'S2 Major')}</span>
        <span class="badge badge-warning">${escapeHtml(bug.priority || 'P2 High')}</span>
      </div>
    </div>
    <div class="qa-bug-details">
      <p class="mb-1"><strong>Feature Affected:</strong> ${escapeHtml(bug.feature || 'Application Core')}</p>
      <p class="mb-1"><strong>Expected:</strong> ${escapeHtml(bug.expected || '')}</p>
      <p class="mb-1 text-danger"><strong>Actual Behavior:</strong> ${escapeHtml(bug.actual || '')}</p>
      ${bug.screenshot ? `<p class="mb-1"><a href="${escapeHtml(bug.screenshot)}" target="_blank" class="btn btn-outline-danger btn-sm">View Failure Screenshot</a></p>` : ''}
      <div class="qa-bug-trace">${escapeHtml(bug.error_details || '')}</div>
    </div>
  `;
  bugsList.appendChild(card);
}

function filterResultsTable(filter) {
  qaCurrentFilter = filter;
  const rows = document.querySelectorAll('#qa-results-body tr[data-status]');
  rows.forEach(r => {
    const st = r.getAttribute('data-status');
    if (filter === 'all' || st === filter) {
      r.style.display = '';
    } else {
      r.style.display = 'none';
    }
  });

  // Update active button state
  document.querySelectorAll('.qa-table-filters button').forEach(b => {
    b.classList.remove('active');
  });
  const activeBtn = event?.target;
  if (activeBtn) activeBtn.classList.add('active');
}

function triggerTestRun(suiteName) {
  const headlessChk = document.getElementById('headless-toggle-chk');
  const isHeadless = headlessChk ? headlessChk.checked : false;

  const targetSection = document.getElementById('qa-testing-dashboard');
  if (targetSection) {
    targetSection.scrollIntoView({ behavior: 'smooth' });
  }

  const curLabel = document.getElementById('qa-current-test-name');
  if (curLabel) {
    curLabel.textContent = `Connecting to Selenium WebDriver (${isHeadless ? 'Headless' : 'Visible Chrome'})...`;
  }

  fetch('/api/run-tests', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      suite: suiteName,
      headless: isHeadless
    })
  })
  .then(res => {
    if (res.status === 409) {
      alert('A test suite is already executing. Please wait for completion.');
      return null;
    }
    return res.json();
  })
  .then(data => {
    if (data && data.status === 'started') {
      const statusPill = document.getElementById('qa-runner-status');
      if (statusPill) {
        statusPill.textContent = `RUNNING: ${suiteName.toUpperCase()}`;
        statusPill.className = 'badge badge-warning py-2 px-3 mr-2';
      }
    }
  })
  .catch(err => {
    console.error('Failed to trigger test suite:', err);
    alert('Failed to connect to local server test runner. Ensure server.py is running on http://localhost:8000.');
  });
}

function loadHistoryList() {
  const select = document.getElementById('qa-history-select');
  if (!select) return;

  fetch('/api/history')
    .then(res => res.json())
    .then(files => {
      select.innerHTML = '<option value="">Select a previous test run...</option>';
      files.forEach(f => {
        const opt = document.createElement('option');
        opt.value = f.filename;
        opt.textContent = `${f.run_id} - Suite: ${f.suite_name.toUpperCase()} (${f.passed}/${f.total} Passed - ${f.pass_rate}%)`;
        select.appendChild(opt);
      });
    })
    .catch(() => {});
}

function loadSelectedHistory() {
  const select = document.getElementById('qa-history-select');
  if (!select || !select.value) return;

  fetch(`/api/history?file=${encodeURIComponent(select.value)}`)
    .then(res => res.json())
    .then(data => {
      renderFullQASnapshot(data);
      const curLabel = document.getElementById('qa-current-test-name');
      if (curLabel) {
        curLabel.textContent = `Loaded report ${data.run_id} (${data.start_time})`;
      }
    })
    .catch(err => {
      alert('Failed to load selected history report.');
    });
}
