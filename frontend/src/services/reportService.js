import axios from "axios";

const API =
`${import.meta.env.VITE_API_URL}/load-reports`;

export const getReports = async () => {
  const res = await axios.get(API);
  return res.data;
};

export const getReport = async (id) => {
  const res = await axios.get(`${API}/${id}`);
  return res.data;
};

export const createReport = async (data) => {
  const res = await axios.post(API, data);
  return res.data;
};