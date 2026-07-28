// Dashboard JavaScript logic
let barChartInstance = null;
let pieChartInstance = null;

async function fetchDashboard() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/summary`);
        if (!response.ok) throw new Error('Failed to fetch dashboard summary');
        const data = await response.json();

        // Update Summary Cards
        document.getElementById('total-zones').innerText = data.total_zones ?? 0;
        document.getElementById('total-meters').innerText = data.total_meters ?? 0;
        document.getElementById('total-readings').innerText = data.total_readings ?? 0;
        document.getElementById('active-alerts').innerText = data.active_alerts ?? 0;
        document.getElementById('resolved-alerts').innerText = data.resolved_alerts ?? 0;
        document.getElementById('total-load').innerText = `${Number(data.total_load_kw || 0).toFixed(2)} kW`;
        document.getElementById('utilization').innerText = `${Number(data.overall_utilization || 0).toFixed(2)}%`;

        // Render Load Bar Chart
        renderBarChart([
            { label: 'Current Load', value: Number(data.total_load_kw || 0) },
            { label: 'Utilization', value: Number(data.overall_utilization || 0) }
        ]);

        // Render Alert Pie Chart
        renderPieChart([
            { label: 'Active', value: data.active_alerts || 0 },
            { label: 'Resolved', value: data.resolved_alerts || 0 }
        ]);

    } catch (error) {
        console.error('Dashboard Error:', error);
        showToast('Failed to load dashboard data', 'error');
    }
}

function renderBarChart(chartData) {
    const ctx = document.getElementById('loadBarChart').getContext('2d');
    if (barChartInstance) barChartInstance.destroy();

    barChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.map(d => d.label),
            datasets: [{
                label: 'kW / %',
                data: chartData.map(d => d.value),
                backgroundColor: '#2563EB',
                borderRadius: 8
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

function renderPieChart(chartData) {
    const ctx = document.getElementById('statsPieChart').getContext('2d');
    if (pieChartInstance) pieChartInstance.destroy();

    pieChartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartData.map(d => d.label),
            datasets: [{
                data: chartData.map(d => d.value),
                backgroundColor: ['#EF4444', '#22C55E']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchDashboard();
    setInterval(fetchDashboard, 30000);
});
