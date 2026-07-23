import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, MapPin, Calendar, User, FileText, Loader2, AlertTriangle, ShieldCheck } from "lucide-react";
import api from "../../services/api";

export default function Analytics() {
  const [formData, setFormData] = useState({
    Latitude: "",
    Longitude: "",
    Year: new Date().getFullYear(),
    Month: new Date().getMonth() + 1,
    AgeYear: "",
    GenderID: "M", 
    CrimeHead: "Crimes Against Property", 
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: Number(value) || value,
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const payload = {
        latitude: Number(formData.Latitude),
        longitude: Number(formData.Longitude),
        Year: Number(formData.Year),
        Month: Number(formData.Month),
        AgeYear: Number(formData.AgeYear),
        GenderID: String(formData.GenderID),
        CrimeHead: String(formData.CrimeHead)
      };
      
      const res = await api.post("/ai/predict_risk", payload);
      setResult(res.data);
    } catch (error) {
      console.error("Prediction Error:", error);
      setResult({ error: "Failed to connect to ML Backend." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* HEADER */}
      <div>
        <h1 className="flex items-center gap-3 text-4xl font-bold text-white">
          <Brain className="text-cyan-500" size={36} />
          AI Risk Predictor
        </h1>
        <p className="mt-2 text-slate-400">
          Advanced Machine Learning model for forecasting crime hotspots.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* FORM */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="rounded-3xl border border-cyan-500/20 bg-slate-900/50 p-8 shadow-2xl backdrop-blur-xl"
        >
          <h2 className="mb-6 text-2xl font-semibold text-white">Enter Parameters</h2>
          
          <form onSubmit={handlePredict} className="space-y-5">
            {/* Location */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-400 flex items-center gap-2">
                  <MapPin size={16} /> Latitude
                </label>
                <input
                  type="number"
                  step="any"
                  name="Latitude"
                  value={formData.Latitude}
                  onChange={handleChange}
                  placeholder="e.g. 12.9716"
                  required
                  className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-cyan-500"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-400 flex items-center gap-2">
                  <MapPin size={16} /> Longitude
                </label>
                <input
                  type="number"
                  step="any"
                  name="Longitude"
                  value={formData.Longitude}
                  onChange={handleChange}
                  placeholder="e.g. 77.5946"
                  required
                  className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-cyan-500"
                />
              </div>
            </div>

            {/* Time */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-400 flex items-center gap-2">
                  <Calendar size={16} /> Year
                </label>
                <input
                  type="number"
                  name="Year"
                  value={formData.Year}
                  onChange={handleChange}
                  required
                  className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-cyan-500"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-400 flex items-center gap-2">
                  <Calendar size={16} /> Month
                </label>
                <input
                  type="number"
                  name="Month"
                  min="1"
                  max="12"
                  value={formData.Month}
                  onChange={handleChange}
                  required
                  className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-cyan-500"
                />
              </div>
            </div>

            {/* Demographics */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-400 flex items-center gap-2">
                  <User size={16} /> Suspect Age
                </label>
                <input
                  type="number"
                  name="AgeYear"
                  value={formData.AgeYear}
                  onChange={handleChange}
                  placeholder="Age"
                  required
                  className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-cyan-500"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-400 flex items-center gap-2">
                  <User size={16} /> Gender
                </label>
                <select
                  name="GenderID"
                  value={formData.GenderID}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-cyan-500"
                >
                  <option value="M">Male</option>
                  <option value="F">Female</option>
                </select>
              </div>
            </div>

            {/* Crime Category */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-400 flex items-center gap-2">
                <FileText size={16} /> Crime Category
              </label>
              <select
                name="CrimeHead"
                value={formData.CrimeHead}
                onChange={handleChange}
                className="w-full rounded-xl border border-slate-700 bg-slate-800 p-3 text-white outline-none focus:border-cyan-500"
              >
                <option value="Crimes Against Property">Robbery / Property</option>
                <option value="Cyber Crime">Cyber Crime</option>
                <option value="Crimes Against Body">Assault / Body</option>
                <option value="Economic Offences">Economic Offences</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-6 flex w-full items-center justify-center gap-3 rounded-xl bg-cyan-600 p-4 font-bold text-white transition hover:bg-cyan-500 disabled:opacity-50"
            >
              {loading ? <Loader2 className="animate-spin" /> : <Brain />}
              {loading ? "Analyzing Models..." : "Predict Risk"}
            </button>
          </form>
        </motion.div>

        {/* RESULTS */}
        <div className="flex flex-col justify-center">
          <AnimatePresence>
            {!result && !loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center justify-center text-center p-12 opacity-50"
              >
                <Brain size={80} className="text-slate-600 mb-6" />
                <h3 className="text-xl text-slate-400 font-medium">Awaiting Data...</h3>
                <p className="text-sm text-slate-500 mt-2 max-w-sm">
                  Input parameters into the ML engine to generate a predictive heatmap score.
                </p>
              </motion.div>
            )}

            {result && !result.error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.9, x: 30 }}
                animate={{ opacity: 1, scale: 1, x: 0 }}
                className="relative overflow-hidden rounded-3xl border border-white/10 bg-slate-900/80 p-8 backdrop-blur-2xl"
              >
                {/* Glow effect based on hotspot */}
                <div 
                  className={`absolute -right-20 -top-20 h-64 w-64 rounded-full blur-[100px] ${
                    result.is_hotspot ? "bg-red-600/40" : "bg-green-500/30"
                  }`} 
                />

                <h3 className="text-2xl font-bold text-white mb-8">AI Analysis Complete</h3>

                <div className="space-y-8">
                  {/* Status Indicator */}
                  <div className="flex items-center gap-6">
                    <div className={`p-5 rounded-full ${result.is_hotspot ? "bg-red-500/20 text-red-500" : "bg-green-500/20 text-green-500"}`}>
                      {result.is_hotspot ? <AlertTriangle size={40} /> : <ShieldCheck size={40} />}
                    </div>
                    <div>
                      <p className="text-sm text-slate-400 font-medium uppercase tracking-wider">Classification</p>
                      <p className={`text-3xl font-extrabold mt-1 ${result.is_hotspot ? "text-red-400" : "text-green-400"}`}>
                        {result.is_hotspot ? "HIGH RISK HOTSPOT" : "SAFE ZONE"}
                      </p>
                    </div>
                  </div>

                  {/* Score Meter */}
                  <div className="bg-black/30 p-6 rounded-2xl border border-white/5">
                    <p className="text-sm text-slate-400 font-medium mb-3">Probability Score</p>
                    <div className="flex items-end gap-3">
                      <span className="text-5xl font-black text-white">
                        {(result.risk_score * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="w-full h-3 bg-slate-800 rounded-full mt-5 overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${result.risk_score * 100}%` }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        className={`h-full rounded-full ${result.is_hotspot ? "bg-red-500" : "bg-green-500"}`}
                      />
                    </div>
                  </div>
                </div>

              </motion.div>
            )}

            {result && result.error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="rounded-3xl border border-red-500/30 bg-red-500/10 p-8 backdrop-blur-xl text-center"
              >
                <AlertTriangle size={60} className="mx-auto text-red-500 mb-4" />
                <h3 className="text-xl font-bold text-white">{result.error}</h3>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}