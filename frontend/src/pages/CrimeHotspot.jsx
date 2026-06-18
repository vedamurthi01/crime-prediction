import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:5000/api";

function CrimeHotspot() {
  const [hotspots, setHotspots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    crime_type: "ALL",
    start_hour: 0,
    end_hour: 23,
  });
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [locationDetails, setLocationDetails] = useState(null);
  const [crimeTypes, setCrimeTypes] = useState([]);

  useEffect(() => {
    loadCrimeTypes();
    loadHotspots();
  }, []);

  const loadCrimeTypes = async () => {
    try {
      const response = await axios.get(`${API_URL}/visualization/statistics`);
      if (response.data.success && response.data.statistics.top_crime_types) {
        const types = Object.keys(response.data.statistics.top_crime_types);
        setCrimeTypes(["ALL", ...types]);
      }
    } catch (err) {
      console.error("Error loading crime types:", err);
    }
  };

  const loadHotspots = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      if (filters.crime_type !== "ALL") {
        params.append("crime_type", filters.crime_type);
      }
      params.append("start_hour", filters.start_hour);
      params.append("end_hour", filters.end_hour);

      const response = await axios.get(`${API_URL}/hotspot/data?${params}`);
      if (response.data.success) {
        setHotspots(response.data.hotspots);
      }
    } catch (err) {
      setError("Failed to load hotspot data");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadLocationDetails = async (location) => {
    try {
      const response = await axios.get(
        `${API_URL}/hotspot/location/${location}`
      );
      if (response.data.success) {
        setLocationDetails(response.data);
        setSelectedLocation(location);
      }
    } catch (err) {
      console.error("Error loading location details:", err);
    }
  };

  const getRiskColor = (riskLevel) => {
    if (riskLevel >= 75) return "#ef4444";
    if (riskLevel >= 50) return "#f59e0b";
    if (riskLevel >= 25) return "#eab308";
    return "#10b981";
  };

  const getRiskLabel = (riskLevel) => {
    if (riskLevel >= 75) return "High Risk";
    if (riskLevel >= 50) return "Medium Risk";
    if (riskLevel >= 25) return "Low-Medium";
    return "Low Risk";
  };

  const handleFilterChange = (field, value) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
  };

  const applyFilters = () => {
    loadHotspots();
  };

  const closeDetails = () => {
    setSelectedLocation(null);
    setLocationDetails(null);
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="card-title">Crime Hotspot Map</h1>
        <p className="card-subtitle">
          Interactive crime density visualization by location with filters
        </p>

        {/* Filters */}
        <div
          className="card"
          style={{ marginBottom: "2rem", background: "rgba(30,30,30,0.6)" }}
        >
          <h3 style={{ color: "white", marginBottom: "1rem" }}>Filters</h3>
          <div className="grid grid-3">
            <div className="form-group">
              <label>Crime Type</label>
              <select
                value={filters.crime_type}
                onChange={(e) =>
                  handleFilterChange("crime_type", e.target.value)
                }
              >
                {crimeTypes.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Start Hour</label>
              <select
                value={filters.start_hour}
                onChange={(e) =>
                  handleFilterChange("start_hour", parseInt(e.target.value))
                }
              >
                {[...Array(24)].map((_, i) => (
                  <option key={i} value={i}>
                    {i}:00
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>End Hour</label>
              <select
                value={filters.end_hour}
                onChange={(e) =>
                  handleFilterChange("end_hour", parseInt(e.target.value))
                }
              >
                {[...Array(24)].map((_, i) => (
                  <option key={i} value={i}>
                    {i}:00
                  </option>
                ))}
              </select>
            </div>
          </div>
          <button
            onClick={applyFilters}
            className="btn btn-primary"
            style={{ marginTop: "1rem" }}
          >
            Apply Filters
          </button>
        </div>

        {/* Hotspot Grid */}
        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading hotspot data...</p>
          </div>
        ) : error ? (
          <div className="error">{error}</div>
        ) : (
          <>
            <div className="grid grid-3" style={{ marginBottom: "2rem" }}>
              {hotspots.slice(0, 15).map((hotspot) => (
                <div
                  key={hotspot.location}
                  className="card"
                  style={{
                    cursor: "pointer",
                    background: "rgba(20,20,20,0.6)",
                    border: `2px solid ${getRiskColor(hotspot.risk_level)}`,
                    transition: "transform 0.2s, box-shadow 0.2s",
                  }}
                  onClick={() => loadLocationDetails(hotspot.location)}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = "translateY(-4px)";
                    e.currentTarget.style.boxShadow = `0 8px 16px ${getRiskColor(
                      hotspot.risk_level
                    )}40`;
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = "translateY(0)";
                    e.currentTarget.style.boxShadow = "none";
                  }}
                >
                  <h3 style={{ color: "white", marginBottom: "0.5rem" }}>
                    {hotspot.location}
                  </h3>
                  <div
                    style={{
                      fontSize: "2rem",
                      fontWeight: "bold",
                      color: getRiskColor(hotspot.risk_level),
                      margin: "1rem 0",
                    }}
                  >
                    {hotspot.risk_level}
                  </div>
                  <div style={{ color: "#b8bfc8", fontSize: "0.9rem" }}>
                    {getRiskLabel(hotspot.risk_level)}
                  </div>
                  <div
                    style={{
                      marginTop: "1rem",
                      paddingTop: "1rem",
                      borderTop: "1px solid rgba(255,255,255,0.1)",
                      color: "#e0e0e0",
                    }}
                  >
                    <div>
                      Total Crimes: <strong>{hotspot.crime_count}</strong>
                    </div>
                    <div>
                      Most Common: <strong>{hotspot.most_common_crime}</strong>
                    </div>
                    <div>
                      Avg Time:{" "}
                      <strong>{hotspot.avg_hour.toFixed(1)}:00</strong>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {hotspots.length > 15 && (
              <div
                style={{
                  textAlign: "center",
                  color: "#b8bfc8",
                  marginTop: "1rem",
                }}
              >
                Showing top 15 of {hotspots.length} locations
              </div>
            )}
          </>
        )}
      </div>

      {/* Location Details Modal */}
      {selectedLocation && locationDetails && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0,0,0,0.8)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000,
            padding: "2rem",
          }}
          onClick={closeDetails}
        >
          <div
            className="card"
            style={{
              maxWidth: "900px",
              width: "100%",
              maxHeight: "90vh",
              overflow: "auto",
              background: "rgba(20,20,20,0.95)",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "1.5rem",
              }}
            >
              <h2 style={{ color: "white", margin: 0 }}>{selectedLocation}</h2>
              <button
                onClick={closeDetails}
                className="btn"
                style={{ padding: "0.5rem 1rem" }}
              >
                Close
              </button>
            </div>

            <div className="grid grid-2" style={{ marginBottom: "2rem" }}>
              <div className="stat-card">
                <div className="stat-value">{locationDetails.total_crimes}</div>
                <div className="stat-label">Total Crimes</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">
                  {locationDetails.statistics.avg_victim_age}
                </div>
                <div className="stat-label">Avg Victim Age</div>
              </div>
            </div>

            <div style={{ marginBottom: "2rem" }}>
              <h3 style={{ color: "white", marginBottom: "1rem" }}>
                Top Crime Types
              </h3>
              <div className="grid grid-2">
                {Object.entries(locationDetails.statistics.crime_distribution)
                  .slice(0, 6)
                  .map(([crime, count]) => (
                    <div
                      key={crime}
                      style={{
                        background: "rgba(30,30,30,0.6)",
                        padding: "1rem",
                        borderRadius: "8px",
                        border: "1px solid rgba(255,255,255,0.1)",
                      }}
                    >
                      <div style={{ color: "#e0e0e0", fontWeight: "bold" }}>
                        {crime}
                      </div>
                      <div
                        style={{
                          color: "#b8bfc8",
                          fontSize: "1.5rem",
                          marginTop: "0.5rem",
                        }}
                      >
                        {count}
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            <div className="grid grid-2">
              <div>
                <h3 style={{ color: "white", marginBottom: "1rem" }}>
                  Most Dangerous Hours
                </h3>
                {Object.entries(
                  locationDetails.statistics.most_dangerous_hours
                ).map(([hour, count]) => (
                  <div
                    key={hour}
                    style={{
                      background: "rgba(239,68,68,0.1)",
                      padding: "0.75rem",
                      borderRadius: "6px",
                      marginBottom: "0.5rem",
                      color: "#e0e0e0",
                      display: "flex",
                      justifyContent: "space-between",
                    }}
                  >
                    <span>{hour}:00</span>
                    <span style={{ color: "#ef4444" }}>{count} crimes</span>
                  </div>
                ))}
              </div>

              <div>
                <h3 style={{ color: "white", marginBottom: "1rem" }}>
                  Safest Hours
                </h3>
                {Object.entries(locationDetails.statistics.safest_hours).map(
                  ([hour, count]) => (
                    <div
                      key={hour}
                      style={{
                        background: "rgba(16,185,129,0.1)",
                        padding: "0.75rem",
                        borderRadius: "6px",
                        marginBottom: "0.5rem",
                        color: "#e0e0e0",
                        display: "flex",
                        justifyContent: "space-between",
                      }}
                    >
                      <span>{hour}:00</span>
                      <span style={{ color: "#10b981" }}>{count} crimes</span>
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CrimeHotspot;
