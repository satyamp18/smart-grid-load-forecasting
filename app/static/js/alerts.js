// Alert Management Page JavaScript logic & WebSocket handler
let alerts = [];
let socket = null;

async function loadAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts/`);
        if (!response.ok) throw new Error('Failed to load alerts');
        alerts = await response.json();
        updateSummaryCards();
        renderAlertsTable();
    } catch (error) {
        console.error(error);
        showToast('Failed to load alerts', 'error');
    }
}

function updateSummaryCards() {
    document.getElementById('total-alerts').innerText = alerts.length;
    document.getElementById('critical-alerts').innerText = alerts.filter(a => a.severity === 'HIGH' || a.severity === 'CRITICAL').length;
    document.getElementById('active-alerts').innerText = alerts.filter(a => a.status === 'ACTIVE').length;
    document.getElementById('resolved-alerts').innerText = alerts.filter(a => a.status === 'RESOLVED').length;
}

function renderAlertsTable() {
    const container = document.getElementById('table-content-container');
    const searchValue = document.getElementById('search-box').value.toLowerCase();
    const severityFilter = document.getElementById('severity-filter').value;
    const statusFilter = document.getElementById('status-filter').value;

    const filtered = alerts.filter(alert => {
        const searchMatch = alert.message.toLowerCase().includes(searchValue) || String(alert.zone_id).includes(searchValue);
        const severityMatch = severityFilter === 'ALL' || alert.severity === severityFilter;
        const statusMatch = statusFilter === 'ALL' || alert.status === statusFilter;
        return searchMatch && severityMatch && statusMatch;
    });

    if (filtered.length === 0) {
        container.innerHTML = `<div class="empty-state"><h2>No Alerts Found</h2></div>`;
        return;
    }

    container.innerHTML = `
        <div class="table-container">
            <table class="alerts-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Zone</th>
                        <th>Message</th>
                        <th>Severity</th>
                        <th>Status</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${filtered.map(alert => `
                        <tr>
                            <td>${alert.id}</td>
                            <td>Zone ${alert.zone_id}</td>
                            <td>${alert.message}</td>
                            <td><span class="severity ${alert.severity.toLowerCase()}">${alert.severity}</span></td>
                            <td><span class="status ${alert.status.toLowerCase()}">${alert.status}</span></td>
                            <td>${formatDate(alert.created_at)}</td>
                            <td>
                                ${alert.status === 'ACTIVE' ? `<button class="resolve-btn" onclick="resolveAlert(${alert.id})">Resolve</button>` : ''}
                                <button class="delete-btn" onclick="deleteAlertItem(${alert.id})">Delete</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

async function resolveAlert(id) {
    try {
        const response = await fetch(`${API_BASE}/alerts/${id}/status?status=RESOLVED`, {
            method: 'PUT'
        });
        if (!response.ok) throw new Error('Failed to resolve alert');
        showToast('Alert resolved', 'success');
        loadAlerts();
    } catch (error) {
        console.error(error);
        showToast('Unable to update alert', 'error');
    }
}

async function deleteAlertItem(id) {
    if (!confirm('Delete this alert?')) return;
    try {
        const response = await fetch(`${API_BASE}/alerts/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete alert');
        showToast('Alert deleted', 'success');
        loadAlerts();
    } catch (error) {
        console.error(error);
        showToast('Unable to delete alert', 'error');
    }
}

function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/alerts`;

    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        console.log('Alert WebSocket Connected');
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === 'NEW_ALERT') {
                showToast('⚠ New Alert Received', 'warning');
                loadAlerts();
            }
        } catch (err) {
            console.error('WebSocket parsing error:', err);
        }
    };

    socket.onclose = () => {
        console.log('Alert WebSocket Closed. Reconnecting in 5s...');
        setTimeout(initWebSocket, 5000);
    };

    socket.onerror = (err) => {
        console.error('Alert WebSocket Error:', err);
    };
}

document.addEventListener('DOMContentLoaded', () => {
    loadAlerts();
    initWebSocket();
    document.getElementById('refresh-btn').addEventListener('click', loadAlerts);
    document.getElementById('search-box').addEventListener('input', renderAlertsTable);
    document.getElementById('severity-filter').addEventListener('change', renderAlertsTable);
    document.getElementById('status-filter').addEventListener('change', renderAlertsTable);
});
