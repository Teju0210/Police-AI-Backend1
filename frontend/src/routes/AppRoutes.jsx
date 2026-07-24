import { HashRouter, Routes, Route } from "react-router-dom";

// Pages
import Login from "../pages/Login/Login";
import Dashboard from "../pages/Dashboard/Dashboard";
import Chat from "../pages/Chat/Chat";
import Heatmap from "../pages/Heatmap/Heatmap";
import Network from "../pages/Network/Network";
import Reports from "../pages/Reports/Reports";
import Analytics from "../pages/Analytics/Analytics";

// Layout
import DashboardLayout from "../layouts/DashboardLayout";

// Protection
import ProtectedRoute from "./ProtectedRoute";


export default function AppRoutes() {

  return (

    <HashRouter>

      <Routes>


        {/* Public Route */}

        <Route
          path="/"
          element={<Login />}
        />



        {/* Protected Routes */}

        <Route

          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }

        >


          <Route
            path="/dashboard"
            element={<Dashboard />}
          />


          <Route
            path="/chat"
            element={<Chat />}
          />


          <Route
            path="/heatmap"
            element={<Heatmap />}
          />


          <Route
            path="/network"
            element={<Network />}
          />


          <Route
            path="/reports"
            element={<Reports />}
          />


          <Route
            path="/analytics"
            element={<Analytics />}
          />


        </Route>


      </Routes>


    </HashRouter>

  );
}