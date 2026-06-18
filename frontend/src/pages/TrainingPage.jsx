import React, { useState } from "react";
import { trainCrimeTypeModel, trainCriminalKNN } from "../services/api";

function TrainingPage() {
  const [crimeTypeTraining, setCrimeTypeTraining] = useState(false);
  const [knnTraining, setKnnTraining] = useState(false);
  const [crimeTypeResult, setCrimeTypeResult] = useState(null);
  const [knnResult, setKnnResult] = useState(null);
  const [error, setError] = useState(null);

  const handleTrainCrimeType = async () => {
    setCrimeTypeTraining(true);
    setError(null);
    setCrimeTypeResult(null);

    try {
      const result = await trainCrimeTypeModel();
      setCrimeTypeResult(result);
    } catch (err) {
      setError("Error training crime type model: " + err.message);
    } finally {
      setCrimeTypeTraining(false);
    }
  };

  const handleTrainKNN = async () => {
    setKnnTraining(true);
    setError(null);
    setKnnResult(null);

    try {
      const result = await trainCriminalKNN(5);
      setKnnResult(result);
    } catch (err) {
      setError("Error training KNN model: " + err.message);
    } finally {
      setKnnTraining(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="card-title" style={{ color: "white" }}>
          Model Training
        </h1>
        <p className="card-subtitle">
          Train machine learning models on crime datasets
        </p>

        {error && <div className="error">{error}</div>}

        <div className="grid grid-2">
          {/* Crime Type Model Training */}
          <div className="card">
            <h3 style={{ color: "white" }}>Crime Type Prediction Models</h3>
            <p style={{ color: "white", marginBottom: "1rem" }}>
              Trains 6 different ML algorithms and selects the best performer:
            </p>
            <ul
              style={{
                marginLeft: "1.5rem",
                marginBottom: "1.5rem",
                color: "white",
              }}
            >
              <li>Logistic Regression</li>
              <li>Decision Tree</li>
              <li>Random Forest</li>
              <li>XGBoost</li>
              <li>SVM</li>
              <li>Naive Bayes</li>
            </ul>

            <button
              onClick={handleTrainCrimeType}
              disabled={crimeTypeTraining}
              className="btn btn-primary"
            >
              {crimeTypeTraining ? "Training..." : "Train Crime Type Models"}
            </button>

            {crimeTypeTraining && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Training models... This may take a few minutes</p>
              </div>
            )}

            {crimeTypeResult && crimeTypeResult.success && (
              <div className="result-box">
                <h4 className="result-title" style={{ color: "white" }}>
                  Training Completed
                </h4>
                <p style={{ color: "white" }}>
                  <strong>Best Model:</strong> {crimeTypeResult.best_model}
                </p>
                <p style={{ color: "white" }}>
                  <strong>Accuracy:</strong>{" "}
                  {(crimeTypeResult.accuracy * 100).toFixed(2)}%
                </p>

                <h5
                  style={{
                    marginTop: "1rem",
                    marginBottom: "0.5rem",
                    color: "white",
                  }}
                >
                  All Models Performance:
                </h5>
                {Object.entries(crimeTypeResult.all_models || {}).map(
                  ([name, metrics]) => (
                    <div
                      key={name}
                      style={{
                        marginBottom: "0.5rem",
                        paddingLeft: "1rem",
                        color: "white",
                      }}
                    >
                      <strong>{name}:</strong>{" "}
                      {(metrics.accuracy * 100).toFixed(2)}%
                    </div>
                  )
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default TrainingPage;
