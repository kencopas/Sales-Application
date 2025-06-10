import { showModal, hideModal } from './modal.js';

let timeOnPageStart = Date.now();

// Wait for DOM to load before accessing elements
document.addEventListener('DOMContentLoaded', () => {
    // const quoteBtn = document.getElementById('quoteBtn');
    const submitBtn = document.getElementById('submitBtn');
    const calendlyBtn = document.getElementById('calendlyBtn');
    // const hideBtn = document.getElementById('hideBtn');

    // quoteBtn.addEventListener('click', () => showModal('formModal'));
    submitBtn.addEventListener('click', sendUserInfo);
    calendlyBtn.addEventListener('click', calendlyRedirect);
    // hideBtn.addEventListener('click', () => hideModal('formModal'))

    trackClicks();
});

// Track user time
window.addEventListener('beforeunload', () => {
    const timeSpent = Date.now() - timeOnPageStart;
    sendUserEvent('time_spent', { milliseconds: timeSpent });
});

// Track every click on the page
function trackClicks() {
    console.log('trackClicks()')
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
    console.log(
        'sendUserEvent(\n',
        '    type=' + type + '\n',
        '    payload=' + payload + '\n'
    )
    fetch('/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, data: payload })
    }).catch(err => console.error('Tracking failed:', err));
}

function calendlyRedirect() {
    console.log('calendlyRedirect()')
    window.location.href = "/book";
}
