import {
  LayoutDashboard,
  MessageSquare,
  Map,
  Network,
  FileText,
  Shield,
  BarChart3,
  Settings,
  Cpu,
  Activity
} from "lucide-react";

import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";

const menuItems = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    name: "AI Assistant",
    icon: MessageSquare,
    path: "/chat",
  },
  {
    name: "Crime Heatmap",
    icon: Map,
    path: "/heatmap",
  },
  {
    name: "Repeated Offenders",
    icon: Network,
    path: "/network",
  },
  {
    name: "Reports",
    icon: FileText,
    path: "/reports",
  },
  {
    name: "AI Risk Predictor",
    icon: BarChart3,
    path: "/analytics",
  },
];

export default function Sidebar() {
  return (
    <motion.aside
      initial={{ x: -80, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.8 }}
      className="
        relative
        w-72
        h-screen
        overflow-hidden
        border-r
        border-white/10
        bg-[#111827]/70
        backdrop-blur-xl
        flex
        flex-col
      "
    >
      {/* Background Glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute -top-32 -left-32 h-72 w-72 rounded-full bg-cyan-600/10 blur-[120px]" />
        <div className="absolute bottom-0 right-0 h-64 w-64 rounded-full bg-blue-700/10 blur-[120px]" />
      </div>

      {/* Logo Area */}
      <div className="relative z-10 flex h-20 items-center gap-4 border-b border-white/10 px-6">
        <div className="relative flex items-center justify-center h-12 w-12">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
            className="absolute inset-0 rounded-full border border-dashed border-cyan-500/40"
          />
          <motion.div
            whileHover={{ scale: 1.1, rotate: 5 }}
            className="
              relative
              z-10
              rounded-xl
              bg-gradient-to-br
              from-cyan-500
              to-blue-700
              p-2
              shadow-[0_0_20px_rgba(34,211,238,0.4)]
            "
          >
            <Shield className="text-white" size={20} />
          </motion.div>
        </div>

        <div>
          <h1 className="text-lg font-bold tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-300">
            CrimeVision AI
          </h1>
          <p className="text-[10px] uppercase tracking-widest text-cyan-500 font-semibold mt-0.5">
            Intelligence Platform
          </p>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="relative z-10 flex-1 overflow-y-auto px-4 py-6 scrollbar-hide">
        <div className="space-y-1.5">
          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink key={item.name} to={item.path}>
                {({ isActive }) => (
                  <motion.div
                    whileHover={{ x: 6 }}
                    whileTap={{ scale: 0.97 }}
                    className={`
                      relative
                      flex
                      items-center
                      gap-4
                      rounded-xl
                      px-4
                      py-3.5
                      transition-all
                      duration-300
                      group
                      overflow-hidden
                      ${
                        isActive
                          ? "bg-gradient-to-r from-cyan-500/10 to-transparent text-white"
                          : "text-slate-400 hover:bg-white/5 hover:text-slate-200"
                      }
                    `}
                  >
                    {isActive && (
                      <motion.div
                        layoutId="activeBar"
                        className="absolute left-0 top-0 bottom-0 w-1 bg-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.8)]"
                      />
                    )}

                    <Icon 
                      size={20} 
                      className={`transition-colors duration-300 ${isActive ? "text-cyan-400" : "group-hover:text-cyan-400/70"}`} 
                    />

                    <span className={`font-medium text-sm tracking-wide ${isActive ? "font-semibold" : ""}`}>
                      {item.name}
                    </span>
                  </motion.div>
                )}
              </NavLink>
            );
          })}
        </div>
      </nav>

      {/* System Status Footer */}
      <div className="relative z-10 border-t border-white/10 bg-slate-900/30 p-5 mt-auto">
        <div className="flex items-center gap-2 mb-4">
          <div className="h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px_rgba(52,211,153,0.8)] animate-pulse" />
          <span className="text-xs uppercase tracking-wider font-semibold text-slate-300">
            System Online
          </span>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-slate-400">
              <Cpu size={14} />
              <span className="text-xs">AI Core</span>
            </div>
            <span className="text-xs font-mono text-cyan-400">34%</span>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-slate-400">
              <Activity size={14} />
              <span className="text-xs">Database</span>
            </div>
            <span className="text-xs font-mono text-cyan-400">Stable</span>
          </div>
        </div>
      </div>
    </motion.aside>
  );
}