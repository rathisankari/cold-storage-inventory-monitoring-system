
import { useEffect, useState } from "react";
import api from "../services/api";
import "../App.css";

function AIAnomalies() {
  const [storageUnitId, setStorageUnitId] = useState("3");
  const [limit, setLimit] = useState("100");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const loadAnomalies = async () => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await api.get(
        `/ai/anomalies/${storageUnitId}`,
        { params: { limit: Number(limit) } }
      );
      setData(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to load AI analysis. Check your login and permissions."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnomalies();
  }, []);

  return (
    <div className="inventory-page">
      <main className="inventory-content">
        <section className="inventory-header">
          <div>
            <span className="section-label">Experimental AI</span>
            <h1>Temperature Anomaly Detection</h1>
            <p>
              Analyze historical readings using Isolation Forest.
              Existing temperature safety limits remain authoritative.
            </p>
          </div>
        </section>

        <section className="inventory-records-section">
          <div className="section-header">
            <div>
              <span className="section-label">Analysis settings</span>
              <h2>Historical Readings</h2>
            </div>
          </div>

          <div className="inventory-card">
            <div className="inventory-details">
              <label>
                Storage Unit ID
                <input
                  type="number"
                  min="1"
                  value={storageUnitId}
                  onChange={(event) =>
                    setStorageUnitId(event.target.value)
                  }
                />
              </label>

              <label>
                Readings to analyze
                <select
                  value={limit}
                  onChange={(event) => setLimit(event.target.value)}
                >
                  <option value="10">10</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                  <option value="200">200</option>
                  <option value="500">500</option>
                </select>
              </label>
            </div>

            <div className="inventory-card-actions">
              <button
                onClick={loadAnomalies}
                disabled={loading || !storageUnitId}
              >
                {loading ? "Analyzing..." : "Run AI Analysis"}
              </button>
            </div>
          </div>

          {error && (
            <div className="page-message" role="alert">
              {error}
            </div>
          )}

          {data && (
            <>
              <div className="inventory-grid">
                <div className="inventory-card">
                  <span>Readings analyzed</span>
                  <h2>{data.readings_analyzed}</h2>
                </div>

                <div className="inventory-card">
                  <span>AI anomalies</span>
                  <h2>{data.anomaly_count}</h2>
                </div>

                <div className="inventory-card">
                  <span>Safety-threshold breaches</span>
                  <h2>{data.threshold_breach_count}</h2>
                </div>

                <div className="inventory-card">
                  <span>Configured safe range</span>
                  <h2>
                    {data.configured_min_temp}–{data.configured_max_temp}°C
                  </h2>
                </div>
              </div>

              <p>
                Method: {data.method}. AI predictions are experimental
                and do not replace configured temperature safety limits.
              </p>

              <div className="inventory-records-section">
                <div className="section-header">
                  <div>
                    <span className="section-label">Reading history</span>
                    <h2>Analysis Results</h2>
                  </div>
                </div>

                <div className="inventory-grid">
                  {data.results.map((result) => (
                    <div
                      className="inventory-card"
                      key={result.reading_id}
                    >
                      <div className="inventory-card-header">
                        <div>
                          <h3>Reading #{result.reading_id}</h3>
                          <span>
                            {new Date(result.recorded_at).toLocaleString()}
                          </span>
                        </div>

                        <span
                          className={`inventory-status ${
                            result.threshold_breach ? "bad" : "good"
                          }`}
                        >
                          {result.threshold_breach
                            ? "Outside safe range"
                            : "Within safe range"}
                        </span>
                      </div>

                      <div className="inventory-details">
                        <div>
                          <span>Temperature</span>
                          <strong>{result.temperature}°C</strong>
                        </div>

                        <div>
                          <span>AI prediction</span>
                          <strong>{result.ai_prediction}</strong>
                        </div>

                        <div>
                          <span>Anomaly score</span>
                          <strong>{result.anomaly_score}</strong>
                        </div>

                        <div>
                          <span>Source</span>
                          <strong>{result.source}</strong>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default AIAnomalies;
