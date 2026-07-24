import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const crimeData = [
  {
    month: "Jan",
    crimes: 120,
    solved: 90,
  },
  {
    month: "Feb",
    crimes: 180,
    solved: 140,
  },
  {
    month: "Mar",
    crimes: 150,
    solved: 115,
  },
  {
    month: "Apr",
    crimes: 240,
    solved: 180,
  },
  {
    month: "May",
    crimes: 220,
    solved: 170,
  },
  {
    month: "Jun",
    crimes: 310,
    solved: 255,
  },
  {
    month: "Jul",
    crimes: 280,
    solved: 230,
  },
];

export default function CrimeTrendChart() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg h-[400px]">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-bold text-white">
            Crime Trend Analysis
          </h2>

          <p className="text-slate-400 text-sm mt-1">
            Monthly crime vs solved cases
          </p>
        </div>
      </div>

      <ResponsiveContainer width="100%" height="82%">
        <LineChart data={crimeData}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#334155"
          />

          <XAxis
            dataKey="month"
            stroke="#94a3b8"
          />

          <YAxis
            stroke="#94a3b8"
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "#0f172a",
              border: "1px solid #334155",
              borderRadius: "10px",
              color: "#fff",
            }}
          />

          <Legend />

          <Line
            type="monotone"
            dataKey="crimes"
            stroke="#3b82f6"
            strokeWidth={3}
            dot={{ r: 5 }}
            activeDot={{ r: 8 }}
            name="Total Crimes"
          />

          <Line
            type="monotone"
            dataKey="solved"
            stroke="#22c55e"
            strokeWidth={3}
            dot={{ r: 5 }}
            activeDot={{ r: 8 }}
            name="Solved Cases"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
