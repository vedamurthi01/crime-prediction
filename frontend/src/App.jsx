import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useLocation,
} from "react-router-dom";
import "./App.css";

// Pages
import HomePage from "./pages/HomePage";
import CrimeTypePrediction from "./pages/CrimeTypePrediction";
import AnalyticsDashboard from "./pages/AnalyticsDashboard";
import TrainingPage from "./pages/TrainingPage";
import CrimeHotspot from "./pages/CrimeHotspot";
import RiskAssessment from "./pages/RiskAssessment";

function Navigation() {
  const location = useLocation();

  const isActive = (path) => (location.pathname === path ? "active" : "");

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-brand">
          Crime Prediction System
        </Link>
        <ul className="nav-links">
          <li>
            <Link to="/" className={isActive("/")}>
              Home
            </Link>
          </li>
          <li>
            <Link to="/train" className={isActive("/train")}>
              Training
            </Link>
          </li>
          <li>
            <Link to="/predict-crime" className={isActive("/predict-crime")}>
              Crime Prediction
            </Link>
          </li>
          <li>
            <Link to="/hotspot" className={isActive("/hotspot")}>
              Crime Hotspot
            </Link>
          </li>
          <li>
            <Link to="/risk" className={isActive("/risk")}>
              Risk Assessment
            </Link>
          </li>
          <li>
            <Link to="/analytics" className={isActive("/analytics")}>
              Analytics
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <Navigation />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/train" element={<TrainingPage />} />
          <Route path="/predict-crime" element={<CrimeTypePrediction />} />
          <Route path="/hotspot" element={<CrimeHotspot />} />
          <Route path="/risk" element={<RiskAssessment />} />
          <Route path="/analytics" element={<AnalyticsDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
