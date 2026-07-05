import axios from "axios";

export const getZones = async () => {
  const res = await axios.get("http://127.0.0.1:8000/api/v1/zones");
  return res.data.zones;
};