import { useEffect, useState } from "react";
import "./App.css";
import Login from "./Login";
import { getIncidents } from "./services/api";

function Dashboard({ onLogout }) {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadIncidents();
  }, []);

  async function loadIncidents() {
    try {
      setLoading(true);
      setError("");

      const data = await getIncidents();

      console.log("Incidents received:", data);

      setIncidents(data);
    } catch (err) {
      console.error("Incident API error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const logout = () => {
    localStorage.removeItem("access_token");
    onLogout();
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>AI Disaster Management Platform</h1>
          <p>Authority Command Center</p>
        </div>

        <button className="logout-button" onClick={logout}>
          Logout
        </button>
      </header>

      <main className="dashboard">

        <section className="card">
          <div className="section-header">
            <h2>Active Incidents</h2>

            <button onClick={loadIncidents}>
              Refresh
            </button>
          </div>

          {loading && (
            <p>Loading incidents...</p>
          )}

          {error && (
            <p className="error">
              {error}
            </p>
          )}

          {!loading && !error && (
            <div className="incident-count">
              {incidents.length} Active Incident
              {incidents.length !== 1 ? "s" : ""}
            </div>
          )}
        </section>

        <section>
          <h2>Current Incidents</h2>

          {!loading && !error && incidents.length === 0 && (
            <p>No active incidents.</p>
          )}

          <div className="incident-list">
            {incidents.map((incident) => (
              <div
                className="incident-card"
                key={incident.id}
              >
                <div className="incident-header">

                  <div>
                    <h3>{incident.title}</h3>

                    <p>
                      {incident.description}
                    </p>
                  </div>

                  <span
                    className={`severity ${incident.severity.toLowerCase()}`}
                  >
                    {incident.severity}
                  </span>

                </div>

                <div className="incident-details">

                  <span>
                    <strong>Type:</strong>{" "}
                    {incident.disaster_type}
                  </span>

                  <span>
                    <strong>Status:</strong>{" "}
                    {incident.status}
                  </span>

                  <span>
                    <strong>Priority:</strong>{" "}
                    {incident.priority_score}
                  </span>

                  <span>
                    <strong>Location:</strong>{" "}
                    {incident.latitude},{" "}
                    {incident.longitude}
                  </span>

                </div>
              </div>
            ))}
          </div>
        </section>

      </main>
    </div>
  );
}

function App() {
  const [authenticated, setAuthenticated] = useState(
    Boolean(localStorage.getItem("access_token"))
  );

  if (!authenticated) {
    return (
      <Login
        onLogin={() => setAuthenticated(true)}
      />
    );
  }

  return (
    <Dashboard
      onLogout={() => setAuthenticated(false)}
    />
  );
}

export default App;