import { useEffect, useState } from "react";
import api from "../services/api";
import "../App.css";

function ComplianceReport() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/compliance-report/")
      .then((response) => {
        setReport(response.data);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to load compliance report");
      });
  }, []);

  if (error) {
    return <div className="page-message">{error}</div>;
  }

  if (!report) {
    return <div className="page-message">Loading compliance report...</div>;
  }

  return (
    <div className="inventory-page">
      <main className="inventory-content">

        <section className="inventory-header">
          <div>
            <span className="section-label">Compliance</span>
            <h1>Compliance Report</h1>
            <p>
              Summary of temperature monitoring, alerts, and inventory status.
            </p>
          </div>
        </section>

        <section className="inventory-form-section">
          <div className="section-header">
            <div>
              <span className="section-label">Report</span>
              <h2>Temperature Summary</h2>
            </div>
          </div>

          <div className="inventory-details">
            <div>
              <span>Total Readings</span>
              <strong>
                {report.temperature_summary.total_readings}
              </strong>
            </div>

            <div>
              <span>Average Temperature</span>
              <strong>
                {report.temperature_summary.average_temperature}°C
              </strong>
            </div>

            <div>
              <span>Minimum Temperature</span>
              <strong>
                {report.temperature_summary.minimum_temperature}°C
              </strong>
            </div>

            <div>
              <span>Maximum Temperature</span>
              <strong>
                {report.temperature_summary.maximum_temperature}°C
              </strong>
            </div>
          </div>
        </section>

        <section className="inventory-form-section">
          <div className="section-header">
            <div>
              <span className="section-label">Monitoring</span>
              <h2>Alert Summary</h2>
            </div>
          </div>

          <div className="inventory-details">
            <div>
              <span>Total Alerts</span>
              <strong>
                {report.alert_summary.total_alerts}
              </strong>
            </div>

            <div>
              <span>Active Alerts</span>
              <strong>
                {report.alert_summary.active_alerts}
              </strong>
            </div>

            <div>
              <span>Acknowledged Alerts</span>
              <strong>
                {report.alert_summary.acknowledged_alerts}
              </strong>
            </div>

            <div>
              <span>Resolved Alerts</span>
              <strong>
                {report.alert_summary.resolved_alerts}
              </strong>
            </div>
          </div>
        </section>

        <section className="inventory-form-section">
          <div className="section-header">
            <div>
              <span className="section-label">Inventory</span>
              <h2>Inventory Summary</h2>
            </div>
          </div>

          <div className="inventory-details">
            <div>
              <span>Total Items</span>
              <strong>
                {report.inventory_summary.total_items}
              </strong>
            </div>

            <div>
              <span>Total Quantity</span>
              <strong>
                {report.inventory_summary.total_quantity}
              </strong>
            </div>

            <div>
              <span>Good</span>
              <strong>
                {report.inventory_summary.good}
              </strong>
            </div>

            <div>
              <span>Compromised</span>
              <strong>
                {report.inventory_summary.compromised}
              </strong>
            </div>

            <div>
              <span>Expired</span>
              <strong>
                {report.inventory_summary.expired}
              </strong>
            </div>

            <div>
              <span>Depleted</span>
              <strong>
                {report.inventory_summary.depleted}
              </strong>
            </div>

            <div>
              <span>Used</span>
              <strong>
                {report.inventory_summary.used}
              </strong>
            </div>
          </div>
        </section>

        <section className="inventory-form-section">
          <div className="section-header">
            <div>
              <span className="section-label">Report Information</span>
              <h2>Report Date</h2>
            </div>
          </div>

          <div className="inventory-details">
            <div>
              <span>Generated On</span>
              <strong>{report.report_date}</strong>
            </div>
          </div>
        </section>

      </main>
    </div>
  );
}

export default ComplianceReport;