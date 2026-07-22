import {
  LayoutDashboard,
  MessageSquare,
  Map,
  Network,
  FileText,
  Shield,
  BarChart3,
  Settings,
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
    name: "Criminal Network",
    icon: Network,
    path: "/network",
  },
  {
    name: "Reports",
    icon: FileText,
    path: "/reports",
  },
  {
    name: "Analytics",
    icon: BarChart3,
    path: "/analytics",
  },
  {
    name: "Settings",
    icon: Settings,
    path: "/settings",
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
        border-cyan-500/20
        bg-white/5
        backdrop-blur-2xl
      "
    >
      {/* Background Glow */}
      <div className="absolute inset-0">

        <div className="absolute -top-20 -left-20 h-60 w-60 rounded-full bg-cyan-500/20 blur-[120px]" />

        <div className="absolute bottom-0 right-0 h-60 w-60 rounded-full bg-blue-600/20 blur-[120px]" />

      </div>

      {/* Logo */}
      <div className="relative z-10 flex items-center gap-4 border-b border-white/10 p-6">

        <motion.div
          whileHover={{
            rotate: 10,
            scale: 1.1,
          }}
          className="
            rounded-2xl
            bg-linear-to-br
            from-cyan-500
            to-blue-600
            p-3
            shadow-[0_0_25px_rgba(34,211,238,0.5)]
          "
        >
          <Shield className="text-white" size={26} />
        </motion.div>

        <div>
          <h1 className="text-xl font-bold tracking-wide text-white">
            CrimeVision AI
          </h1>

          <p className="text-xs text-slate-400">
            Karnataka Police
          </p>
        </div>

      </div>

      {/* Menu */}
      <nav className="relative z-10 flex-1 p-4">

        {menuItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink key={item.name} to={item.path}>
              {({ isActive }) => (
                <motion.div
                  whileHover={{
                    x: 8,
                    scale: 1.02,
                  }}
                  whileTap={{
                    scale: 0.98,
                  }}
                  className={`
                    mb-3
                    flex
                    items-center
                    gap-4
                    rounded-2xl
                    px-4
                    py-3
                    transition-all
                    duration-300

                    ${
                      isActive
                        ? "border border-cyan-500/30 bg-cyan-500/15 text-cyan-300 shadow-[0_0_25px_rgba(34,211,238,0.25)]"
                        : "text-slate-300 hover:bg-white/10 hover:text-white"
                    }
                  `}
                >
                  <Icon size={20} />

                  <span className="font-medium">
                    {item.name}
                  </span>

                  {isActive && (
                    <motion.div
                      layoutId="activeIndicator"
                      className="ml-auto h-2 w-2 rounded-full bg-cyan-400"
                    />
                  )}
                </motion.div>
              )}
            </NavLink>
          );
        })}

      </nav>

      {/* Footer */}
      <div className="relative z-10 border-t border-white/10 p-5">

        <div className="flex items-center gap-3">

          <div className="h-3 w-3 rounded-full bg-green-400 animate-pulse" />

          <span className="text-sm text-slate-300">
            AI System Online
          </span>

        </div>

      </div>
    </motion.aside>
  );
}