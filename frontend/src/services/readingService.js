import axios from "axios";

const API_URL =
`${import.meta.env.VITE_API_URL}/readings`;

export const getReadings = async () => {
  const response = await axios.get(API_URL);
  return response.data;
};

export const getReading = async (id) => {
  const response = await axios.get(`${API_URL}/${id}`);
  return response.data;
};

export const createReading = async (readingData) => {
  const response = await axios.post(API_URL, readingData);
  return response.data;
};

export const updateReading = async (id, readingData) => {
  const response = await axios.put(`${API_URL}/${id}`, readingData);
  return response.data;
};

export const deleteReading = async (id) => {
  const response = await axios.delete(`${API_URL}/${id}`);
  return response.data;
};