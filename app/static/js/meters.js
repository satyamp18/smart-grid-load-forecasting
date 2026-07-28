// Smart Meters Page JavaScript logic
let meters = [];
let zones = [];
let editingMeter = null;

async function loadData() {
    try {
        const [meterRes, zoneRes] = await Promise.all([
            fetch(`${API_BASE}/meters/`),
            fetch(`${API_BASE}/zones/`)
        ]);

        if (!meterRes.ok || !zoneRes.ok) throw new Error('Failed to fetch data');

        meters = await meterRes.json();
        zones = await zoneRes.json();

        populateZoneSelect();
        renderMeterTable();
    } catch (error) {
        console.error(error);
        showToast('Failed to load data', 'error');
    }
}

function getZoneName(id) {
    const zone = zones.find(z => z.id === id);
    return zone ? zone.zone_name : '-';
}

function populateZoneSelect() {
    const select = document.getElementById('zone_id');
    select.innerHTML = '<option value="">Select Zone</option>' +
        zones.map(z => `<option value="${z.id}">${z.zone_name}</option>`).join('');
}

function renderMeterTable() {
    const tbody = document.getElementById('meters-tbody');
    const searchValue = document.getElementById('search-box').value.toLowerCase();

    const filtered = meters.filter(m => 
        m.meter_code.toLowerCase().includes(searchValue)
    );

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colSpan="5" class="empty-row">No Smart Meters Found</td></tr>`;
        return;
    }

    tbody.innerHTML = filtered.map((meter, index) => `
        <tr>
            <td>${index + 1}</td>
            <td><strong>${meter.meter_code}</strong></td>
            <td>${getZoneName(meter.zone_id)}</td>
            <td><span class="status active">Active</span></td>
            <td>
                <button class="edit-btn" onclick="openModal(${meter.id})">✏️ Edit</button>
                <button class="delete-btn" onclick="deleteMeterItem(${meter.id})">🗑 Delete</button>
            </td>
        </tr>
    `).join('');
}

function openModal(id = null) {
    editingMeter = id ? meters.find(m => m.id === id) : null;
    const modal = document.getElementById('meter-modal');
    const modalTitle = document.getElementById('modal-title');
    const codeInput = document.getElementById('meter_code');
    const zoneSelect = document.getElementById('zone_id');
    const submitBtn = document.getElementById('submit-btn');

    if (editingMeter) {
        modalTitle.innerText = 'Edit Smart Meter';
        codeInput.value = editingMeter.meter_code;
        zoneSelect.value = editingMeter.zone_id;
        submitBtn.innerText = 'Update Meter';
    } else {
        modalTitle.innerText = 'Add Smart Meter';
        codeInput.value = '';
        zoneSelect.value = '';
        submitBtn.innerText = 'Add Meter';
    }

    modal.style.display = 'flex';
}

function closeModal() {
    editingMeter = null;
    document.getElementById('meter-modal').style.display = 'none';
}

async function handleFormSubmit(e) {
    e.preventDefault();
    const meter_code = document.getElementById('meter_code').value.trim();
    const zone_id = Number(document.getElementById('zone_id').value);

    const payload = { meter_code, zone_id };

    try {
        let response;
        if (editingMeter) {
            response = await fetch(`${API_BASE}/meters/${editingMeter.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } else {
            response = await fetch(`${API_BASE}/meters/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        }

        if (!response.ok) throw new Error('Operation failed');

        showToast(editingMeter ? 'Meter Updated Successfully' : 'Meter Added Successfully', 'success');
        closeModal();
        loadData();
    } catch (error) {
        console.error(error);
        showToast('Operation Failed', 'error');
    }
}

async function deleteMeterItem(id) {
    if (!confirm('Are you sure you want to delete this meter?')) return;
    try {
        const response = await fetch(`${API_BASE}/meters/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Delete failed');
        showToast('Meter Deleted Successfully', 'success');
        loadData();
    } catch (error) {
        console.error(error);
        showToast('Delete Failed', 'error');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadData();
    document.getElementById('search-box').addEventListener('input', renderMeterTable);
    document.getElementById('meter-form').addEventListener('submit', handleFormSubmit);
});
