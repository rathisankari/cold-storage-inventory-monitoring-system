import { useEffect, useState } from "react";
import api from "../services/api";
import "../App.css";

function AuditLogs() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/audit-logs/")
      .then((response) => {
        setLogs(response.data);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to load audit logs");
      });
  }, []);

  if (error) {
    return <div className="page-message">{error}</div>;
  }

  return (
    <div className="inventory-page">
      <main className="inventory-content">

        <section className="inventory-header">
          <div>
            <span className="section-label">System History</span>
            <h1>Audit Logs</h1>
            <p>
              Track important actions performed in ColdGuard.
            </p>
          </div>
        </section>

        <section className="inventory-records-section">

          <div className="section-header">
            <div>
              <span className="section-label">Records</span>
              <h2>Audit History</h2>
            </div>

            <span className="record-count">
              {logs.length}
            </span>
          </div>

          <div className="inventory-grid">

            {logs.map((log) => (

              <div
                className="inventory-card"
                key={log.id}
              >

                <div className="inventory-card-header">

                  <div>
                    <h3>{log.action}</h3>

                    <span>
                      Audit ID: {log.id}
                    </span>
                  </div>

                  <span className="inventory-status good">
                    {log.resource_type}
                  </span>

                </div>

                <div className="inventory-details">

                  <div>
                    <span>User ID</span>
                    <strong>{log.user_id}</strong>
                  </div>

                  <div>
                    <span>Resource ID</span>
                    <strong>{log.resource_id}</strong>
                  </div>

                  <div>
                    <span>Action</span>
                    <strong>{log.action}</strong>
                  </div>

                  <div>
                    <span>Time</span>
                    <strong>
                      {new Date(log.created_at).toLocaleString()}
                    </strong>
                  </div>

                </div>

              </div>

            ))}

          </div>

        </section>

      </main>
    </div>
  );
}

export default AuditLogs;