// Zones Page JavaScript logic
let zones = [];
let selectedZone = null;

async function loadZones() {
    try {
        const response = await fetch(`${API_BASE}/zones/`);
        if (!response.ok) throw new Error('Failed to load zones');
        zones = await response.json();
        renderZoneTable();
    } catch (error) {
        console.error(error);
        showToast('Failed to load zones', 'error');
    }
}

function renderZoneTable() {
    const tbody = document.getElementById('zones-tbody');
    const searchValue = document.getElementById('search-box').value.toLowerCase();
    
    const filtered = zones.filter(zone => 
        zone.zone_name.toLowerCase().includes(searchValue)
    );

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colSpan="5" class="empty-row">No Zones Found</td></tr>`;
        return;
    }

    tbody.innerHTML = filtered.map((zone, index) => `
        <tr>
            <td>${index + 1}</td>
            <td><strong>${zone.zone_name}</strong></td>
            <td>${zone.max_capacity_kw} KW</td>
            <td><span class="status active">Active</span></td>
            <td>
                <button class="edit-btn" onclick="openModal(${zone.id})">✏️ Edit</button>
                <button class="delete-btn" onclick="deleteZoneItem(${zone.id})">🗑 Delete</button>
            </td>
        </tr>
    `).join('');
}

function openModal(id = null) {
    selectedZone = id ? zones.find(z => z.id === id) : null;
    const modal = document.getElementById('zone-modal');
    const modalTitle = document.getElementById('modal-title');
    const nameInput = document.getElementById('zone_name');
    const capacityInput = document.getElementById('max_capacity_kw');
    const submitBtn = document.getElementById('submit-btn');

    if (selectedZone) {
        modalTitle.innerText = 'Edit Zone';
        nameInput.value = selectedZone.zone_name;
        capacityInput.value = selectedZone.max_capacity_kw;
        submitBtn.innerText = 'Update Zone';
    } else {
        modalTitle.innerText = 'Add Zone';
        nameInput.value = '';
        capacityInput.value = '';
        submitBtn.innerText = 'Add Zone';
    }

    modal.style.display = 'flex';
}

function closeModal() {
    selectedZone = null;
    document.getElementById('zone-modal').style.display = 'none';
}

async function handleFormSubmit(e) {
    e.preventDefault();
    const zone_name = document.getElementById('zone_name').value.trim();
    const max_capacity_kw = Number(document.getElementById('max_capacity_kw').value);

    const payload = { zone_name, max_capacity_kw };

    try {
        let response;
        if (selectedZone) {
            response = await fetch(`${API_BASE}/zones/${selectedZone.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        } else {
            response = await fetch(`${API_BASE}/zones/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        }

        if (!response.ok) throw new Error('Operation failed');
        
        showToast(selectedZone ? 'Zone Updated Successfully' : 'Zone Added Successfully', 'success');
        closeModal();
        loadZones();
    } catch (error) {
        console.error(error);
        showToast('Operation Failed', 'error');
    }
}

async function deleteZoneItem(id) {
    if (!confirm('Delete this zone?')) return;
    try {
        const response = await fetch(`${API_BASE}/zones/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Delete failed');
        showToast('Zone Deleted Successfully', 'success');
        loadZones();
    } catch (error) {
        console.error(error);
        showToast('Delete Failed', 'error');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loadZones();
    document.getElementById('search-box').addEventListener('input', renderZoneTable);
    document.getElementById('zone-form').addEventListener('submit', handleFormSubmit);
});
