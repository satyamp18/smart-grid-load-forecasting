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
  FaCheckCircle,
  FaChartLine,
  FaBatteryHalf,
} from "react-icons/fa";

function Dashboard() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard();

    const interval = setInterval(() => {
      fetchDashboard();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await api.get("/dashboard/summary");

      console.log("Dashboard Response:", response.data);

      setDashboard(response.data);
    } catch (error) {
      console.error("Dashboard API Error:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  if (!dashboard) return <h2>No Dashboard Data Found</h2>;

  const loadData = [
    {
      zone: "Current Load",
      load: Number(dashboard.total_load_kw),
    },
    {
      zone: "Utilization",
      load: Number(dashboard.overall_utilization),
    },
  ];

  const alertData = [
    {
      name: "Active",
      value: dashboard.active_alerts,
    },
    {
      name: "Resolved",
      value: dashboard.resolved_alerts,
    },
  ];

  return (
    <div>
      <div
        style={{
          background: "#fff",
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

      <div className="dashboard-grid">
        <DashboardCard
          title="Zones"
          value={dashboard.total_zones}
          icon={<FaMapMarkedAlt />}
          color="linear-gradient(135deg,#2563EB,#60A5FA)"
        />

        <DashboardCard
          title="Smart Meters"
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
          title="Active Alerts"
          value={dashboard.active_alerts}
          icon={<FaExclamationTriangle />}
          color="linear-gradient(135deg,#DC2626,#FB7185)"
        />

        <DashboardCard
          title="Resolved Alerts"
          value={dashboard.resolved_alerts}
          icon={<FaCheckCircle />}
          color="linear-gradient(135deg,#10B981,#34D399)"
        />

        <DashboardCard
          title="Total Load"
          value={`${Number(dashboard.total_load_kw).toFixed(2)} kW`}
          icon={<FaBatteryHalf />}
          color="linear-gradient(135deg,#7C3AED,#A855F7)"
        />

        <DashboardCard
          title="Utilization"
          value={`${Number(dashboard.overall_utilization).toFixed(2)}%`}
          icon={<FaChartLine />}
          color="linear-gradient(135deg,#F59E0B,#FBBF24)"
        />
      </div>

      <div className="chart-grid">
        <LoadBarChart data={loadData} />
        <StatsPieChart data={alertData} />
      </div>
    </div>
  );
}

export default Dashboard;