import React, { useState } from "react";
import { predictCrimeType } from "../services/api";
import "./CrimeTypePrediction.css";

function CrimeTypePrediction() {
  const [formData, setFormData] = useState({
    location: "",
    time: 12,
    weapon_used: "",
    victim_age: 30,
    suspect_age: 30,
    month: 1,
    weekday: 0,
    district: "",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "time" ||
        name === "victim_age" ||
        name === "suspect_age" ||
        name === "month" ||
        name === "weekday"
          ? parseInt(value)
          : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictCrimeType(formData);
      setResult(data);
    } catch (err) {
      setError("Error predicting crime type: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="crime-prediction-page">
      <div className="container">
        <div className="card">
          <h1 className="card-title" style={{ color: "white" }}>
            Crime Type Prediction
          </h1>
          <p className="card-subtitle">
            Predict the type of crime based on various factors
          </p>

          {error && <div className="error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="grid grid-2">
              <div className="form-group">
                <label className="form-label">Location</label>
                <select
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  className="form-select"
                  required
                >
                  <option value="">Select Location</option>
                  <option value="Agra">Agra</option>
                  <option value="Ahmedabad">Ahmedabad</option>
                  <option value="Bangalore">Bangalore</option>
                  <option value="Bhopal">Bhopal</option>
                  <option value="Chennai">Chennai</option>
                  <option value="Delhi">Delhi</option>
                  <option value="Faridabad">Faridabad</option>
                  <option value="Ghaziabad">Ghaziabad</option>
                  <option value="Hyderabad">Hyderabad</option>
                  <option value="Indore">Indore</option>
                  <option value="Jaipur">Jaipur</option>
                  <option value="Kalyan">Kalyan</option>
                  <option value="Kanpur">Kanpur</option>
                  <option value="Kolkata">Kolkata</option>
                  <option value="Lucknow">Lucknow</option>
                  <option value="Ludhiana">Ludhiana</option>
                  <option value="Meerut">Meerut</option>
                  <option value="Mumbai">Mumbai</option>
                  <option value="Nagpur">Nagpur</option>
                  <option value="Nashik">Nashik</option>
                  <option value="Patna">Patna</option>
                  <option value="Pune">Pune</option>
                  <option value="Rajkot">Rajkot</option>
                  <option value="Surat">Surat</option>
                  <option value="Thane">Thane</option>
                  <option value="Vadodara">Vadodara</option>
                  <option value="Varanasi">Varanasi</option>
                  <option value="Vasai">Vasai</option>
                  <option value="Visakhapatnam">Visakhapatnam</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">District</label>
                <select
                  name="district"
                  value={formData.district}
                  onChange={handleChange}
                  className="form-select"
                >
                  <option value="">Select District</option>
                  <option value="Agra">Agra</option>
                  <option value="Ahmedabad">Ahmedabad</option>
                  <option value="Bangalore">Bangalore</option>
                  <option value="Bhopal">Bhopal</option>
                  <option value="Chennai">Chennai</option>
                  <option value="Delhi">Delhi</option>
                  <option value="Hyderabad">Hyderabad</option>
                  <option value="Jaipur">Jaipur</option>
                  <option value="Kolkata">Kolkata</option>
                  <option value="Lucknow">Lucknow</option>
                  <option value="Mumbai">Mumbai</option>
                  <option value="Pune">Pune</option>
                  <option value="Surat">Surat</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Time (Hour: 0-23)</label>
                <input
                  type="number"
                  name="time"
                  value={formData.time}
                  onChange={handleChange}
                  className="form-input"
                  min="0"
                  max="23"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Weapon Used</label>
                <select
                  name="weapon_used"
                  value={formData.weapon_used}
                  onChange={handleChange}
                  className="form-select"
                  required
                >
                  <option value="">Select Weapon</option>
                  <option value="Firearm">Firearm</option>
                  <option value="Knife">Knife</option>
                  <option value="Blunt Object">Blunt Object</option>
                  <option value="Poison">Poison</option>
                  <option value="Explosives">Explosives</option>
                  <option value="None">None</option>
                  <option value="Other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Victim Age</label>
                <input
                  type="number"
                  name="victim_age"
                  value={formData.victim_age}
                  onChange={handleChange}
                  className="form-input"
                  min="0"
                  max="120"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Suspect Age</label>
                <input
                  type="number"
                  name="suspect_age"
                  value={formData.suspect_age}
                  onChange={handleChange}
                  className="form-input"
                  min="0"
                  max="120"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Month (1-12)</label>
                <input
                  type="number"
                  name="month"
                  value={formData.month}
                  onChange={handleChange}
                  className="form-input"
                  min="1"
                  max="12"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Weekday (0=Mon, 6=Sun)</label>
                <input
                  type="number"
                  name="weekday"
                  value={formData.weekday}
                  onChange={handleChange}
                  className="form-input"
                  min="0"
                  max="6"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? "Predicting..." : "Predict Crime Type"}
            </button>
          </form>

          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Analyzing crime patterns...</p>
            </div>
          )}

          {result && result.success && (
            <div className="result-box">
              <h3 className="result-title" style={{ color: "white" }}>
                Prediction Results
              </h3>

              <div style={{ marginBottom: "1.5rem" }}>
                <h4 style={{ color: "white", fontSize: "1.5rem" }}>
                  {result.predicted_crime_type}
                </h4>
                <p style={{ color: "white" }}>
                  Confidence: {(result.confidence * 100).toFixed(2)}%
                </p>
              </div>

              <h4 style={{ marginBottom: "1rem", color: "white" }}>
                Top 3 Predictions:
              </h4>
              {result.top_predictions?.map((pred, index) => (
                <div
                  key={index}
                  style={{
                    background: index === 0 ? "#3a3a3a" : "#2a2a2a",
                    padding: "1rem",
                    marginBottom: "0.5rem",
                    borderRadius: "8px",
                    border: "1px solid #404040",
                    color: "white",
                  }}
                >
                  <strong>
                    #{index + 1}: {pred.crime_type}
                  </strong>
                  <span style={{ float: "right", color: "#b0b0b0" }}>
                    {(pred.probability * 100).toFixed(2)}%
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CrimeTypePrediction;
