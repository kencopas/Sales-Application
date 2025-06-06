import { showModal, hideModal } from './modal.js';

let timeOnPageStart = Date.now();

// Wait for DOM to load before accessing elements
document.addEventListener('DOMContentLoaded', () => {
    const quoteBtn = document.getElementById('quoteBtn');
    const submitBtn = document.getElementById('submitBtn');
    const hideBtn = document.getElementById('hideBtn');

    quoteBtn.addEventListener('click', () => showModal('formModal'));
    submitBtn.addEventListener('click', sendUserInfo);
    hideBtn.addEventListener('click', () => hideModal('formModal'))

    trackClicks();
});

// Track user time
window.addEventListener('beforeunload', () => {
    const timeSpent = Date.now() - timeOnPageStart;
    sendUserEvent('time_spent', { milliseconds: timeSpent });
});

// Track every click on the page
function trackClicks() {
    document.addEventListener('click', (e) => {
        sendUserEvent('click', {
            element: e.target.tagName,
            id: e.target.id || null,
            class: e.target.className || null,
            timestamp: new Date().toISOString()
        });
    });
}

// Send analytics events
function sendUserEvent(type, payload) {
    fetch('/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, data: payload })
    }).catch(err => console.error('Tracking failed:', err));
}

// Send user form data
function sendUserInfo() {
    const result = {};
    const elementIds = ['first_name', 'last_name', 'email', 'phone_number', 'state', 'zipcode'];

    elementIds.forEach(id => {
        const el = document.getElementById(id);
        result[id] = el?.value.trim() || null;
    });

    fetch('/user_submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(result)
    }).catch(err => console.error('Form submission failed:', err));
}
