# Generative Adaptive UI System

## Overview
This project is a full-stack Generative Adaptive UI System that uses a Variational Autoencoder (VAE) to generate and adapt web UI layouts in real time based on user interaction data. It consists of:
- **Frontend:** React app for adaptive UI rendering and user event logging
- **Backend:** Express.js server for event collection and API endpoints
- **Deep Learning Module:** Python VAE for generative layout modeling
- **Data Pipeline:** Scripts for processing, aggregating, and combining user and UI data

---

## Project Structure
```
.
├── backend/                # Express backend server
│   └── utils/user_events.json  # User event logs
├── data/
│   ├── processed/          # Processed CSVs for model input
│   ├── raw/                # Raw datasets
│   └── scripts/            # Data processing scripts
├── deep-learning/          # VAE model, training, and generation scripts
│   └── models/vae_trained.pth  # Trained model
├── frontend/               # React frontend app
│   └── public/generatedLayouts.json # Generated layouts
└── README.md               # This file
```

---

## Quick Start

### 1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd personalized-layouts
```

### 2. **Set Up Python Environment (Deep Learning & Data Processing)**
```bash
python -m venv myenv
# On Windows:
myenv\Scripts\activate
# On Mac/Linux:
source myenv/bin/activate
pip install torch pandas scikit-learn
```

### 3. **Set Up Backend (Express Server)**
```bash
cd backend
npm install
node server.js
```

### 4. **Set Up Frontend (React App)**
```bash
cd ../frontend
npm install
npm start
```

---

## Running the System

### **Start Backend**
```bash
cd backend
node server.js
```

### **Start Frontend**
```bash
cd frontend
npm start
```

### **(Optional) Generate Layouts**
```bash
python deep-learning/generate_layouts.py
```

---

## Retraining the Model
If you want to retrain the VAE model (e.g., after updating data):

1. **Aggregate user events:**
   ```bash
   python data/scripts/aggregate_user_events.py
   ```
2. **Combine features:**
   ```bash
   python data/scripts/create_combined_features.py
   ```
3. **Train the VAE:**
   ```bash
   python deep-learning/train_vae.py
   ```
4. **Generate new layouts:**
   ```bash
   python deep-learning/generate_layouts.py
   ```

---

## Data Pipeline
- **Raw data:** Place in `data/raw/`
- **Processing scripts:** In `data/scripts/`
- **Processed data:** Output to `data/processed/`
- **Aggregated user events:** `aggregate_user_events.py` → `aggregated_user_events.csv`
- **Combined features:** `create_combined_features.py` → `vae_combined_features.csv`

---

## Troubleshooting
- **Model shape mismatch:** Ensure `input_dim` in all scripts matches the number of columns in `vae_combined_features.csv`.
- **Port conflicts:** Make sure backend (default: 5000) and frontend (default: 3000) are not in use by other apps.
- **CORS errors:** The backend should have CORS enabled for frontend requests.
- **Data not updating:** Rerun data processing and retrain the model after changing any data.
- **Old model errors:** Delete all `vae_trained.pth` files before retraining if you change the feature size.

---

## Contributing
1. Fork the repo and create your branch (`git checkout -b feature/your-feature`)
2. Commit your changes (`git commit -am 'Add new feature'`)
3. Push to the branch (`git push origin feature/your-feature`)
4. Create a new Pull Request

---

## License
Specify your license here (MIT, Apache, etc.)

---

## Contact
For questions or support, open an issue or contact the maintainer.

---

## New User: Full Setup from Scratch

Follow these steps if you are setting up this project on a new machine for the first time:

### 1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd personalized-layouts
```

### 2. **Install Python and Node.js**
- Make sure you have Python 3.8+ and Node.js 16+ installed.
- [Download Python](https://www.python.org/downloads/)
- [Download Node.js](https://nodejs.org/)

### 3. **Set Up Python Virtual Environment**
```bash
python -m venv myenv
# On Windows:
myenv\Scripts\activate
# On Mac/Linux:
source myenv/bin/activate
```

### 4. **Install Python Dependencies**
```bash
pip install torch pandas scikit-learn
```

### 5. **Set Up Backend**
```bash
cd backend
npm install
node server.js
```

### 6. **Set Up Frontend**
```bash
cd ../frontend
npm install
npm start
```

### 7. **Process Data and Train Model (Full Pipeline)**
If you want to process data and train the model from scratch:
```bash
# Aggregate user events
python data/scripts/aggregate_user_events.py

# Combine all features for model input
python data/scripts/create_combined_features.py

# Train the VAE model
python deep-learning/train_vae.py

# Generate layouts for the frontend
python deep-learning/generate_layouts.py
```

### 8. **(Optional) Troubleshooting Commands**
- **Delete old model checkpoints:**
  ```bash
  del deep-learning\models\vae_trained.pth
  ```
- **Check training data shape:**
  (Already printed by train_vae.py)
- **Check model path:**
  (Already printed by train_vae.py and generate_layouts.py)

### 9. **Typical Workflow for Development**
- Start backend: `node backend/server.js`
- Start frontend: `npm start` (in frontend directory)
- (Re)train model and generate layouts as needed

---

**You are now ready to use and develop the Generative Adaptive UI System from scratch!** 