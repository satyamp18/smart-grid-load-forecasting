import {
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function LoadBarChart({ data }) {
  return (
    <div className="chart-card">

      <h3>Zone Load Distribution</h3>

      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="zone" />
          <YAxis />
          <Tooltip />
          <Bar
            dataKey="load"
            fill="#2563EB"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>

    </div>
  );
}

export default LoadBarChart;