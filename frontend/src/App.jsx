import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
  useLocation,
  useNavigate,
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Alerts from "./pages/Alerts";
import AuditLogs from "./pages/AuditLogs";
import ComplianceReport from "./pages/ComplianceReport";

import "./App.css";

function ProtectedRoute({ children }) {
  const token = localStorage.getItem("access_token");

  if (!token) {
    window.location.href = "/";
    return null;
  }

  return children;
}

function AppContent() {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_role");

    navigate("/");
  };

  return (
    <>
      {location.pathname !== "/" && location.pathname !== "/register" && (
        <nav className="navbar">
          <div className="navbar-brand">
            <h2>ColdGuard</h2>
            <span>Cold Storage Monitoring</span>
          </div>

          <div className="navbar-links">
            <NavLink
              to="/dashboard"
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              Dashboard
            </NavLink>

            <NavLink
              to="/inventory"
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              Inventory
            </NavLink>

            <NavLink
              to="/alerts"
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              Alerts
            </NavLink>

            <NavLink
              to="/audit-logs"
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              Audit Logs
            </NavLink>

            <NavLink
              to="/compliance-report"
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              Compliance Report
            </NavLink>

            <button onClick={handleLogout}>Logout</button>
          </div>
        </nav>
      )}

      <Routes>
        <Route path="/" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/inventory"
          element={
            <ProtectedRoute>
              <Inventory />
            </ProtectedRoute>
          }
        />

        <Route
          path="/alerts"
          element={
            <ProtectedRoute>
              <Alerts />
            </ProtectedRoute>
          }
        />

        <Route
          path="/audit-logs"
          element={
            <ProtectedRoute>
              <AuditLogs />
            </ProtectedRoute>
          }
        />

        <Route
          path="/compliance-report"
          element={
            <ProtectedRoute>
              <ComplianceReport />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;