import React, { useEffect, useState } from "react";
import { logUserEvent } from '../../data/eventLogger';

// Map VAE features to UI properties (customize as needed)
function getAdaptiveStyles(features) {
  features = Array.isArray(features) && features.length >= 8 ? features : Array(8).fill(0);
  return {
    sidebar: {
      background: `linear-gradient(135deg, #e3f0ff 0%, #c9e7ff 100%)`,
      width: `${220 + Math.abs(features[0]) * 40}px`,
      fontSize: `${1 + Math.abs(features[1]) * 0.18}rem`,
      padding: `${28 + Math.abs(features[4]) * 8}px 24px`,
      color: features[5] > 0 ? "#1976d2" : "#333",
      borderRadius: 18,
      boxShadow: "0 4px 24px rgba(25, 118, 210, 0.10)",
      minHeight: 500,
      margin: "32px 0 32px 0"
    },
    header: {
      background: `linear-gradient(90deg, #1976d2 60%, #90caf9 100%)`,
      fontSize: `${1.35 + Math.abs(features[1]) * 0.12}rem`,
      color: "#fff",
      letterSpacing: `${0.5 + features[0] * 0.2}px`,
      padding: `28px 48px 22px 48px`,
      borderRadius: "0 0 24px 24px",
      boxShadow: "0 2px 16px rgba(25, 118, 210, 0.10)"
    },
    content: {
      background: `#fff`,
      borderRadius: 24,
      boxShadow: "0 8px 32px rgba(25, 118, 210, 0.13)",
      padding: `${40 + Math.abs(features[4]) * 10}px 48px`,
      margin: "40px 0",
      fontSize: `${1.12 + Math.abs(features[1]) * 0.1}rem`,
      minHeight: 400,
      display: "flex",
      flexDirection: "column",
      gap: 32
    },
    card: {
      background: `linear-gradient(135deg, #f5faff 0%, #e3f0ff 100%)`,
      borderRadius: 18,
      boxShadow: "0 2px 12px rgba(25,118,210,0.08)",
      padding: "28px 32px",
      marginBottom: 18,
      minWidth: 220,
      minHeight: 120,
      display: "flex",
      flexDirection: "column",
      justifyContent: "center"
    },
    footer: {
      background: "#1976d2",
      color: "#fff",
      fontSize: `${1 + Math.abs(features[1]) * 0.08}rem`,
      letterSpacing: `${0.2 + features[0] * 0.1}px`,
      padding: "22px 0",
      marginTop: 40,
      borderRadius: "18px 18px 0 0"
    }
  };
}

