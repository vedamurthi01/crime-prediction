import React, { useState } from "react";
import { predictCriminal } from "../services/api";

function CriminalPrediction() {
  const [formData, setFormData] = useState({
    crime_type: "",
    location: "",
    time: 12,
    modus_operandi: "",
    district: "",
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "time" ? parseInt(value) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictCriminal(formData);
      setResult(data);
    } catch (err) {
      setError("Error predicting suspects: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="card-title" style={{ color: "white" }}>
          Criminal Identification
        </h1>
        <p className="card-subtitle">
          Identify top suspect matches using KNN algorithm
        </p>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="grid grid-2">
            <div className="form-group">
              <label className="form-label">Crime Type</label>
              <select
                name="crime_type"
                value={formData.crime_type}
                onChange={handleChange}
                className="form-select"
                required
              >
                <option value="">Select Crime Type</option>
                <option value="ARSON">ARSON</option>
                <option value="ASSAULT">ASSAULT</option>
                <option value="BURGLARY">BURGLARY</option>
                <option value="COUNTERFEITING">COUNTERFEITING</option>
                <option value="CYBERCRIME">CYBERCRIME</option>
                <option value="DOMESTIC VIOLENCE">DOMESTIC VIOLENCE</option>
                <option value="DRUG OFFENSE">DRUG OFFENSE</option>
                <option value="EXTORTION">EXTORTION</option>
                <option value="FIREARM OFFENSE">FIREARM OFFENSE</option>
                <option value="FRAUD">FRAUD</option>
                <option value="HOMICIDE">HOMICIDE</option>
                <option value="IDENTITY THEFT">IDENTITY THEFT</option>
                <option value="ILLEGAL POSSESSION">ILLEGAL POSSESSION</option>
                <option value="KIDNAPPING">KIDNAPPING</option>
                <option value="PUBLIC INTOXICATION">PUBLIC INTOXICATION</option>
                <option value="ROBBERY">ROBBERY</option>
                <option value="SEXUAL ASSAULT">SEXUAL ASSAULT</option>
                <option value="SHOPLIFTING">SHOPLIFTING</option>
                <option value="TRAFFIC VIOLATION">TRAFFIC VIOLATION</option>
                <option value="VANDALISM">VANDALISM</option>
                <option value="VEHICLE - STOLEN">VEHICLE - STOLEN</option>
              </select>
            </div>

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
                name="modus_operandi"
                value={formData.modus_operandi}
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
          </div>

          <button type="submit" disabled={loading} className="btn btn-primary">
            {loading ? "Searching..." : "Identify Suspects"}
          </button>
        </form>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Searching suspect database...</p>
          </div>
        )}

        {result && result.success && (
          <div className="result-box">
            <h3 className="result-title" style={{ color: "white" }}>
              Top 5 Suspect Matches
            </h3>

            <ul className="suspect-list">
              {result.top_suspects?.map((suspect) => (
                <li key={suspect.suspect_id} className="suspect-item">
                  <span className="suspect-rank">#{suspect.rank}</span>

                  <div>
                    <h4 style={{ marginBottom: "0.5rem", color: "white" }}>
                      {suspect.name}
                    </h4>
                    <p style={{ color: "#b0b0b0", fontSize: "0.9rem" }}>
                      <strong>ID:</strong> {suspect.suspect_id} |
                      <strong> Age:</strong> {suspect.age} |
                      <strong> Similarity:</strong>{" "}
                      {(suspect.similarity_score * 100).toFixed(1)}%
                    </p>
                    <p style={{ color: "#b0b0b0", fontSize: "0.9rem" }}>
                      <strong>Known Crime:</strong> {suspect.known_crime_type} |
                      <strong> Location:</strong> {suspect.known_location}
                    </p>
                  </div>
                </li>
              ))}
            </ul>

            {result.top_suspects?.length === 0 && (
              <p
                style={{ textAlign: "center", color: "white", padding: "2rem" }}
              >
                No matching suspects found in database
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default CriminalPrediction;
