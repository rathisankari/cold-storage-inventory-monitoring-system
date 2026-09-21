import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import api from "../services/api";
import "../App.css";

function Dashboard() {
  const [monitoring, setMonitoring] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [temperatureHistory, setTemperatureHistory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/monitoring/3"),
      api.get("/alerts/"),
      api.get("/monitoring/3/temperature-history"),
    ])
      .then(
        ([monitoringResponse, alertsResponse, historyResponse]) => {
          setMonitoring(monitoringResponse.data);
          setAlerts(alertsResponse.data);
          setTemperatureHistory(historyResponse.data);
        }
      )
      .catch((error) => {
        console.error(error);
        setError("Failed to connect to backend");
      });
  }, []);

  if (error) {
    return <div className="page-message">{error}</div>;
  }

  if (!monitoring) {
    return <div className="page-message">Loading...</div>;
  }

  const temperature =
    monitoring.latest_temperature?.temperature ?? 0;

  const chartData = [...temperatureHistory]
    .reverse()
    .filter(
      (record) =>
        record.recorded_at !== null &&
        record.temperature !== null &&
        !isNaN(Number(record.temperature))
    )
    .map((record) => ({
      time: new Date(record.recorded_at).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
      temperature: Number(record.temperature),
    }));

  const activeAlerts = alerts.filter(
    (alert) => alert.status === "Active"
  );

  const activeAlert = activeAlerts[0];

  const handleAcknowledge = () => {
    if (!activeAlert) {
      return;
    }

    api
      .put(`/alerts/${activeAlert.id}/acknowledge`)
      .then((response) => {
        setAlerts((currentAlerts) =>
          currentAlerts.map((alert) =>
            alert.id === response.data.id
              ? response.data
              : alert
          )
        );
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const isNormal =
    temperature >= monitoring.min_temp &&
    temperature <= monitoring.max_temp;

  return (
    <div className="dashboard">
      <main className="dashboard-content">

        <section className="summary-grid">

          <div className="summary-card">
            <span className="card-label">
              Storage Unit
            </span>

            <h2>
              {monitoring.storage_unit_name}
            </h2>
          </div>

          <div className="summary-card">
            <span className="card-label">
              Temperature
            </span>

            <h2>
              {temperature}
              {"\u00B0"}C
            </h2>
          </div>

          <div className="summary-card">
            <span className="card-label">
              Humidity
            </span>

            <h2>
              {monitoring.latest_temperature?.humidity ?? 0}%
            </h2>
          </div>

          <div className="summary-card">
            <span className="card-label">
              Active Alerts
            </span>

            <h2>
              {activeAlerts.length}
            </h2>
          </div>

        </section>

        <section className="room-section">

          <div className="section-header">

            <div>
              <span className="section-label">
                Storage Monitoring
              </span>

              <h2>
                {monitoring.storage_unit_name}
              </h2>
            </div>

            <span
              className={`temperature-status ${
                isNormal ? "normal" : "warning"
              }`}
            >
              {isNormal
                ? "Normal"
                : monitoring.temperature_status}
            </span>

          </div>

          <div className="room-details">

            <div>
              <span>
                Current Temperature
              </span>

              <strong>
                {temperature}
                {"\u00B0"}C
              </strong>
            </div>

            <div>
              <span>
                Allowed Range
              </span>

              <strong>
                {monitoring.min_temp}
                {"\u00B0"}C - {monitoring.max_temp}
                {"\u00B0"}C
              </strong>
            </div>

            <div>
              <span>
                Humidity
              </span>

              <strong>
                {monitoring.latest_temperature?.humidity ?? 0}%
              </strong>
            </div>

          </div>

        </section>

        <section className="alerts-section">

          <div className="section-header">

            <div>
              <span className="section-label">
                Monitoring
              </span>

              <h2>
                Active Alerts
              </h2>
            </div>

            <span className="alert-count">
              {activeAlerts.length}
            </span>

          </div>

          {activeAlerts.length > 0 ? (

            <div className="alert-box">

              <div className="alert-icon">
                !
              </div>

              <div>

                <strong>
                  {activeAlert.alert_type}
                </strong>

                <p>
                  {activeAlert.message}
                </p>

                <button
                  onClick={handleAcknowledge}
                >
                  Acknowledge
                </button>

              </div>

            </div>

          ) : (

            <p className="no-alerts">
              No active alerts
            </p>

          )}

        </section>

        <section className="history-section">

          <div className="section-header">

            <div>
              <span className="section-label">
                Temperature History
              </span>

              <h2>
                Temperature Trend
              </h2>
            </div>

          </div>

          <div className="temperature-chart">

            <ResponsiveContainer
              width="100%"
              height={320}
            >

              <LineChart
                data={chartData}
                margin={{
                  top: 20,
                  right: 30,
                  left: 20,
                  bottom: 20,
                }}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="time"
                  tick={{
                    fontSize: 11,
                    fill: "#667085",
                  }}
                  tickLine={false}
                  axisLine={{
                    stroke: "#d0d5dd",
                  }}
                  interval="preserveStartEnd"
                />

                <YAxis
                  domain={[0, 10]}
                  tick={{
                    fontSize: 11,
                    fill: "#667085",
                  }}
                  tickLine={false}
                  axisLine={false}
                />

                <Tooltip
                  contentStyle={{
                    background: "#ffffff",
                    border: "1px solid #e5eaf1",
                    borderRadius: "8px",
                    boxShadow:
                      "0 4px 12px rgba(23, 32, 51, 0.08)",
                  }}
                  labelStyle={{
                    color: "#344054",
                    fontWeight: 600,
                  }}
                  formatter={(value) => [
                    `${value}°C`,
                    "Temperature",
                  ]}
                />

                <Line
                  type="monotone"
                  dataKey="temperature"
                  stroke="#2563eb"
                  strokeWidth={3}
                  dot={{
                    r: 4,
                    fill: "#2563eb",
                  }}
                  activeDot={{
                    r: 6,
                  }}
                  connectNulls={true}
                  isAnimationActive={false}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </section>

      </main>
    </div>
  );
}

export default Dashboard;