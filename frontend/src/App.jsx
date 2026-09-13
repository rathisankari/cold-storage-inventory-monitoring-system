import { BrowserRouter, Routes, Route, NavLink, useLocation, useNavigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Inventory from "./pages/Inventory";
import Login from "./pages/Login";

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
      {location.pathname !== "/" && (
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

            <button onClick={handleLogout}>
              Logout
            </button>
          </div>
        </nav>
      )}

      <Routes>
        <Route path="/" element={<Login />} />

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