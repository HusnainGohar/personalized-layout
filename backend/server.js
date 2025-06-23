const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.options('*', cors());

const eventsFile = path.join(__dirname, 'utils', 'user_events.json');

app.post('/api/user-event', (req, res) => {
  const event = req.body;
  fs.appendFile(eventsFile, JSON.stringify(event) + '\n', (err) => {
    if (err) {
      console.error('Failed to save user event:', err);
      return res.status(500).json({ success: false });
    }
    res.json({ success: true });
  });
});

app.post('/api/generate-layout', (req, res) => {
  // Aggregate click counts per component from user_events.json
  const eventsFile = path.join(__dirname, 'utils', 'user_events.json');
  fs.readFile(eventsFile, 'utf8', (err, data) => {
    let featureVector = [];
    if (!err && data) {
      try {
        const events = data.trim().split('\n').map(line => JSON.parse(line));
        // List of known components (order matters for feature vector)
        const components = [
          'dashboard-menu', 'profile-menu', 'settings-menu',
          'analytics-card', 'profile-card', 'notifications-card', 'adaptive-action-btn'
        ];
        // Count clicks per component
        const counts = {};
        components.forEach(c => counts[c] = 0);
        events.forEach(ev => {
          if (ev.eventType === 'click' && ev.eventData && ev.eventData.component && counts.hasOwnProperty(ev.eventData.component)) {
            counts[ev.eventData.component] += 1;
          }
        });
        featureVector = components.map(c => counts[c]);
        // Pad or trim to input_dim (60)
        while (featureVector.length < 60) featureVector.push(0);
        if (featureVector.length > 60) featureVector = featureVector.slice(0, 60);
      } catch (e) {
        featureVector = Array(60).fill(0);
      }
    } else {
      featureVector = Array(60).fill(0);
    }
    // Call Python script with feature vector
    const featureArg = `'${JSON.stringify(featureVector)}'`;
    exec(`python ../deep-learning/generate_layouts.py ${featureArg}`, (error, stdout, stderr) => {
      if (error) {
        console.error('Error generating layout:', error);
        return res.status(500).json({ success: false, error: error.message });
      }
      // Read the generated layout JSON
      const layoutPath = path.join(__dirname, '..', 'frontend', 'public', 'generatedLayouts.json');
      fs.readFile(layoutPath, 'utf8', (err, data) => {
        if (err) {
          console.error('Error reading generated layout:', err);
          return res.status(500).json({ success: false, error: err.message });
        }
        res.json({ success: true, layout: JSON.parse(data), featureVector });
      });
    });
  });
});

// Function to run retraining pipeline
function retrainModel() {
  console.log('Starting automatic retraining...');
  const retrainScript = path.join(__dirname, '..', 'retrain_pipeline.bat');
  const projectRoot = path.join(__dirname, '..');
  exec(`"${retrainScript}"`, { cwd: projectRoot }, (error, stdout, stderr) => {
    if (error) {
      console.error(`Retrain error: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`Retrain stderr: ${stderr}`);
      return;
    }
    console.log(`Retrain output: ${stdout}`);
  });
}

// Run retraining every 24 hours (86,400,000 ms)
setInterval(retrainModel, 24 * 60 * 60 * 1000);

// Optionally, run once on server start
retrainModel();

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
