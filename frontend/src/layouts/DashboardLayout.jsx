import { Outlet } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";

import PageTransition from "../components/common/PageTransition";
import AnimatedBackground from "../components/common/AnimatedBackground";
import AnimatedGrid from "../components/common/AnimatedGrid";

export default function DashboardLayout() {
  return (
    <div className="relative flex h-screen overflow-hidden bg-[#070B17] text-white">

      {/* Animated Background */}
      <AnimatedBackground />

      {/* Animated Grid */}
      <AnimatedGrid />

      {/* Sidebar */}
      <div className="relative z-10">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex flex-1 flex-col overflow-hidden">

        {/* Navbar */}
        <Navbar />

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-8">
          <PageTransition>
            <Outlet />
          </PageTransition>
        </main>

      </div>

    </div>
  );
}