export default function GenUIRenderer() {
  const [layouts, setLayouts] = useState([]);
  const [current, setCurrent] = useState(0);
  const [error, setError] = useState(null);
  const [featureVector, setFeatureVector] = useState([]);

  // Fetch adaptive layout JSON from backend
  useEffect(() => {
    fetch("http://localhost:5000/api/generate-layout", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    })
      .then(res => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then(data => {
        setLayouts(data.layout);
        setFeatureVector(data.featureVector || []);
      })
      .catch(err => setError(err.message));
  }, []);

  // Auto-cycle layouts to simulate real-time adaptation
  useEffect(() => {
    if (layouts.length > 1) {
      const timer = setInterval(() => {
        setCurrent(prev => (prev + 1) % layouts.length);
      }, 3000);
      return () => clearInterval(timer);
    }
  }, [layouts]);

  // Loading and error states
  if (error) return <div style={{ color: "#d32f2f", padding: 32, fontWeight: 600 }}>Error loading adaptive UI: {error}</div>;
  if (layouts.length === 0) return <div style={{ padding: 32 }}>Loading adaptive UI...</div>;

  // Get current layout and mapped styles
  const layout = layouts[current];
  const styles = getAdaptiveStyles(layout.features);

  // Card reordering logic
  const cardDefs = [
    { id: 'analytics-card', content: (
      <div style={styles.card} onClick={() => logUserEvent('click', { component: 'analytics-card' })}>
        <div style={{ fontWeight: 700, fontSize: "1.2em", marginBottom: 8 }}>Analytics Overview</div>
        <div style={{ fontSize: "1.05em", color: "#1976d2" }}>Sessions: <b>1,245</b></div>
        <div style={{ fontSize: "1.05em", color: "#1976d2" }}>Active Users: <b>87</b></div>
        <div style={{ fontSize: "1.05em", color: "#1976d2" }}>Bounce Rate: <b>32%</b></div>
      </div>
    ) },
    { id: 'profile-card', content: (
      <div style={styles.card} onClick={() => logUserEvent('click', { component: 'profile-card' })}>
        <div style={{ fontWeight: 700, fontSize: "1.2em", marginBottom: 8 }}>User Profile</div>
        <div style={{ fontSize: "1.05em" }}><b>Name:</b> Jane Doe</div>
        <div style={{ fontSize: "1.05em" }}><b>Email:</b> jane.doe@email.com</div>
        <div style={{ fontSize: "1.05em" }}><b>Status:</b> Active</div>
      </div>
    ) },
    { id: 'notifications-card', content: (
      <div style={styles.card} onClick={() => logUserEvent('click', { component: 'notifications-card' })}>
        <div style={{ fontWeight: 700, fontSize: "1.2em", marginBottom: 8 }}>Notifications</div>
        <ul style={{ paddingLeft: 18, fontSize: "1.05em" }}>
          <li>🔔 New message from support</li>
          <li>🔔 Your report is ready</li>
          <li>🔔 System update available</li>
        </ul>
      </div>
    ) }
  ];
  // Map card IDs to featureVector indices
  const cardOrder = [3, 4, 5]; // analytics-card, profile-card, notifications-card
  const sortedCards = cardDefs
    .map((card, i) => ({ ...card, clicks: featureVector[cardOrder[i]] || 0 }))
    .sort((a, b) => b.clicks - a.clicks);

  return (
    <div style={{ minHeight: "100vh", background: "#e3eafc", display: "flex", flexDirection: "column" }}>
      {/* Header */}
      <header style={styles.header} role="banner">
        <div style={{ fontWeight: 700, fontSize: "2.1em", letterSpacing: 1 }}>GenUI Adaptive Platform</div>
        <nav role="navigation" aria-label="Main Navigation" style={{ marginTop: 12 }}>
          <a href="#" style={{ color: "#fff", margin: "0 28px", textDecoration: "none", fontWeight: 600, fontSize: "1.1em" }}>Home</a>
          <a href="#" style={{ color: "#fff", margin: "0 28px", textDecoration: "none", fontWeight: 600, fontSize: "1.1em" }}>Features</a>
          <a href="#" style={{ color: "#fff", margin: "0 28px", textDecoration: "none", fontWeight: 600, fontSize: "1.1em" }}>About</a>
        </nav>
      </header>

      <div style={{ display: "flex", flex: 1, flexDirection: "row", width: "100%", maxWidth: 1400, margin: "0 auto" }}>
        {/* Sidebar */}
        <aside style={styles.sidebar} aria-label="Sidebar">
          <div style={{ fontWeight: 700, marginBottom: 18, fontSize: "1.3em", color: "#1976d2" }}>Welcome, User!</div>
          <div style={{ marginBottom: 18, fontSize: "1.05em" }}>
            <b>Profile:</b> <span style={{ color: "#1976d2" }}>Pro Member</span>
          </div>
          <div style={{ marginBottom: 18, fontSize: "1.05em" }}>
            <b>Notifications:</b> <span style={{ color: "#1976d2" }}>3 new</span>
          </div>
          <div style={{ marginTop: 24, fontSize: "1.05em" }}>
            <ul style={{ paddingLeft: 18, listStyle: "none" }}>
              <li style={{ marginBottom: 10 }} onClick={() => logUserEvent('click', { component: 'dashboard-menu' })}><span role="img" aria-label="dashboard">📊</span> Dashboard</li>
              <li style={{ marginBottom: 10 }} onClick={() => logUserEvent('click', { component: 'profile-menu' })}><span role="img" aria-label="profile">👤</span> Profile</li>
              <li style={{ marginBottom: 10 }} onClick={() => logUserEvent('click', { component: 'settings-menu' })}><span role="img" aria-label="settings">⚙️</span> Settings</li>
            </ul>
          </div>
        </aside>

        {/* Main Content */}
        <main style={styles.content} role="main">
          <div style={{ display: "flex", gap: 32, flexWrap: "wrap" }}>
            {sortedCards.map(card => card.content)}
          </div>
          {/* Main Adaptive Card */}
          <div style={{ ...styles.card, marginTop: 32, minWidth: 320 }}>
            <h2 style={{ margin: 0, color: "#1976d2", fontWeight: 700, fontSize: "2em" }}>
              Adaptive Card Demo
            </h2>
            <p style={{ margin: "18px 0 0 0" }}>
              This area will adapt its style, spacing, and layout based on the generative model output.<br />
              <span style={{ color: "#1976d2", fontWeight: 600 }}>Try retraining or changing the VAE features!</span>
            </p>
            <button
              style={{
                marginTop: 26,
                padding: "12px 32px",
                borderRadius: 8,
                border: "none",
                background: "#1976d2",
                color: "#fff",
                fontWeight: 700,
                fontSize: "1.15rem",
                boxShadow: "0 1px 4px #1976d255",
                cursor: "pointer"
              }}
              aria-label="Trigger adaptive action"
              onClick={() => { logUserEvent('click', { component: 'adaptive-action-btn' }); alert("Action triggered!"); }}
            >
              Action
            </button>
          </div>
        </main>
      </div>

      {/* Footer */}
      <footer style={styles.footer} role="contentinfo">
        &copy; {new Date().getFullYear()} GenUI Adaptive Platform &mdash; Powered by VAE
      </footer>
    </div>
  );
}
