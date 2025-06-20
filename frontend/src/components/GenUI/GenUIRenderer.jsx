import React, { useEffect, useState } from "react";

// Map VAE features to UI properties
function getAdaptiveStyles(features) {
  // Defensive: fallback if features missing
  features = Array.isArray(features) && features.length >= 8 ? features : Array(8).fill(0);

  // Example mappings (customize as needed)
  return {
    sidebar: {
      background: `rgba(${200 + features[2] * 20},${220 + features[3] * 15},255,0.95)`,
      width: `${180 + Math.abs(features[0]) * 40}px`,
      fontSize: `${1 + Math.abs(features[1]) * 0.2}rem`,
      padding: `${20 + Math.abs(features[4]) * 8}px`,
      color: features[5] > 0 ? "#1976d2" : "#333",
      order: features[6] > 0 ? 2 : 0 // flip sidebar position
    },
    header: {
      background: `linear-gradient(90deg, #1976d2 ${60 + features[2] * 15}%, #90caf9 ${100 - features[2] * 10}%)`,
      fontSize: `${1.25 + Math.abs(features[1]) * 0.15}rem`,
      color: features[5] > 0.5 ? "#fff" : "#222",
      letterSpacing: `${0.5 + features[0] * 0.2}px`,
      padding: `${18 + Math.abs(features[4]) * 6}px 32px`
    },
    content: {
      background: `rgba(255,255,255,${0.9 - Math.abs(features[3]) * 0.2})`,
      borderRadius: `${16 + Math.abs(features[5]) * 8}px`,
      boxShadow: "0 8px 32px rgba(25, 118, 210, 0.13)",
      padding: `${32 + Math.abs(features[4]) * 10}px`,
      margin: "32px 0",
      fontSize: `${1.1 + Math.abs(features[1]) * 0.1}rem`
    },
    footer: {
      background: features[6] > 0 ? "#1976d2" : "#90caf9",
      color: features[7] > 0 ? "#fff" : "#222",
      fontSize: `${1 + Math.abs(features[1]) * 0.08}rem`,
      letterSpacing: `${0.2 + features[0] * 0.1}px`,
      padding: "18px 0",
      marginTop: 40
    }
  };
}

export default function GenUIRenderer() {
  const [layouts, setLayouts] = useState([]);
  const [current, setCurrent] = useState(0);
  const [error, setError] = useState(null);

  // Fetch adaptive layout JSON
  useEffect(() => {
    fetch("/adaptive_layout.json")
      .then(res => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then(data => setLayouts(data))
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
  if (error) return <div style={{ color: "red", padding: 32 }}>Error loading adaptive UI: {error}</div>;
  if (layouts.length === 0) return <div style={{ padding: 32 }}>Loading adaptive UI...</div>;

  // Get current layout and mapped styles
  const layout = layouts[current];
  const styles = getAdaptiveStyles(layout.features);

  return (
    <div style={{ minHeight: "100vh", background: "#e3eafc", display: "flex", flexDirection: "column" }}>
      {/* Header */}
      <header
        style={{
          ...styles.header,
          width: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between"
        }}
        role="banner"
      >
        <div style={{ fontWeight: 700, fontSize: "1.7em" }}>GenUI Adaptive Platform</div>
        {/* Menu */}
        <nav role="navigation" aria-label="Main Navigation">
          <a href="#" style={{ color: styles.header.color, margin: "0 20px", textDecoration: "none", fontWeight: 600 }}>Home</a>
          <a href="#" style={{ color: styles.header.color, margin: "0 20px", textDecoration: "none", fontWeight: 600 }}>Features</a>
          <a href="#" style={{ color: styles.header.color, margin: "0 20px", textDecoration: "none", fontWeight: 600 }}>About</a>
        </nav>
      </header>

      <div
        style={{
          display: "flex",
          flex: 1,
          flexDirection: "row",
          width: "100%",
          maxWidth: 1300,
          margin: "0 auto"
        }}
      >
        {/* Sidebar */}
        <aside
          style={{
            ...styles.sidebar,
            minHeight: "400px",
            marginTop: 40,
            marginRight: styles.sidebar.order === 0 ? 32 : 0,
            marginLeft: styles.sidebar.order === 2 ? 32 : 0,
            order: styles.sidebar.order,
            borderRadius: 14,
            boxShadow: "0 2px 12px rgba(25,118,210,0.08)",
            display: "flex",
            flexDirection: "column",
            justifyContent: "flex-start",
            alignItems: "flex-start"
          }}
          aria-label="Sidebar"
        >
          <div style={{ fontWeight: 700, marginBottom: 18, fontSize: "1.2em" }}>Sidebar</div>
          <div>User: <b>{layout?.event?.section || "N/A"}</b></div>
          <div>Action: <b>{layout?.event?.action || "N/A"}</b></div>
          <div style={{ marginTop: 24, fontSize: "0.98em" }}>
            <ul style={{ paddingLeft: 18 }}>
              <li>Menu 1</li>
              <li>Menu 2</li>
              <li>Menu 3</li>
            </ul>
          </div>
        </aside>

        {/* Main Content */}
        <main
          style={{
            ...styles.content,
            flex: 1,
            marginTop: 40,
            marginLeft: styles.sidebar.order === 0 ? 0 : 32,
            marginRight: styles.sidebar.order === 2 ? 0 : 32,
            display: "flex",
            flexDirection: "column",
            alignItems: "center"
          }}
          role="main"
        >
          <h2 style={{ margin: 0, color: "#1976d2", fontWeight: 700, fontSize: "2em" }}>
            Adaptive Card: {layout?.event?.action ? layout.event.action.charAt(0).toUpperCase() + layout.event.action.slice(1) : "N/A"}
          </h2>
          <p style={{ margin: "18px 0 0 0" }}>
            Section: <b>{layout?.event?.section || "N/A"}</b><br />
            Width: {typeof layout.width === "number" ? layout.width.toFixed(1) : "N/A"}px<br />
            Height: {typeof layout.height === "number" ? layout.height.toFixed(1) : "N/A"}px
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
            onClick={() => alert("Action triggered!")}
          >
            Action
          </button>
        </main>
      </div>

      {/* Footer */}
      <footer
        style={{
          ...styles.footer,
          width: "100%",
          textAlign: "center"
        }}
        role="contentinfo"
      >
        &copy; {new Date().getFullYear()} GenUI Adaptive Platform &mdash; Powered by VAE
      </footer>
    </div>
  );
}
