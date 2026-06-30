import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
} from "recharts";

function App() {
  const [meters, setMeters] = useState([]);
  const [zones, setZones] = useState([]);
  const [readings, setReadings] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/v1/meters")
      .then((res) => res.json())
      .then((data) => setMeters(data))
      .catch((err) => console.error(err));

    fetch("http://127.0.0.1:8000/api/v1/zones")
      .then((res) => res.json())
      .then((data) => setZones(data))
      .catch((err) => console.error(err));

    fetch("http://127.0.0.1:8000/api/v1/readings")
      .then((res) => res.json())
      .then((data) => setReadings(data))
      .catch((err) => console.error(err));
  }, []);

  const zoneData = zones.map((z) => ({
    zone: z.zone_name,
    load: z.max_capacity_kw,
  }));

  const historyData = readings.map((r) => ({
    day: `R${r.id}`,
    load: r.power_kw,
  }));

  return (
    <div
      style={{
        background: "#0f172a",
        minHeight: "100vh",
        color: "white",
        padding: "25px",
        fontFamily: "Arial",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: "30px" }}>
        Smart Grid Operations Center
      </h1>

      {/* Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4,1fr)",
          gap: "15px",
        }}
      >
        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "12px",
            textAlign: "center",
          }}
        >
          <h3>Active Meters</h3>
          <h2>{meters.length}</h2>
        </div>

        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "12px",
            textAlign: "center",
          }}
        >
          <h3>Zones</h3>
          <h2>{zones.length}</h2>
        </div>

        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "12px",
            textAlign: "center",
          }}
        >
          <h3>Readings</h3>
          <h2>{readings.length}</h2>
        </div>

        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "12px",
            textAlign: "center",
          }}
        >
          <h3>System Status</h3>
          <h2>Healthy</h2>
        </div>
      </div>

      {/* Charts */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "20px",
          marginTop: "25px",
        }}
      >
        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "12px",
            height: "350px",
          }}
        >
          <h3>Zone Capacity</h3>

          <ResponsiveContainer width="100%" height="90%">
            <BarChart data={zoneData}>
              <XAxis dataKey="zone" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="load" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div
          style={{
            background: "#1e293b",
            padding: "20px",
            borderRadius: "12px",
            height: "350px",
          }}
        >
          <h3>Power Readings</h3>

          <ResponsiveContainer width="100%" height="90%">
            <LineChart data={historyData}>
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="load" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Meter Table */}
      <div
        style={{
          marginTop: "25px",
          background: "#1e293b",
          padding: "20px",
          borderRadius: "12px",
        }}
      >
        <h3>Meter Data</h3>

        <table width="100%">
          <thead>
            <tr>
              <th>ID</th>
              <th>Meter Code</th>
              <th>Zone ID</th>
            </tr>
          </thead>

          <tbody>
            {meters.map((meter) => (
              <tr key={meter.id}>
                <td>{meter.id}</td>
                <td>{meter.meter_code}</td>
                <td>{meter.zone_id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Reading Table */}
      <div
        style={{
          marginTop: "25px",
          background: "#1e293b",
          padding: "20px",
          borderRadius: "12px",
        }}
      >
        <h3>Latest Readings</h3>

        <table width="100%">
          <thead>
            <tr>
              <th>ID</th>
              <th>Meter ID</th>
              <th>Voltage</th>
              <th>Current</th>
              <th>Power</th>
            </tr>
          </thead>

          <tbody>
            {readings.map((r) => (
              <tr key={r.id}>
                <td>{r.id}</td>
                <td>{r.meter_id}</td>
                <td>{r.voltage}</td>
                <td>{r.current}</td>
                <td>{r.power_kw}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div
        style={{
          marginTop: "20px",
          textAlign: "center",
          fontSize: "20px",
        }}
      >
        🟢 Backend Connected Successfully
      </div>
    </div>
  );
}

export default App;