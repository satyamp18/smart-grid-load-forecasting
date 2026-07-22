import { useEffect, useState } from "react";
import api from "../services/api";
import DashboardCard from "../components/DashboardCard";
import Loading from "../components/Loading";
import "../assets/styles/cards.css";
import "../styles/Dashboard.css";
import LoadBarChart from "../components/charts/LoadBarChart";
import StatsPieChart from "../components/charts/StatsPieChart";

import {
  FaMapMarkedAlt,
  FaBolt,
  FaDatabase,
  FaExclamationTriangle,
} from "react-icons/fa";
const loadData = [
  { zone: "North", load: 420 },
  { zone: "South", load: 310 },
  { zone: "East", load: 520 },
  { zone: "West", load: 390 },
];

const meterData = [
  { name: "North", value: 3 },
  { name: "South", value: 2 },
  { name: "East", value: 2 },
  { name: "West", value: 2 },
];

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await api.get("/dashboard/summary");
      setDashboard(response.data);
    } catch (error) {
      console.error("Dashboard API Error:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
  }

  if (!dashboard) {
    return <h2>No Dashboard Data Found</h2>;
  }

  return (
    <div>

      {/* Welcome Section */}

      <div
        style={{
          background: "white",
          padding: "25px",
          borderRadius: "18px",
          marginBottom: "25px",
          boxShadow: "0 8px 20px rgba(0,0,0,.08)",
        }}
      >
        <h1>Welcome Admin 👋</h1>

        <p style={{ color: "#64748B" }}>
          Monitor Smart Grid performance, zones, meters and energy usage in
          real time.
        </p>
      </div>

      {/* Dashboard Cards */}

      <div className="dashboard-grid">

        <DashboardCard
          title="Zones"
          value={dashboard.total_zones}
          icon={<FaMapMarkedAlt />}
          color="linear-gradient(135deg,#2563EB,#60A5FA)"
        />

        <DashboardCard
          title="Meters"
          value={dashboard.total_meters}
          icon={<FaBolt />}
          color="linear-gradient(135deg,#16A34A,#4ADE80)"
        />

        <DashboardCard
          title="Readings"
          value={dashboard.total_readings}
          icon={<FaDatabase />}
          color="linear-gradient(135deg,#9333EA,#C084FC)"
        />

        <DashboardCard
          title="Alerts"
          value={dashboard.total_alerts}
          icon={<FaExclamationTriangle />}
          color="linear-gradient(135deg,#DC2626,#FB7185)"
        />

        <DashboardCard
          title="Total Load"
          value={`${dashboard.total_load_kw?.toFixed(2)} kW`}
          icon={<FaBolt />}
          color="linear-gradient(135deg,#7C3AED,#A855F7)"
        />

      </div>
      <div className="chart-grid">

        <LoadBarChart data={loadData} />

        <StatsPieChart data={meterData} />

      </div>

    </div>
  );
}

export default Dashboard;