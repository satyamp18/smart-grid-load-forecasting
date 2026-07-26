import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000/api/v1",
    headers: {
        "Content-Type": "application/json",
    },
});

// =========================
// Get All Alerts
// =========================
export const getAllAlerts = async () => {
    const response = await API.get("/alerts");
    return response.data;
};

// =========================
// Get Alert By ID
// =========================
export const getAlertById = async (id) => {
    const response = await API.get(`/alerts/${id}`);
    return response.data;
};

// =========================
// Create Alert
// =========================
export const createAlert = async (alertData) => {
    const response = await API.post("/alerts", alertData);
    return response.data;
};

// =========================
// Update Alert Status
// =========================
export const updateAlertStatus = async (id, status) => {
    const response = await API.patch(`/alerts/${id}`, {
        status,
    });

    return response.data;
};

// =========================
// Delete Alert
// =========================
export const deleteAlert = async (id) => {
    const response = await API.delete(`/alerts/${id}`);
    return response.data;
};

// =========================
// Default Export
// =========================
const alertService = {
    getAllAlerts,
    getAlertById,
    createAlert,
    updateAlertStatus,
    deleteAlert,
};

export default alertService;