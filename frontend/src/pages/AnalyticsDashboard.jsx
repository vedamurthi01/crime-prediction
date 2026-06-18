import React, { useState, useEffect } from "react";
import { getAllVisualizations } from "../services/api";

function AnalyticsDashboard() {
  const [loading, setLoading] = useState(true);
  const [visualizations, setVisualizations] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadVisualizations();
  }, []);

  const loadVisualizations = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await getAllVisualizations();
      if (data.success) {
        setVisualizations(data.visualizations);
      } else {
        setError("Failed to load visualizations");
      }
    } catch (err) {
      setError("Error loading visualizations: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const stats = visualizations?.statistics || {};

  return (
    <div className="container">
      <div className="card">
        <h1 className="card-title" style={{ color: "white" }}>
          Crime Analytics Dashboard
        </h1>
        <p className="card-subtitle">
          Comprehensive crime data analysis and visualizations
        </p>

        {error && <div className="error">{error}</div>}

        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading analytics...</p>
          </div>
        ) : (
          <>
            {/* Statistics Cards */}
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">
                  {stats.total_crimes?.toLocaleString() || 0}
                </div>
                <div className="stat-label">Total Crimes</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">
                  {Object.keys(stats.top_crime_types || {}).length}
                </div>
                <div className="stat-label">Crime Types</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">
                  {Object.keys(stats.top_locations || {}).length}
                </div>
                <div className="stat-label">Locations</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">
                  {stats.avg_victim_age?.toFixed(0) || "N/A"}
                </div>
                <div className="stat-label">Avg Victim Age</div>
              </div>
            </div>

            {/* Crime Heatmap */}
            {visualizations?.heatmap && (
              <div className="card">
                <h3 style={{ color: "white" }}>
                  Crime Heatmap: Location vs Hour
                </h3>
                <img
                  src={`data:image/png;base64,${visualizations.heatmap}`}
                  alt="Crime Heatmap"
                  className="viz-image"
                />
              </div>
            )}

            {/* Charts Grid */}
            <div className="grid grid-2">
              {visualizations?.hour_chart && (
                <div className="card">
                  <h3 style={{ color: "white" }}>Crimes by Hour</h3>
                  <img
                    src={`data:image/png;base64,${visualizations.hour_chart}`}
                    alt="Crimes by Hour"
                    className="viz-image"
                  />
                </div>
              )}

              {visualizations?.type_chart && (
                <div className="card">
                  <h3 style={{ color: "white" }}>Crimes by Type</h3>
                  <img
                    src={`data:image/png;base64,${visualizations.type_chart}`}
                    alt="Crimes by Type"
                    className="viz-image"
                  />
                </div>
              )}
            </div>

            {/* Monthly Trend */}
            {visualizations?.monthly_trend && (
              <div className="card">
                <h3 style={{ color: "white" }}>Monthly Crime Trend</h3>
                <img
                  src={`data:image/png;base64,${visualizations.monthly_trend}`}
                  alt="Monthly Trend"
                  className="viz-image"
                />
              </div>
            )}

            {/* Top Crime Types */}
            {stats.top_crime_types && (
              <div className="card">
                <h3 style={{ color: "white" }}>Top Crime Types</h3>
                <div style={{ overflowX: "auto" }}>
                  <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                      <tr style={{ borderBottom: "2px solid #505050" }}>
                        <th
                          style={{
                            padding: "1rem",
                            textAlign: "left",
                            color: "white",
                          }}
                        >
                          Crime Type
                        </th>
                        <th
                          style={{
                            padding: "1rem",
                            textAlign: "right",
                            color: "white",
                          }}
                        >
                          Count
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(stats.top_crime_types).map(
                        ([type, count], index) => (
                          <tr
                            key={type}
                            style={{ borderBottom: "1px solid #404040" }}
                          >
                            <td style={{ padding: "0.75rem", color: "white" }}>
                              {type}
                            </td>
                            <td
                              style={{
                                padding: "0.75rem",
                                textAlign: "right",
                                fontWeight: "bold",
                                color: "white",
                              }}
                            >
                              {count}
                            </td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Top Locations */}
            {stats.top_locations && (
              <div className="card">
                <h3 style={{ color: "white" }}>Top Crime Locations</h3>
                <div style={{ overflowX: "auto" }}>
                  <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                      <tr style={{ borderBottom: "2px solid #505050" }}>
                        <th
                          style={{
                            padding: "1rem",
                            textAlign: "left",
                            color: "white",
                          }}
                        >
                          Location
                        </th>
                        <th
                          style={{
                            padding: "1rem",
                            textAlign: "right",
                            color: "white",
                          }}
                        >
                          Count
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(stats.top_locations).map(
                        ([location, count]) => (
                          <tr
                            key={location}
                            style={{ borderBottom: "1px solid #404040" }}
                          >
                            <td style={{ padding: "0.75rem", color: "white" }}>
                              {location}
                            </td>
                            <td
                              style={{
                                padding: "0.75rem",
                                textAlign: "right",
                                fontWeight: "bold",
                                color: "white",
                              }}
                            >
                              {count}
                            </td>
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            <button onClick={loadVisualizations} className="btn btn-secondary">
              Refresh Analytics
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default AnalyticsDashboard;
