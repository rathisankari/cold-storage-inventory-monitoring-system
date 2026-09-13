import { useEffect, useState } from "react";
import api from "../services/api";

function MonitoringTest() {
  const [monitoring, setMonitoring] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/monitoring/3")
      .then((response) => {
        setMonitoring(response.data);
      })
      .catch((error) => {
        console.error(error);
        setError("Failed to connect to backend");
      });
  }, []);

  if (error) {
    return <p>{error}</p>;
  }

  if (!monitoring) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <h1>{monitoring.storage_unit_name}</h1>

      <p>Status: {monitoring.status}</p>

      <p>
        Temperature Range: {monitoring.min_temp}
        {"\u00B0"}C - {monitoring.max_temp}
        {"\u00B0"}C
      </p>

      <h2>Latest Temperature</h2>

      <p>
        Temperature: {monitoring.latest_temperature.temperature}
        {"\u00B0"}C
      </p>

      <p>
        Humidity: {monitoring.latest_temperature.humidity}%
      </p>

      <p>Temperature Status: {monitoring.temperature_status}</p>

      <p>Active Alerts: {monitoring.active_alerts}</p>
    </div>
  );
}

export default MonitoringTest;