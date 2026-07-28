// Meter Readings Page JavaScript logic
let readings = [];
let selectedReading = null;

async function loadReadings() {
    try {
        const response = await fetch(`${API_BASE}/readings/`);
        if (!response.ok) throw new Error('Failed to load readings');
        readings = await response.json();
        updateStats();
        renderReadingsTable();
    } catch (error) {
        console.error(error);
        showToast('Failed to load readings', 'error');
    }
}

function updateStats() {
    document.getElementById('total-readings-count').innerText = readings.length;
    const totalKw = readings.reduce((sum, item) => sum + (item.power_kw || 0), 0);
    document.getElementById('total-kw-val').innerText = totalKw.toFixed(2);
}

function renderReadingsTable() {
    const tbody = document.getElementById('readings-tbody');
    const searchValue = document.getElementById('search-box').value.toLowerCase();

    const filtered = readings.filter(r => 
        r.meter_id.toString().includes(searchValue)
    );

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colSpan="7" class="empty-state">No readings found.</td></tr>`;
        return;
    }

    tbody.innerHTML = filtered.map(r => `
        <tr>
            <td>${r.id}</td>
            <td>${r.meter_id}</td>
            <td>${r.voltage} V</td>
            <td>${r.current} A</td>
            <td>${Number(r.power_kw || 0).toFixed(2)} kW</td>
            <td>${formatDate(r.timestamp)}</td>
            <td>
                <button class="edit-btn" onclick="openModal(${r.id})">✏ Edit</button>
                <button class="delete-btn" onclick="deleteReadingItem(${r.id})">🗑 Delete</button>
            </td>
        </tr>
    `).join('');
}

function updatePowerPreview() {
    const v = Number(document.getElementById('voltage').value || 0);
    const c = Number(document.getElementById('current').value || 0);
    const power = (v * c) / 1000;
    document.getElementById('power_preview').value = power.toFixed(2);
}

function openModal(id = null) {
    selectedReading = id ? readings.find(r => r.id === id) : null;
    const modal = document.getElementById('reading-modal');
    const modalTitle = document.getElementById('modal-title');
    const meterInput = document.getElementById('meter_id');
    const voltageInput = document.getElementById('voltage');
    const currentInput = document.getElementById('current');
    const timestampInput = document.getElementById('timestamp');
    const submitBtn = document.getElementById('submit-btn');

    if (selectedReading) {
        modalTitle.innerText = 'Edit Reading';
        meterInput.value = selectedReading.meter_id;
        voltageInput.value = selectedReading.voltage;
        currentInput.value = selectedReading.current;
        timestampInput.value = selectedReading.timestamp ? selectedReading.timestamp.slice(0, 16) : '';
        submitBtn.innerText = 'Update';
    } else {
        modalTitle.innerText = 'Add Reading';
        meterInput.value = '';
        voltageInput.value = '';
        currentInput.value = '';
        timestampInput.value = '';
        submitBtn.innerText = 'Save';
    }

    updatePowerPreview();
    modal.style.display = 'flex';
}

function closeModal() {
    selectedReading = null;
    document.getElementById('reading-modal').style.display = 'none';
}

async function handleFormSubmit(e) {
    e.preventDefault();
    const meter_id = Number(document.getElementById('meter_id').value);
    const voltage = Number(document.getElementById('voltage').value);
    const current = Number(document.getElementById('current').value);
    const rawTime = document.getElementById('timestamp').value;

    if (!meter_id || !voltage || !current || !rawTime) {
        showToast('Please fill all fields', 'warning');
        return;
    }

    const payload = {
        meter_id,
        voltage,
        current,
        timestamp: new Date(rawTime).toISOString()
    };

    try {
        let response;
        if (selectedReading) {
            response = await fetch(`${API_BASE}/readings/${selectedReading.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } else {
            response = await fetch(`${API_BASE}/readings/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        }

        if (!response.ok) throw new Error('Operation failed');

        showToast(selectedReading ? 'Reading updated successfully' : 'Reading added successfully', 'success');
        closeModal();
        loadReadings();
    } catch (error) {
        console.error(error);
        showToast('Operation failed', 'error');
    }
}

async function deleteReadingItem(id) {
    if (!confirm('Delete this reading?')) return;
    try {
        const response = await fetch(`${API_BASE}/readings/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Delete failed');
        showToast('Reading deleted successfully', 'success');
        loadReadings();
    } catch (error) {
        console.error(error);
        showToast('Unable to delete reading', 'error');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadReadings();
    document.getElementById('search-box').addEventListener('input', renderReadingsTable);
    document.getElementById('voltage').addEventListener('input', updatePowerPreview);
    document.getElementById('current').addEventListener('input', updatePowerPreview);
    document.getElementById('reading-form').addEventListener('submit', handleFormSubmit);
});
