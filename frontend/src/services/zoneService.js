import api from "./api";

// Get all zones
export const getZones = async () => {
    const response = await api.get("/zones");
    return response.data;
};

// Get single zone
export const getZone = async (id) => {
    const response = await api.get(`/zones/${id}`);
    return response.data;
};

// Create zone
export const createZone = async (zoneData) => {
    const response = await api.post("/zones", zoneData);
    return response.data;
};

// Update zone
export const updateZone = async (id, zoneData) => {
    const response = await api.put(`/zones/${id}`, zoneData);
    return response.data;
};

// Delete zone
export const deleteZone = async (id) => {
    const response = await api.delete(`/zones/${id}`);
    return response.data;
};