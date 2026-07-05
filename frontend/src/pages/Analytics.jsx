import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function Analytics() {
  const [data, setData] = useState([]);

  const fetchZones = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/api/v1/zones"
      );

      const formatted = (res.data.zones || []).map((z) => ({
        name: z.zone_name,
        capacity: z.max_capacity_kw,
      }));

      setData(formatted);
    } catch (err) {
      console.log("Error fetching data:", err);
    }
  };

  useEffect(() => {
    fetchZones();

    // auto refresh every 5 sec (LIVE DASHBOARD)
    const interval = setInterval(() => {
      fetchZones();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>📊 Smart Grid Analytics Dashboard</h2>

      <p>Total Zones: {data.length}</p>

      <div style={{ width: "100%", height: 350 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="capacity" fill="#4f46e5" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}