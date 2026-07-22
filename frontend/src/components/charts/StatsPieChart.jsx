import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = [
  "#2563EB",
  "#22C55E",
  "#F59E0B",
  "#EF4444",
];

function StatsPieChart({ data }) {

  return (

    <div className="chart-card">

      <h3>Meter Distribution</h3>

      <ResponsiveContainer width="100%" height={320}>

        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            outerRadius={110}
            label
          >

            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
              />
            ))}

          </Pie>

          <Tooltip />

        </PieChart>

      </ResponsiveContainer>

    </div>

  );

}

export default StatsPieChart;