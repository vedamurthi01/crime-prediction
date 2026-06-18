import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { getTrainingStatus } from "../services/api";
import "./HomePage.css";

function HomePage() {
  const [trainingStatus, setTrainingStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    try {
      const data = await getTrainingStatus();
      setTrainingStatus(data);
    } catch (error) {
      console.error("Error loading status:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home-page">
      <div className="container">
        <div className="card">
          <h1 className="card-title">Crime Prediction System</h1>
          <p className="card-subtitle">
            Advanced ML-based crime type prediction with real-time analytics
            using multiple machine learning algorithms
          </p>

          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p>Loading system status...</p>
            </div>
          ) : (
            <>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">
                    {trainingStatus?.models?.crime_type_model ? "✓" : "✗"}
                  </div>
                  <div className="stat-label">Crime Type Model</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">29</div>
                  <div className="stat-label">Cities Covered</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">40K+</div>
                  <div className="stat-label">Training Records</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">5</div>
                  <div className="stat-label">Core Features</div>
                </div>
              </div>

              <div className="grid grid-2">
                <div className="card">
                  <h3 style={{ color: "white" }}>Features</h3>
                  <ul
                    style={{
                      lineHeight: "2",
                      marginLeft: "1.5rem",
                      color: "white",
                    }}
                  >
                    <li>Crime Type Prediction (6 ML Algorithms)</li>
                    <li>Crime Hotspot Mapping with Filters</li>
                    <li>Real-time Risk Assessment Tool</li>
                    <li>Interactive Analytics Dashboard</li>
                    <li>Crime Trends & Visualizations</li>
                    <li>Location-based Safety Insights</li>
                  </ul>
                </div>

                <div className="card">
                  <h3 style={{ color: "white" }}>Quick Start</h3>
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      gap: "1rem",
                      marginTop: "1rem",
                    }}
                  >
                    {!trainingStatus?.all_trained && (
                      <Link to="/train" className="btn btn-primary">
                        Train Models First
                      </Link>
                    )}
                    <Link to="/predict-crime" className="btn btn-primary">
                      Predict Crime Type
                    </Link>
                    <Link to="/hotspot" className="btn btn-primary">
                      Crime Hotspot Map
                    </Link>
                    <Link to="/risk" className="btn btn-primary">
                      Risk Assessment
                    </Link>
                    <Link to="/analytics" className="btn btn-secondary">
                      Analytics Dashboard
                    </Link>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
