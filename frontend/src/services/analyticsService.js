import axios from "axios";

const API_URL =
`${import.meta.env.VITE_API_URL}/analytics`;

export const getCurrentLoad = async (zoneId) => {
  const { data } = await axios.get(
    `${API_URL}/current-load/${zoneId}`
  );
  return data;
};

export const getPeakLoad = async (zoneId) => {
  const { data } = await axios.get(
    `${API_URL}/peak-load/${zoneId}`
  );
  return data;
};

export const getAverageLoad = async (zoneId) => {
  const { data } = await axios.get(
    `${API_URL}/average-load/${zoneId}`
  );
  return data;
};

export const getHistory = async (zoneId) => {
  const { data } = await axios.get(
    `${API_URL}/history/${zoneId}`
  );
  return data;
};