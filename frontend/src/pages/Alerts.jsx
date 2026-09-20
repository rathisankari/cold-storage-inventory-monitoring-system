import { useEffect, useState } from "react";
import api from "../services/api";
import "../App.css";

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState("");

  const loadAlerts = async () => {
    try {
      const response = await api.get("/alerts/");
      setAlerts(response.data);
    } catch (error) {
      console.error(error);
      setError("Failed to load alerts");
    }
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  const acknowledgeAlert = async (alertId) => {
    try {
      await api.put(`/alerts/${alertId}/acknowledge`);
      loadAlerts();
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Failed to acknowledge alert");
    }
  };

  const getStatusClass = (status) => {
    if (status === "Active") return "bad";
    if (status === "Acknowledged") return "warning";
    return "good";
  };

  if (error) {
    return <div className="page-message">{error}</div>;
  }

  return (
    <div className="inventory-page">
      <main className="inventory-content">
        <section className="inventory-header">
          <div>
            <span className="section-label">Temperature Monitoring</span>
            <h1>Alerts</h1>
            <p>View and manage temperature breach alerts.</p>
          </div>
        </section>

        <section className="inventory-records-section">
          <div className="section-header">
            <div>
              <span className="section-label">Records</span>
              <h2>Alert History</h2>
            </div>

            <span className="record-count">{alerts.length}</span>
          </div>

          <div className="inventory-grid">
            {alerts.map((alert) => (
              <div className="inventory-card" key={alert.id}>
                <div className="inventory-card-header">
                  <div>
                    <h3>{alert.alert_type}</h3>
                    <span>Alert ID: {alert.id}</span>
                  </div>

                  <span
                    className={`inventory-status ${getStatusClass(
                      alert.status
                    )}`}
                  >
                    {alert.status}
                  </span>
                </div>

                <div className="inventory-details">
                  <div>
                    <span>Storage Unit</span>
                    <strong>{alert.storage_unit_id}</strong>
                  </div>

                  <div>
                    <span>Severity</span>
                    <strong>{alert.severity}</strong>
                  </div>

                  <div>
                    <span>Message</span>
                    <strong>{alert.message}</strong>
                  </div>

                  <div>
                    <span>Created</span>
                    <strong>
                      {new Date(alert.created_at).toLocaleString()}
                    </strong>
                  </div>
                </div>

                {alert.status === "Active" && (
                  <div className="inventory-card-actions">
                    <button onClick={() => acknowledgeAlert(alert.id)}>
                      Acknowledge
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default Alerts;