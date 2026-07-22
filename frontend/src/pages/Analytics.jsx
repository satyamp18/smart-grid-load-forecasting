import { useEffect, useState } from "react";
import { toast } from "react-toastify";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  getCurrentLoad,
  getPeakLoad,
  getAverageLoad,
  getHistory,
} from "../services/analyticsService";

import "../styles/analytics.css";

function Analytics() {
  const [zoneId, setZoneId] = useState(1);

  const [currentLoad, setCurrentLoad] = useState(0);
  const [peakLoad, setPeakLoad] = useState(0);
  const [averageLoad, setAverageLoad] = useState(0);

  const [history, setHistory] = useState([]);

  const loadAnalytics = async () => {
    try {
      const [
        current,
        peak,
        average,
        historyData,
      ] = await Promise.all([
        getCurrentLoad(zoneId),
        getPeakLoad(zoneId),
        getAverageLoad(zoneId),
        getHistory(zoneId),
      ]);

      setCurrentLoad(current.current_load_kw);
      setPeakLoad(peak.peak_load_kw);
      setAverageLoad(average.average_load_kw);
      setHistory(historyData);
    } catch (err) {
      toast.error("Failed to load analytics");
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, [zoneId]);

  return (
    <div className="analytics-page">

      <div className="analytics-header">

        <div>
          <h2>Analytics Dashboard</h2>
          <p>Monitor smart grid power analytics.</p>
        </div>

        <select
          value={zoneId}
          onChange={(e) =>
            setZoneId(Number(e.target.value))
          }
        >
          <option value={1}>Zone 1</option>
          <option value={2}>Zone 2</option>
          <option value={3}>Zone 3</option>
        </select>

      </div>

      <div className="analytics-cards">

        <div className="analytics-card">
          <h3>{currentLoad.toFixed(2)}</h3>
          <span>Current Load (kW)</span>
        </div>

        <div className="analytics-card">
          <h3>{peakLoad.toFixed(2)}</h3>
          <span>Peak Load (kW)</span>
        </div>

        <div className="analytics-card">
          <h3>{averageLoad.toFixed(2)}</h3>
          <span>Average Load (kW)</span>
        </div>

        <div className="analytics-card">
          <h3>{history.length}</h3>
          <span>Total Readings</span>
        </div>

      </div>

      <div className="chart-card">

        <h3>Power Trend</h3>

        <ResponsiveContainer
          width="100%"
          height={350}
        >

          <LineChart data={history}>

            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="id"
            />

            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="power_kw"
              stroke="#2563eb"
              strokeWidth={3}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

      <div className="table-card">

        <h3>Recent Readings</h3>

        <table>

          <thead>

            <tr>
              <th>Meter</th>
              <th>Voltage</th>
              <th>Current</th>
              <th>Power</th>
              <th>Time</th>
            </tr>

          </thead>

          <tbody>

            {history.map((item) => (

              <tr key={item.id}>

                <td>{item.meter_id}</td>

                <td>{item.voltage}</td>

                <td>{item.current}</td>

                <td>{item.power_kw.toFixed(2)}</td>

                <td>
                  {new Date(
                    item.timestamp
                  ).toLocaleString()}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}

export default Analytics;