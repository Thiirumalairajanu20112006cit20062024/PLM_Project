# ⚙️ Digital Twin-Enabled AI Framework for Predictive Maintenance and Product Lifecycle Optimization of Heavy Equipment Engine Components

---

## 📌 Project Information

- **Course:** ME4506 – Product Lifecycle Management (PLM)
- **Faculty Mentor:** Dhanesh Babu
- **Team Members:** Thirumalairajan U & Tharunkumar RP
- **Project Location:** `C:\Users\thiru\.gemini\antigravity\scratch\PLM_Project`

---

## 📄 Abstract

Heavy equipment engines operate under extreme conditions involving high mechanical loads, continuous vibration, and elevated thermal stress, making critical components such as bearings, fuel injectors, and turbochargers highly susceptible to gradual degradation and unexpected failure. Conventional maintenance strategies — whether reactive (repair after failure) or preventive (fixed-schedule servicing) — are both inefficient and costly, often resulting in either unnecessary downtime or premature component replacement. 

This project proposes a **Digital Twin-Enabled Artificial Intelligence Framework** that addresses these limitations by integrating machine learning-based predictive maintenance with Product Lifecycle Management (PLM) decision logic. The proposed framework operates on real-time sensor data — including temperature, RPM, oil pressure, vibration amplitude, load condition, and cumulative operating hours — collected or simulated for a selected engine component. 

This data is preprocessed using Python and fed into two parallel machine learning models: a **Random Forest classifier** that categorizes component health into three states (**Healthy**, **Warning**, and **Failure Risk**), and a **regression model** that estimates the **Remaining Useful Life (RUL)** of the component in hours. The outputs of these models are visualized through a digital twin dashboard, which mirrors the virtual condition of the physical component in real time and displays health status trends, failure probability, and maintenance alerts. The AI predictions are directly integrated into a PLM decision layer that spans the operation, maintenance, and end-of-life stages of the component lifecycle. Based on the predicted health status and RUL, the system recommends one of three lifecycle actions: **continue operation (Healthy)**, **schedule maintenance (Warning)**, or **initiate replacement planning (Failure Risk)**. This closes the gap between sensor-level data and actionable lifecycle decisions, shifting maintenance strategy from reactive or schedule-based to fully predictive and data-driven.

---

## 🏷️ Keywords

`Digital Twin`, `Predictive Maintenance`, `Machine Learning`, `Product Lifecycle Management`, `Remaining Useful Life`, `Random Forest`, `Heavy Equipment`, `Sensor Data`, `Health Monitoring`.

---

## 🎯 Key Objectives

1. **Build a synthetic/real sensor dataset** reflecting realistic engine component degradation patterns.
2. **Train an AI classification model** for health status prediction and a **regression model** for RUL estimation.
3. **Develop a digital twin dashboard** to visualize component health, trends, and failure probability.
4. **Integrate AI outputs into a PLM decision layer** to recommend operate, maintain, or replace actions.

---

## 📊 Dataset Specifications

The dataset `sensor_data.csv` consists of 1,200 operational data points representing heavy equipment engine sensor readings:

| Column Name | Feature Type | Unit / Range | Description |
| :--- | :--- | :--- | :--- |
| `hours_operated` | Numerical | 50.0 – 10,000.0 hrs | Total cumulative engine operational hours |
| `temperature` | Numerical | 40.0 – 150.0 °C | Engine coolant / oil temperature |
| `vibration` | Numerical | 0.0 – 25.0 mm/s | Crankshaft / bearing vibration velocity |
| `oil_pressure` | Numerical | 10.0 – 75.0 PSI | Lubrication system pressure |
| `rpm` | Numerical | 500 – 3000 RPM | Engine rotational speed |
| `load` | Numerical | 0.0 – 100.0 % | Operational engine load percentage |
| `health_label` | Categorical | Healthy / Warning / Failure | Target variable for classification |
| `RUL` | Numerical | 0.0 – 1,500.0 hrs | Target variable for regression (Remaining Useful Life) |

---

## ⚙️ Machine Learning Evaluation Results

### 1. Classification Model (`RandomForestClassifier`)
- **Target:** Classify engine state into `Healthy`, `Warning`, or `Failure`.
- **Accuracy:** **96.67%**
- **Precision:** **96.71%**
- **Recall:** **96.67%**
- **F1 Score:** **96.68%**

```text
Confusion Matrix:
         Failure  Healthy  Warning
Failure       67        0        3
Healthy        0       68        2
Warning        3        0       97
```

### 2. Regression Model (`RandomForestRegressor`)
- **Target:** Estimate Remaining Useful Life (RUL) in hours.
- **Mean Absolute Error (MAE):** **42.40 hours**
- **Root Mean Squared Error (RMSE):** **54.80 hours**
- **R² Score:** **0.9717** (97.17% of RUL variance explained)

---

## 💻 Streamlit Dashboard & Digital Twin Features (`app.py`)

1. **Digital Twin Telemetry Panel:** Live health status badge, confidence percentage, RUL gauge indicator, and ISO 10816 vibration severity class.
2. **Subsystem CAD Wear Monitors:** Real-time stress scores for Thermal Stress, Journal Bearing Wear, Oil Pressure Index, and Piston Duty Fatigue.
3. **Interactive Simulation Controls:** Sliders for operational parameters & pre-configured simulation stress scenarios.
4. **PLM Financial ROI Optimizer:** Calculates immediate maintenance cost vs catastrophic failure penalty and net financial PLM ROI.
5. **Generative AI Copilot & XAI:** Feature importance horizontal bar chart, automated root-cause failure analysis (RCFA), and interactive engineering Q&A chatbot.
6. **Executive Report Export:** Downloadable executive CSV/PDF report.

---

## 🚀 Execution Commands

```bash
# Step 1: Navigate to project directory
cd C:\Users\thiru\.gemini\antigravity\scratch\PLM_Project

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Train machine learning models
python train_model.py

# Step 4: Launch Streamlit Digital Twin Dashboard
streamlit run app.py
```
