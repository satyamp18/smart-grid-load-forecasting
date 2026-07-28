// Load Reports Page JavaScript logic
let reports = [];

async function loadReports() {
    try {
        const response = await fetch(`${API_BASE}/load-reports/`);
        if (!response.ok) throw new Error('Failed to load reports');
        reports = await response.json();

        document.getElementById('total-reports-count').innerText = reports.length;
        renderReportsTable();
    } catch (error) {
        console.error(error);
        showToast('Failed to load reports', 'error');
    }
}

function renderReportsTable() {
    const container = document.getElementById('reports-table-container');

    if (reports.length === 0) {
        container.innerHTML = `<p style="padding: 40px; text-align: center; color: #64748b;">No Reports Found</p>`;
        return;
    }

    container.innerHTML = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Zone</th>
                    <th>Total Load (kW)</th>
                    <th>Report Time</th>
                </tr>
            </thead>
            <tbody>
                ${reports.map(r => `
                    <tr>
                        <td>${r.id}</td>
                        <td>${r.zone_id}</td>
                        <td>${r.total_load_kw}</td>
                        <td>${formatDate(r.report_time)}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

async function handleReportFormSubmit(e) {
    e.preventDefault();
    const zone_id = Number(document.getElementById('zone_id').value);
    const total_load_kw = Number(document.getElementById('total_load_kw').value);
    const report_time = document.getElementById('report_time').value;

    if (!zone_id || !total_load_kw || !report_time) {
        showToast('Please fill all fields', 'warning');
        return;
    }

    const payload = {
        zone_id,
        total_load_kw,
        report_time: new Date(report_time).toISOString()
    };

    try {
        const response = await fetch(`${API_BASE}/load-reports/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Failed to create report');

        showToast('Report Added Successfully', 'success');
        document.getElementById('report-form').reset();
        loadReports();
    } catch (error) {
        console.error(error);
        showToast('Unable to create report', 'error');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadReports();
    document.getElementById('refresh-btn').addEventListener('click', loadReports);
    document.getElementById('report-form').addEventListener('submit', handleReportFormSubmit);
});
