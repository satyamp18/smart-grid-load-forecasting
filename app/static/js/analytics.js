// Analytics Page JavaScript logic
let lineChartInstance = null;

async function loadAnalytics() {
    const zoneId = Number(document.getElementById('zone-select').value || 1);

    try {
        const [currentRes, peakRes, avgRes, historyRes] = await Promise.all([
            fetch(`${API_BASE}/analytics/current-load/${zoneId}`),
            fetch(`${API_BASE}/analytics/peak-load/${zoneId}`),
            fetch(`${API_BASE}/analytics/average-load/${zoneId}`),
            fetch(`${API_BASE}/analytics/history/${zoneId}`)
        ]);

        if (!currentRes.ok || !peakRes.ok || !avgRes.ok || !historyRes.ok) {
            throw new Error('Failed to load analytics data');
        }

        const currentData = await currentRes.json();
        const peakData = await peakRes.json();
        const avgData = await avgRes.json();
        const historyData = await historyRes.json();

        document.getElementById('current-load-val').innerText = Number(currentData.current_load_kw || 0).toFixed(2);
        document.getElementById('peak-load-val').innerText = Number(peakData.peak_load_kw || 0).toFixed(2);
        document.getElementById('avg-load-val').innerText = Number(avgData.average_load_kw || 0).toFixed(2);
        document.getElementById('history-count').innerText = historyData.length || 0;

        renderLineChart(historyData);
        renderHistoryTable(historyData);
    } catch (error) {
        console.error(error);
        showToast('Failed to load analytics', 'error');
    }
}

function renderLineChart(history) {
    const ctx = document.getElementById('powerLineChart').getContext('2d');
    if (lineChartInstance) lineChartInstance.destroy();

    lineChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: history.map(item => item.id),
            datasets: [{
                label: 'Power (kW)',
                data: history.map(item => item.power_kw),
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

function renderHistoryTable(history) {
    const tbody = document.getElementById('analytics-tbody');
    if (!history || history.length === 0) {
        tbody.innerHTML = `<tr><td colSpan="5">No Readings Found</td></tr>`;
        return;
    }

    tbody.innerHTML = history.map(item => `
        <tr>
            <td>${item.meter_id}</td>
            <td>${item.voltage}</td>
            <td>${item.current}</td>
            <td>${Number(item.power_kw || 0).toFixed(2)}</td>
            <td>${formatDate(item.timestamp)}</td>
        </tr>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    loadAnalytics();
    document.getElementById('zone-select').addEventListener('change', loadAnalytics);
});
