const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(bodyParser.json());

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

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
