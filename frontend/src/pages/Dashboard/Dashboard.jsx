import { useState, useEffect } from "react";
import {
  ShieldAlert,
  CheckCircle2,
  MapPinned,
  Users,
  FileText,
  Brain,
  Loader2
} from "lucide-react";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import api from "../../services/api";
import HeroBanner from "../../components/dashboard/HeroBanner";
import StatsCard from "../../components/dashboard/StatsCard";
import ChartCard from "../../components/dashboard/ChartCard";
import AlertCard from "../../components/dashboard/AlertCard";

const iconMap = {
  ShieldAlert,
  CheckCircle2,
  MapPinned,
  Users,
  FileText,
  Brain
};

export default function Dashboard() {
  const [stats, setStats] = useState([]);
  const [crimeTrend, setCrimeTrend] = useState([]);
  const [crimeCategory, setCrimeCategory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // Note: api baseURL is http://127.0.0.1:8000/api but our endpoints are at /dashboard
        // Since we didn't add /api prefix in backend, we should use full URL or adjust path
        // We will just use the axios instance and override the URL temporarily or just use fetch
        // Alternatively, since axios baseURL is /api, we can fetch from `http://127.0.0.1:8000/dashboard/...`
        
        const [statsRes, trendRes, categoryRes] = await Promise.all([
          api.get("http://127.0.0.1:8000/dashboard/stats"),
          api.get("http://127.0.0.1:8000/dashboard/crime-trend"),
          api.get("http://127.0.0.1:8000/dashboard/crime-category")
        ]);

        const formattedStats = statsRes.data.stats.map(st => ({
          ...st,
          icon: iconMap[st.icon] || ShieldAlert
        }));

        setStats(formattedStats);
        setCrimeTrend(trendRes.data.crimeTrend);
        setCrimeCategory(categoryRes.data.crimeCategory);
      } catch (err) {
        console.error("Failed to fetch dashboard data", err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <p className="text-red-400">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* HERO */}
      <HeroBanner />

      {/* STATS */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        {stats.map((item) => (
          <StatsCard key={item.title} {...item} />
        ))}
      </div>

      {/* CHARTS */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <ChartCard title="Crime Trend Analysis">
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={crimeTrend}>
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="crimes" stroke="#22d3ee" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard title="Crime Categories">
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={crimeCategory}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="cases" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* AI INSIGHTS */}
      <ChartCard title="AI Intelligence Insights">
        <div className="space-y-4">
          <div className="rounded-xl border border-red-500/20 bg-red-500/10 p-4">
            <div className="flex gap-3 items-center">
              <ShieldAlert className="text-red-400" />
              <h3 className="text-white font-bold">Risk Alert</h3>
            </div>
            <p className="text-slate-300 mt-2">Robbery cases increased in Bengaluru zones.</p>
          </div>

          <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/10 p-4">
            <div className="flex gap-3 items-center">
              <Brain className="text-cyan-400" />
              <h3 className="text-white font-bold">AI Prediction</h3>
            </div>
            <p className="text-slate-300 mt-2">AI model detected possible crime hotspots.</p>
          </div>
        </div>
      </ChartCard>

      {/* ALERTS */}
      <ChartCard title="Live Crime Alerts">
        <AlertCard title="Armed Robbery" location="Electronic City" time="2 mins ago" color="text-red-400" />
        <AlertCard title="Cyber Fraud" location="Whitefield" time="15 mins ago" color="text-yellow-400" />
        <AlertCard title="Vehicle Theft" location="Koramangala" time="30 mins ago" color="text-blue-400" />
      </ChartCard>
    </div>
  );
}