import api from "./api";

export const getMeters = async () => {
  const res = await api.get("/meters");
  return res.data;
};

export const getMeter = async (id) => {
  const res = await api.get(`/meters/${id}`);
  return res.data;
};

export const createMeter = async (meter) => {
  const res = await api.post("/meters", meter);
  return res.data;
};

export const updateMeter = async (id, meter) => {
  const res = await api.put(`/meters/${id}`, meter);
  return res.data;
};

export const deleteMeter = async (id) => {
  await api.delete(`/meters/${id}`);
};