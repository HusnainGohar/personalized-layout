import React, { useEffect, useState } from "react";
import "./GenUIRenderer.css"                        

const AdaptiveForm = () => {
  const [layout, setLayout] = useState(null);
  const [formData, setFormData] = useState({});
  const [error, setError] = useState(null);

  // Fetch the adaptive layout from generatedLayouts.json
  useEffect(() => {
    fetch("/generatedLayouts.json")
      .then(res => {
        if (!res.ok) throw new Error("Failed to load adaptive layout");
        return res.json();
      })
      .then(data => {
        // For demo, use the first layout; or select based on user/context
        if (Array.isArray(data) && data.length > 0) {
          setLayout(data[0]);
        } else {
          throw new Error("No layout data found");
        }
      })
      .catch(err => setError(err.message));
  }, []);

  // Example: Map VAE features to form fields and style
  function getFieldsAndStyle(features) {
    // You can customize this mapping based on your VAE output meaning
    return {
      fields: [
        {
          label: "Name",
          type: "text",
          width: 220 + (features[0] || 0) * 10,
          color: `rgba(230,245,255,${0.7 + (features[1] || 0) * 0.05})`
        },
        {
          label: "Email",
          type: "email",
          width: 220 + (features[2] || 0) * 10,
          color: `rgba(255,245,230,${0.7 + (features[3] || 0) * 0.05})`
        },
        {
          label: "Password",
          type: "password",
          width: 220 + (features[4] || 0) * 10,
          color: `rgba(245,230,255,${0.7 + (features[5] || 0) * 0.05})`
        }
      ],
      style: {
        background: `linear-gradient(135deg, #e3f2fd ${(features[6] || 0) * 10}%, #fce4ec ${(features[7] || 0) * 10}%)`,
        borderRadius: 16 + Math.abs(features[8] || 0) * 4,
        padding: 32 + Math.abs(features[9] || 0) * 2
      }
    };
  }

  if (error) return <div className="error">{error}</div>;
  if (!layout) return <div>Loading adaptive form...</div>;

  // Map VAE features to UI
  const { fields, style } = getFieldsAndStyle(layout.features);

  const handleChange = (label, value) => {
    setFormData(prev => ({ ...prev, [label]: value }));
  };

  const handleSubmit = e => {
    e.preventDefault();
    alert("Form submitted!\n" + JSON.stringify(formData, null, 2));
  };

  return (
    <form
      className="adaptive-form"
      style={{
        ...style,
        width: 360,
        margin: "40px auto",
        boxShadow: "0 2px 12px rgba(0,0,0,0.12)"
      }}
      onSubmit={handleSubmit}
    >
      <h3 style={{ textAlign: "center", marginBottom: 24 }}>
        Adaptive Form (Layout #{layout.layout_id})
      </h3>
      {fields.map((field, idx) => (
        <div key={idx} style={{ marginBottom: 18 }}>
          <label style={{ display: "block", marginBottom: 6 }}>{field.label}</label>
          <input
            type={field.type}
            value={formData[field.label] || ""}
            onChange={e => handleChange(field.label, e.target.value)}
            style={{
              width: field.width,
              background: field.color,
              border: "1px solid #ccc",
              borderRadius: 6,
              padding: "8px 12px",
              fontSize: "1rem"
            }}
            required
          />
        </div>
      ))}
      <button
        type="submit"
        style={{
          width: "100%",
          padding: "10px 0",
          background: "#1976d2",
          color: "#fff",
          border: "none",
          borderRadius: 6,
          fontWeight: "bold"
        }}
      >
        Submit
      </button>
    </form>
  );
};

export default AdaptiveForm;
