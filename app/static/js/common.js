// Common helper functions for Smart Grid Frontend

const API_BASE = '/api/v1';

// Toast Notification
function showToast(message, type = 'info') {
    if (window.Toastify) {
        let bg = '#2563eb';
        if (type === 'success') bg = '#16a34a';
        if (type === 'error') bg = '#dc2626';
        if (type === 'warning') bg = '#f59e0b';

        Toastify({
            text: message,
            duration: 3000,
            gravity: 'top',
            position: 'right',
            style: { background: bg, borderRadius: '8px', color: '#ffffff' }
        }).showToast();
    } else {
        alert(message);
    }
}

// Highlight active sidebar navigation
document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar nav a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
});

// Format Date string
function formatDate(dateStr) {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleString();
}
