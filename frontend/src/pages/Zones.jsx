import { useEffect, useState } from "react";
import axios from "axios";

export default function Zones() {
  const [zones, setZones] = useState([]);

  // Smart status logic
  const getStatus = (capacity) => {
    if (capacity >= 1000) return "🔴 Overload";
    if (capacity >= 800) return "⚠️ Warning";
    return "🟢 Safe";
  };

  // Fetch zones from backend
  const fetchZones = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/api/v1/zones"
      );

      setZones(res.data);
    } catch (err) {
      console.log("API Error:", err);
      setZones([]);
    }
  };

  // initial load + auto refresh
  useEffect(() => {
    fetchZones();

    const interval = setInterval(() => {
      fetchZones();
    }, 5000); // live refresh

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>⚡ Zones Dashboard</h2>

      <h3>Total Zones: {zones.length}</h3>

      <button onClick={fetchZones} style={{ marginBottom: "10px" }}>
        🔄 Refresh
      </button>

      <table border="1" cellPadding="10" width="100%">
        <thead>
          <tr>
            <th>ID</th>
            <th>Zone Name</th>
            <th>Max Capacity (kW)</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {zones.length === 0 ? (
            <tr>
              <td colSpan="4">No Zones Found</td>
            </tr>
          ) : (
            zones.map((z) => (
              <tr key={z.id}>
                <td>{z.id}</td>
                <td>{z.zone_name}</td>
                <td>{z.max_capacity_kw}</td>
                <td>{getStatus(z.max_capacity_kw)}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
