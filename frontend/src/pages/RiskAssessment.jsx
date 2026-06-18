import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://localhost:5000/api";

function RiskAssessment() {
  const [formData, setFormData] = useState({
    location: "",
    time: 12,
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [cities, setCities] = useState([]);

  useEffect(() => {
    loadCities();
  }, []);

  const loadCities = async () => {
    try {
      const response = await axios.get(`${API_URL}/visualization/statistics`);
      if (response.data.success && response.data.statistics.top_locations) {
        const locationsList = Object.keys(
          response.data.statistics.top_locations
        );
        setCities(locationsList);
        if (locationsList.length > 0) {
          setFormData((prev) => ({ ...prev, location: locationsList[0] }));
        }
      }
    } catch (err) {
      console.error("Error loading cities:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/risk/assess`, formData);
      if (response.data.success) {
        setResult(response.data);
      } else {
        setError(response.data.message || "Failed to assess risk");
      }
    } catch (err) {
      setError(err.response?.data?.message || "Error assessing risk");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="card-title">Crime Risk Assessment</h1>
        <p className="card-subtitle">
          Get real-time risk score and safety recommendations for any location
          and time
        </p>

        <div className="grid grid-2">
          {/* Input Form */}
          <div className="card" style={{ background: "rgba(20,20,20,0.6)" }}>
            <h3 style={{ color: "white", marginBottom: "1.5rem" }}>
              Assessment Parameters
            </h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Location</label>
                <select
                  value={formData.location}
                  onChange={(e) => handleChange("location", e.target.value)}
                  required
                >
                  <option value="">Select Location</option>
                  {cities.map((city) => (
                    <option key={city} value={city}>
                      {city}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Time of Day</label>
                <select
                  value={formData.time}
                  onChange={(e) =>
                    handleChange("time", parseInt(e.target.value))
                  }
                  required
                >
                  {[...Array(24)].map((_, i) => (
                    <option key={i} value={i}>
                      {i}:00 {i < 12 ? "AM" : "PM"} (
                      {i === 0 ? 12 : i > 12 ? i - 12 : i}:00)
                    </option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading || !formData.location}
                style={{ width: "100%", marginTop: "1rem" }}
              >
                {loading ? "Assessing..." : "Assess Risk"}
              </button>
            </form>

            {error && (
              <div className="error" style={{ marginTop: "1rem" }}>
                {error}
              </div>
            )}
          </div>

          {/* Risk Score Display */}
          {result && (
            <div
              className="card"
              style={{
                background: "rgba(20,20,20,0.6)",
                border: `2px solid ${result.risk_assessment.risk_color}`,
              }}
            >
              <h3 style={{ color: "white", marginBottom: "1.5rem" }}>
                Risk Analysis
              </h3>

              <div
                style={{
                  textAlign: "center",
                  padding: "2rem",
                  background: `${result.risk_assessment.risk_color}20`,
                  borderRadius: "12px",
                  marginBottom: "1.5rem",
                }}
              >
                <div
                  style={{
                    fontSize: "4rem",
                    fontWeight: "bold",
                    color: result.risk_assessment.risk_color,
                  }}
                >
                  {result.risk_assessment.risk_score}
                </div>
                <div
                  style={{
                    fontSize: "1.5rem",
                    color: result.risk_assessment.risk_color,
                    fontWeight: "bold",
                    marginTop: "0.5rem",
                  }}
                >
                  {result.risk_assessment.risk_level} Risk
                </div>
              </div>

              <div className="grid grid-2" style={{ gap: "1rem" }}>
                <div
                  style={{
                    background: "rgba(30,30,30,0.6)",
                    padding: "1rem",
                    borderRadius: "8px",
                    textAlign: "center",
                  }}
                >
                  <div style={{ color: "#b8bfc8", fontSize: "0.9rem" }}>
                    Total Crimes
                  </div>
                  <div
                    style={{
                      color: "#e0e0e0",
                      fontSize: "1.5rem",
                      fontWeight: "bold",
                      marginTop: "0.5rem",
                    }}
                  >
                    {result.risk_assessment.total_historical_crimes}
                  </div>
                </div>
                <div
                  style={{
                    background: "rgba(30,30,30,0.6)",
                    padding: "1rem",
                    borderRadius: "8px",
                    textAlign: "center",
                  }}
                >
                  <div style={{ color: "#b8bfc8", fontSize: "0.9rem" }}>
                    At This Hour
                  </div>
                  <div
                    style={{
                      color: "#e0e0e0",
                      fontSize: "1.5rem",
                      fontWeight: "bold",
                      marginTop: "0.5rem",
                    }}
                  >
                    {result.risk_assessment.crimes_at_this_hour}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Likely Crimes */}
        {result && result.likely_crimes && (
          <div
            className="card"
            style={{ background: "rgba(20,20,20,0.6)", marginTop: "2rem" }}
          >
            <h3 style={{ color: "white", marginBottom: "1.5rem" }}>
              Most Likely Crime Types
            </h3>
            <div className="grid grid-3">
              {result.likely_crimes.map((crime, index) => (
                <div
                  key={index}
                  style={{
                    background: "rgba(30,30,30,0.6)",
                    padding: "1.5rem",
                    borderRadius: "8px",
                    border:
                      index === 0
                        ? `2px solid ${result.risk_assessment.risk_color}`
                        : "1px solid rgba(255,255,255,0.1)",
                  }}
                >
                  <div
                    style={{
                      color: "#b8bfc8",
                      fontSize: "0.9rem",
                      marginBottom: "0.5rem",
                    }}
                  >
                    #{index + 1}
                  </div>
                  <div
                    style={{
                      color: "#e0e0e0",
                      fontSize: "1.1rem",
                      fontWeight: "bold",
                      marginBottom: "0.75rem",
                    }}
                  >
                    {crime.crime_type}
                  </div>
                  <div
                    style={{
                      fontSize: "2rem",
                      fontWeight: "bold",
                      color:
                        index === 0
                          ? result.risk_assessment.risk_color
                          : "#10b981",
                    }}
                  >
                    {crime.probability}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Safety Tips */}
        {result && result.safety_tips && (
          <div
            className="card"
            style={{ background: "rgba(20,20,20,0.6)", marginTop: "2rem" }}
          >
            <h3 style={{ color: "white", marginBottom: "1.5rem" }}>
              Safety Recommendations
            </h3>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "0.75rem",
              }}
            >
              {result.safety_tips.map((tip, index) => (
                <div
                  key={index}
                  style={{
                    background: "rgba(30,30,30,0.6)",
                    padding: "1rem",
                    borderRadius: "8px",
                    color: "#e0e0e0",
                    display: "flex",
                    alignItems: "center",
                    gap: "0.75rem",
                  }}
                >
                  <div
                    style={{
                      width: "32px",
                      height: "32px",
                      borderRadius: "50%",
                      background: "rgba(59,130,246,0.2)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                      fontSize: "1.2rem",
                    }}
                  >
                    {tip.charAt(0)}
                  </div>
                  <div>{tip}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Time Recommendations */}
        {result && result.time_recommendations && (
          <div className="grid grid-2" style={{ marginTop: "2rem" }}>
            <div
              className="card"
              style={{
                background: "rgba(16,185,129,0.1)",
                border: "1px solid rgba(16,185,129,0.3)",
              }}
            >
              <h3 style={{ color: "#10b981", marginBottom: "1rem" }}>
                Safest Hours
              </h3>
              <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
                {result.time_recommendations.safest_hours.map((hour, index) => (
                  <div
                    key={index}
                    style={{
                      background: "rgba(16,185,129,0.2)",
                      color: "#10b981",
                      padding: "0.5rem 1rem",
                      borderRadius: "6px",
                      fontWeight: "bold",
                    }}
                  >
                    {hour}
                  </div>
                ))}
              </div>
            </div>

            <div
              className="card"
              style={{
                background: "rgba(239,68,68,0.1)",
                border: "1px solid rgba(239,68,68,0.3)",
              }}
            >
              <h3 style={{ color: "#ef4444", marginBottom: "1rem" }}>
                Most Dangerous Hours
              </h3>
              <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
                {result.time_recommendations.most_dangerous_hours.map(
                  (hour, index) => (
                    <div
                      key={index}
                      style={{
                        background: "rgba(239,68,68,0.2)",
                        color: "#ef4444",
                        padding: "0.5rem 1rem",
                        borderRadius: "6px",
                        fontWeight: "bold",
                      }}
                    >
                      {hour}
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RiskAssessment;
