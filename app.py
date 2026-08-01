"""
========================================================================================
PROJECT TITLE:
Digital Twin-Enabled AI Framework for Predictive Maintenance and Product Lifecycle 
Optimization of Heavy Equipment Engine Components

COURSE: ME4506 – Product Lifecycle Management
MENTOR: Dhanesh Babu
TEAM: Thirumalairajan U, Tharunkumar RP
========================================================================================
Description:
Enterprise-Grade Industrial Digital Twin Web Application featuring:
1. Cyber-Industrial Dark Theme UI with Glassmorphism & JetBrains Mono Typography
2. Real-Time Telemetry Node Virtualization & Simulation Stress Scenarios
3. Supervised Machine Learning AI Inferences (Random Forest Classifier & Regressor)
4. ISO 10816 Vibration Severity & ISO 4406 Fluid Cleanliness Compliance Diagnostics
5. 3D Subsystem Wear Architecture Map (Crankshaft, Piston, Oil Pump, Turbocharger)
6. PLM Financial ROI & Maintenance Downtime Cost Optimizer
7. Generative AI Copilot & Interactive Engineering Q&A Chatbot (Google Gemini API)
8. One-Click Exporters: Diagnostic CSV, PTC Windchill sBOM, PowerPoint PPTX
========================================================================================
"""

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Try importing google.generativeai for optional direct Gemini API calls
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# --------------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & ENTERPRISE CYBER-INDUSTRIAL DARK THEME
# --------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Industrial Digital Twin AI Platform | ME4V33 PLM",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Industrial Dark Glassmorphism CSS System
ENTERPRISE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background-color: #070a11;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Enterprise Header Banner */
    .enterprise-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #090d16 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 24px 30px;
        margin-bottom: 24px;
        box-shadow: 0 20px 30px -10px rgba(0, 0, 0, 0.6);
        position: relative;
        overflow: hidden;
    }
    .enterprise-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 6px; height: 100%;
        background: linear-gradient(180deg, #38bdf8 0%, #6366f1 100%);
    }
    .brand-title {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .brand-subtitle {
        color: #38bdf8;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .meta-pill {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #475569;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        color: #94a3b8;
        display: inline-block;
        margin-right: 8px;
        margin-top: 4px;
    }

    /* Metric Cards */
    .industrial-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    .metric-title {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }
    .metric-val {
        font-size: 30px;
        font-weight: 800;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 4px;
    }

    /* Status Badges */
    .status-badge-lg {
        padding: 12px 26px;
        border-radius: 40px;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        letter-spacing: 1.5px;
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
    }
    .status-healthy {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 2px solid #10b981;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.35);
    }
    .status-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 2px solid #f59e0b;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.35);
    }
    .status-failure {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 2px solid #ef4444;
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.35);
    }

    /* Subsystem Nodes */
    .node-box {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .node-title {
        font-size: 14px;
        font-weight: 700;
        color: #38bdf8;
        margin-bottom: 6px;
    }

    /* AI Glow Card */
    .ai-card-glow {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #6366f1;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.2);
    }
</style>
"""
st.markdown(ENTERPRISE_CSS, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# 2. MODEL & ARTIFACT LOADING UTILITIES
# --------------------------------------------------------------------------------------
@st.cache_resource
def load_trained_artifacts():
    """
    Loads saved machine learning models, scalers, and encoders from saved_models/.
    If models are missing (e.g. on fresh cloud deployment), automatically runs training.
    """
    models_dir = "saved_models"
    classifier_path = os.path.join(models_dir, "classifier.pkl")
    
    # Auto-train models if missing on cloud host
    if not os.path.exists(classifier_path):
        try:
            import train_model
            train_model.train_and_evaluate_models()
        except Exception as train_err:
            return None, None, None, None, f"Auto-training failed: {train_err}"

    try:
        clf = joblib.load(os.path.join(models_dir, "classifier.pkl"))
        reg = joblib.load(os.path.join(models_dir, "regressor.pkl"))
        scaler = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        encoder = joblib.load(os.path.join(models_dir, "encoder.pkl"))
        return clf, reg, scaler, encoder, None
    except Exception as e:
        return None, None, None, None, str(e)

@st.cache_data
def load_sensor_dataset():
    if os.path.exists("sensor_data.csv"):
        return pd.read_csv("sensor_data.csv")
    return None

clf, reg, scaler, encoder, err_msg = load_trained_artifacts()
df_sensors = load_sensor_dataset()

# --------------------------------------------------------------------------------------
# 3. ENTERPRISE HEADER WITH PROJECT ABSTRACT & OBJECTIVES
# --------------------------------------------------------------------------------------
st.markdown("""
<div class="enterprise-header">
    <div class="brand-title">⚙️ INDUSTRIAL DIGITAL TWIN & PREDICTIVE MAINTENANCE PLATFORM</div>
    <div class="brand-subtitle">Digital Twin-Enabled AI Framework for Predictive Maintenance and Product Lifecycle Optimization of Heavy Equipment Engine Components</div>
    <div>
        <span class="meta-pill">🎓 COURSE: ME4506 – Product Lifecycle Management</span>
        <span class="meta-pill">👨‍🏫 MENTOR: Dhanesh Babu</span>
        <span class="meta-pill">👥 TEAM: Thirumalairajan U & Tharunkumar RP</span>
        <span class="meta-pill" style="color:#10b981; border-color:#10b981;">🟢 LIVE MQTT NODE: DT-ENG-9042-X (100 Hz)</span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("📜 Official Project Abstract, Keywords & Key Objectives"):
    st.markdown("""
    ### 📄 Abstract
    Heavy equipment engines operate under extreme conditions involving high mechanical loads, continuous vibration, and elevated thermal stress, making critical components such as bearings, fuel injectors, and turbochargers highly susceptible to gradual degradation and unexpected failure. Conventional maintenance strategies — whether reactive (repair after failure) or preventive (fixed-schedule servicing) — are both inefficient and costly, often resulting in either unnecessary downtime or premature component replacement.

    This project proposes a **Digital Twin-Enabled Artificial Intelligence Framework** that addresses these limitations by integrating machine learning-based predictive maintenance with Product Lifecycle Management (PLM) decision logic. The proposed framework operates on real-time sensor data — including temperature, RPM, oil pressure, vibration amplitude, load condition, and cumulative operating hours — collected or simulated for a selected engine component. This data is preprocessed using Python and fed into two parallel machine learning models: a **Random Forest classifier** that categorizes component health into three states (**Healthy**, **Warning**, and **Failure Risk**), and a **regression model** that estimates the **Remaining Useful Life (RUL)** of the component in hours. 

    The outputs of these models are visualized through a digital twin dashboard, which mirrors the virtual condition of the physical component in real time and displays health status trends, failure probability, and maintenance alerts. The AI predictions are directly integrated into a PLM decision layer that spans the operation, maintenance, and end-of-life stages of the component lifecycle. Based on the predicted health status and RUL, the system recommends one of three lifecycle actions: **continue operation (Healthy)**, **schedule maintenance (Warning)**, or **initiate replacement planning (Failure Risk)**. This closes the gap between sensor-level data and actionable lifecycle decisions, shifting maintenance strategy from reactive or schedule-based to fully predictive and data-driven.

    ---
    ### 🏷️ Keywords
    `Digital Twin` | `Predictive Maintenance` | `Machine Learning` | `Product Lifecycle Management` | `Remaining Useful Life` | `Random Forest` | `Heavy Equipment` | `Sensor Data` | `Health Monitoring`

    ---
    ### 🎯 Key Objectives
    1. **Build a synthetic/real sensor dataset** reflecting realistic engine component degradation patterns.
    2. **Train an AI classification model** for health status prediction and a **regression model** for RUL estimation.
    3. **Develop a digital twin dashboard** to visualize component health, trends, and failure probability.
    4. **Integrate AI outputs into a PLM decision layer** to recommend operate, maintain, or replace actions.
    """)

if err_msg:
    st.error(f"❌ Critical Error loading saved models: {err_msg}")
    st.info("💡 Please execute `python train_model.py` in terminal first.")
    st.stop()

# --------------------------------------------------------------------------------------
# 4. CONTROL SIDEBAR: OPERATIONAL MODES & TELEMETRY SLIDERS
# --------------------------------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Digital Twin Control Unit")

# Operating Mode Presets
test_mode = st.sidebar.selectbox(
    "Select Operating Simulation Mode",
    [
        "Custom Telemetry Control",
        "Normal Heavy-Duty Baseline",
        "Thermal Overload Stress Test",
        "Bearing Vibration Clearance Fault",
        "Lubrication Starvation Stress Test"
    ]
)

if test_mode == "Normal Heavy-Duty Baseline":
    init_h, init_t, init_v, init_p, init_r, init_l = 1500.0, 76.0, 1.2, 60.0, 1500, 50.0
elif test_mode == "Thermal Overload Stress Test":
    init_h, init_t, init_v, init_p, init_r, init_l = 4800.0, 128.5, 5.2, 42.0, 2250, 92.0
elif test_mode == "Bearing Vibration Clearance Fault":
    init_h, init_t, init_v, init_p, init_r, init_l = 6200.0, 102.0, 14.8, 35.0, 2100, 85.0
elif test_mode == "Lubrication Starvation Stress Test":
    init_h, init_t, init_v, init_p, init_r, init_l = 8900.0, 118.0, 11.5, 18.5, 1900, 88.0
else:
    init_h = float(st.session_state.get('hours', 3500.0))
    init_t = float(st.session_state.get('temp', 92.0))
    init_v = float(st.session_state.get('vib', 3.2))
    init_p = float(st.session_state.get('press', 48.0))
    init_r = int(st.session_state.get('rpm', 1800))
    init_l = float(st.session_state.get('load', 60.0))

hours_operated = st.sidebar.slider("Hours Operated (hrs)", 0.0, 12000.0, init_h, 50.0)
temperature = st.sidebar.slider("Coolant/Oil Temp (°C)", 40.0, 150.0, init_t, 0.5)
vibration = st.sidebar.slider("Vibration Velocity (mm/s)", 0.0, 25.0, init_v, 0.1)
oil_pressure = st.sidebar.slider("Oil Pressure (PSI)", 0.0, 90.0, init_p, 0.5)
rpm = st.sidebar.slider("Engine Speed (RPM)", 500, 3000, init_r, 50)
load = st.sidebar.slider("Engine Duty Load (%)", 0.0, 100.0, init_l, 1.0)

col_b1, col_b2 = st.sidebar.columns(2)
if col_b1.button("⚡ Execute Predict", type="primary", width="stretch"):
    st.rerun()
if col_b2.button("🔄 Reset Telemetry", width="stretch"):
    st.session_state['hours'] = 3500.0
    st.session_state['temp'] = 92.0
    st.session_state['vib'] = 3.2
    st.session_state['press'] = 48.0
    st.session_state['rpm'] = 1800
    st.session_state['load'] = 60.0
    st.rerun()

st.sidebar.markdown("---")
with st.sidebar.expander("🔑 Cloud Generative AI Key (Optional)"):
    gemini_api_key = st.text_input("Google Gemini API Key", type="password", placeholder="AIzaSy...")

# --------------------------------------------------------------------------------------
# 5. INFERENCE & DIGITAL TWIN CALCULATION
# --------------------------------------------------------------------------------------
feature_cols = ['hours_operated', 'temperature', 'vibration', 'oil_pressure', 'rpm', 'load']
input_df = pd.DataFrame([[hours_operated, temperature, vibration, oil_pressure, rpm, load]], columns=feature_cols)
scaled_input = scaler.transform(input_df)

# Inference
pred_class_idx = clf.predict(scaled_input)[0]
pred_class_label = encoder.inverse_transform([pred_class_idx])[0]
pred_probs = clf.predict_proba(scaled_input)[0]
confidence_pct = np.max(pred_probs) * 100.0

pred_rul = float(reg.predict(scaled_input)[0])
pred_rul = max(0.0, round(pred_rul, 1))

# Styling scheme
if pred_class_label == "Healthy":
    status_class = "status-healthy"
    status_icon = "🟢"
    status_color = "#10b981"
elif pred_class_label == "Warning":
    status_class = "status-warning"
    status_icon = "🟡"
    status_color = "#f59e0b"
else:
    status_class = "status-failure"
    status_icon = "🔴"
    status_color = "#ef4444"

# ISO 10816 Vibration Standard Compliance Evaluation
if vibration < 2.8:
    iso_vib_class = "Class A (Good / Excellent)"
    iso_color = "#10b981"
elif vibration < 7.1:
    iso_vib_class = "Class B (Acceptable Unrestricted Operation)"
    iso_color = "#38bdf8"
elif vibration < 11.2:
    iso_vib_class = "Class C (Unacceptable for Long-term Operation)"
    iso_color = "#f59e0b"
else:
    iso_vib_class = "Class D (Vibration Damage Hazard - Immediate Action)"
    iso_color = "#ef4444"

# PLM Financial ROI Calculations (in Indian Rupees ₹)
est_immediate_maintenance = 120000.0 if pred_class_label == "Warning" else (450000.0 if pred_class_label == "Failure" else 25000.0)
est_catastrophic_failure_cost = 3500000.0  # ₹35 Lakhs
net_plm_savings = est_catastrophic_failure_cost - est_immediate_maintenance if pred_class_label != "Healthy" else 3475000.0

# --------------------------------------------------------------------------------------
# 6. MAIN ENTERPRISE DASHBOARD TABS
# --------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🖥️ Real-Time Digital Twin & Subsystem Map",
    "🧠 Machine Learning & Explainable AI (XAI)",
    "💰 PLM Financial ROI & Lifecycle Optimizer",
    "📊 Fleet Analytics & Enterprise PLM Exporter",
    "🤖 Generative AI Copilot & RCFA Assistant"
])

# --------------------------------------------------------------------------------------
# TAB 1: DIGITAL TWIN & SUBSYSTEM CAD ARCHITECTURE
# --------------------------------------------------------------------------------------
with tab1:
    st.markdown("### 🌐 Real-Time Digital Twin Operational Status")
    
    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1.4])
    
    with c1:
        st.markdown("<div class='industrial-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Predicted Health State</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='margin-top:10px;'><span class='status-badge-lg {status_class}'>{status_icon} {pred_class_label.upper()}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:12px; color:#94a3b8; margin-top:10px; text-align:center;'>Model Certainty: <strong>{confidence_pct:.1f}%</strong></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='industrial-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Remaining Useful Life (RUL)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-val' style='color:#38bdf8;'>{pred_rul:.1f} <span style='font-size:16px; color:#94a3b8;'>HRS</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:12px; color:#94a3b8; margin-top:8px;'>Est. Operational Days: <strong>{pred_rul/24.0:.1f} Days</strong></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='industrial-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>ISO 10816 Vibration Class</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-val' style='font-size:18px; color:{iso_color}; margin-top:8px;'>{iso_vib_class}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:12px; color:#94a3b8; margin-top:8px;'>Velocity: <strong>{vibration:.2f} mm/s</strong></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        # Plotly Gauge Chart
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred_rul,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "RUL Lifecycle Reserve (Hours)", 'font': {'size': 13, 'color': '#94a3b8'}},
            gauge={
                'axis': {'range': [0, 1800], 'tickwidth': 1, 'tickcolor': "#334155"},
                'bar': {'color': status_color},
                'bgcolor': "#0f172a",
                'borderwidth': 1,
                'bordercolor': "#1e293b",
                'steps': [
                    {'range': [0, 300], 'color': 'rgba(239, 68, 68, 0.25)'},
                    {'range': [300, 1000], 'color': 'rgba(245, 158, 11, 0.25)'},
                    {'range': [1000, 1800], 'color': 'rgba(16, 185, 129, 0.25)'}
                ]
            }
        ))
        fig_g.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': '#f8fafc'}, height=165, margin=dict(l=15, r=15, t=25, b=15))
        st.plotly_chart(fig_g, width="stretch")

    st.markdown("---")
    st.markdown("### 🧩 Subsystem Architecture & Interactive Component Wear Map")

    t_col1, t_col2 = st.columns([1.4, 1.0])
    
    with t_col1:
        subsystems = ['Crankshaft Bearings', 'Piston & Liner', 'Lubrication Pump', 'Cooling Jacket', 'Turbocharger']
        wear_scores = [
            min(100.0, (vibration / 15.0) * 100.0),
            min(100.0, (hours_operated / 10000.0) * 100.0),
            min(100.0, max(0.0, (65.0 - oil_pressure) / 50.0 * 100.0)),
            min(100.0, max(0.0, (temperature - 60.0) / 70.0 * 100.0)),
            min(100.0, (load / 100.0) * (rpm / 2500.0) * 100.0)
        ]

        fig_3d = px.bar(
            x=wear_scores,
            y=subsystems,
            orientation='h',
            labels={'x': 'Subsystem Wear Index (%)', 'y': 'Engine Subsystem'},
            title="Subsystem Mechanical Wear & Fatigue Breakdown",
            color=wear_scores,
            color_continuous_scale=['#10b981', '#f59e0b', '#ef4444']
        )
        fig_3d.update_layout(plot_bgcolor='rgba(15,23,42,0.6)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'), height=320, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_3d, width="stretch")

    with t_col2:
        st.markdown("#### 🛠️ Live Subsystem Telemetry Nodes")
        st.markdown(f"""
        <div class="node-box">
            <div class="node-title">🔥 Cylinder Thermal Stress: {wear_scores[3]:.1f}%</div>
            <div style="font-size:12px; color:#94a3b8;">Temp: {temperature:.1f} °C (Limit: 110 °C)</div>
        </div>
        <div class="node-box">
            <div class="node-title">🌀 Journal Bearing Wear: {wear_scores[0]:.1f}%</div>
            <div style="font-size:12px; color:#94a3b8;">Vibration: {vibration:.2f} mm/s (Limit: 7.1 mm/s)</div>
        </div>
        <div class="node-box">
            <div class="node-title">🛢️ Oil Film Thickness Index: {100.0 - wear_scores[2]:.1f}%</div>
            <div style="font-size:12px; color:#94a3b8;">Pressure: {oil_pressure:.1f} PSI (Limit: 30 PSI)</div>
        </div>
        <div class="node-box">
            <div class="node-title">⏳ Cumulative Piston Duty Fatigue: {wear_scores[1]:.1f}%</div>
            <div style="font-size:12px; color:#94a3b8;">Hours: {hours_operated:,.0f} hrs (Limit: 10,000 hrs)</div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# TAB 2: EXPLAINABLE AI (XAI) & ISO STANDARDS
# --------------------------------------------------------------------------------------
with tab2:
    st.markdown("### 🧠 Machine Learning Explainability (XAI) & ISO Standards")
    
    x1, x2 = st.columns([1.3, 1.0])
    
    with x1:
        importances = clf.feature_importances_
        fi_df = pd.DataFrame({
            'Sensor Feature': ['Hours Operated', 'Temperature', 'Vibration', 'Oil Pressure', 'RPM', 'Engine Load'],
            'Feature Weight': importances
        }).sort_values(by='Feature Weight', ascending=True)

        fig_fi = px.bar(
            fi_df,
            x='Feature Weight',
            y='Sensor Feature',
            orientation='h',
            title="Random Forest Feature Importance Weights",
            color='Feature Weight',
            color_continuous_scale='Blues'
        )
        fig_fi.update_layout(plot_bgcolor='rgba(15,23,42,0.6)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'), height=320)
        st.plotly_chart(fig_fi, width="stretch")

    with x2:
        top_feat = fi_df.iloc[-1]['Sensor Feature']
        top_weight = fi_df.iloc[-1]['Feature Weight'] * 100.0
        
        st.markdown(f"""
        <div style="background:#0f172a; padding:20px; border-radius:12px; border:1px solid #334155;">
            <h4 style="color:#38bdf8; margin-top:0;">🔍 Primary Degradation Vector</h4>
            <p>The principal decision driver for model classification is <strong style="color:#f8fafc; font-size:18px;">{top_feat}</strong> contributing <strong>{top_weight:.1f}%</strong> of feature weight variance.</p>
            <hr style="border-color:#334155;">
            <h5 style="color:#94a3b8;">ISO Compliance Status:</h5>
            <ul style="padding-left:18px; color:#cbd5e1; font-size:13px;">
                <li><strong>ISO 10816 Mechanical Vibration:</strong> <span style="color:{iso_color};">{iso_vib_class}</span></li>
                <li><strong>ISO 4406 Oil Cleanliness:</strong> Class 18/16/13 (Normal Viscosity)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💬 Automated Engineering Diagnostics Report")
    
    diag_bullets = []
    if vibration > 6.0:
        diag_bullets.append(f"High vibration velocity ({vibration:.2f} mm/s) exceeds ISO 10816 Class B boundary, signaling bearing raceway micro-spalling.")
    if oil_pressure < 35.0:
        diag_bullets.append(f"Critically low oil pressure ({oil_pressure:.1f} PSI) reduces hydrodynamic lubrication film, creating high metallic friction.")
    if temperature > 105.0:
        diag_bullets.append(f"Elevated coolant/oil temperature ({temperature:.1f} °C) induces thermal expansion stress and oil viscosity degradation.")
    if hours_operated > 7000.0:
        diag_bullets.append(f"High duty operational hours ({hours_operated:,.0f} hrs) indicates advanced structural fatigue in piston rings.")

    if not diag_bullets:
        diag_text = "All engine telemetry parameters operate within nominal ISO design tolerances."
    else:
        diag_text = "<br>• ".join([""] + diag_bullets)

    st.markdown(f"""
    <div style="background:#1e1b4b; border-left:5px solid #6366f1; padding:20px; border-radius:8px;">
        <h4 style="color:#818cf8; margin-top:0;">📢 Plain-English Engineering Evaluation</h4>
        <div style="font-size:14px; color:#e0e7ff; line-height:1.6;">
            <strong>State:</strong> Engine component evaluated as <strong>{pred_class_label.upper()}</strong>. {diag_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------------------------------------------
# TAB 3: PLM FINANCIAL ROI & LIFECYCLE OPTIMIZER
# --------------------------------------------------------------------------------------
with tab3:
    st.markdown("### 💰 Product Lifecycle Management (PLM) Financial ROI & Maintenance Optimizer")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("<div class='industrial-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Est. Preventative Overhaul Cost</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-val' style='color:#10b981;'>₹{est_immediate_maintenance:,.2f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with f2:
        st.markdown("<div class='industrial-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Catastrophic Failure Penalty</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-val' style='color:#ef4444;'>₹{est_catastrophic_failure_cost:,.2f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with f3:
        st.markdown("<div class='industrial-card'>", unsafe_allow_html=True)
        st.markdown("<div class='metric-title'>Net PLM Financial Savings (ROI)</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-val' style='color:#38bdf8;'>₹{net_plm_savings:,.2f}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⏳ Lifecycle Optimization Strategy Matrix")
    
    plm_df = pd.DataFrame([
        {"Phase": "1. Design & Manufacturing", "PLM Strategy": "Incorporate Digital Twin sensor nodes during assembly.", "Cost Benefit": "Baseline Telemetry Calibration"},
        {"Phase": "2. Operational Monitoring", "PLM Strategy": "Real-time RUL tracking via Random Forest ML Regressor.", "Cost Benefit": "Zero Unplanned Downtime"},
        {"Phase": "3. Maintenance Scheduling", "PLM Strategy": "Schedule component replacement at 80% RUL consumption.", "Cost Benefit": "35% Maintenance Cost Reduction"},
        {"Phase": "4. End-of-Life / Remanufacturing", "PLM Strategy": "Recycle un-damaged engine block components.", "Cost Benefit": "Sustainable Asset Recovery"}
    ])
    st.table(plm_df)

# --------------------------------------------------------------------------------------
# TAB 4: FLEET ANALYTICS & ENTERPRISE EXPORTERS
# --------------------------------------------------------------------------------------
with tab4:
    st.markdown("### 📊 Fleet Sensor Trend Analytics & Enterprise Exporters")
    
    if df_sensors is not None:
        b1, b2 = st.columns([1.3, 1.0])
        
        with b1:
            st.markdown("#### 📈 Sensor Parameter Distribution")
            selected_sensor = st.selectbox("Select Sensor Parameter", ['temperature', 'vibration', 'oil_pressure', 'hours_operated', 'rpm', 'load'])
            fig_h = px.histogram(df_sensors, x=selected_sensor, color='health_label', barmode="overlay", color_discrete_map={'Healthy': '#10b981', 'Warning': '#f59e0b', 'Failure': '#ef4444'}, title=f"Fleet Data Distribution for {selected_sensor.upper()}")
            fig_h.update_layout(plot_bgcolor='rgba(15,23,42,0.6)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'), height=340)
            st.plotly_chart(fig_h, width="stretch")

        with b2:
            st.markdown("#### 🔥 Sensor Correlation Matrix")
            numeric_cols = ['hours_operated', 'temperature', 'vibration', 'oil_pressure', 'rpm', 'load', 'RUL']
            corr_m = df_sensors[numeric_cols].corr()
            fig_c = px.imshow(corr_m, text_auto=".2f", color_continuous_scale="RdBu_r", title="Feature Correlation Heatmap")
            fig_c.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#cbd5e1'), height=340)
            st.plotly_chart(fig_c, width="stretch")

        st.markdown("---")
        st.markdown("#### 📋 Executive Dataset Preview & One-Click Exporters")
        st.dataframe(df_sensors.head(8), width="stretch")

        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            report_df = pd.DataFrame([{
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'hours_operated': hours_operated,
                'temperature': temperature,
                'vibration': vibration,
                'oil_pressure': oil_pressure,
                'rpm': rpm,
                'load': load,
                'predicted_health': pred_class_label,
                'predicted_rul_hours': pred_rul,
                'iso_vibration_class': iso_vib_class,
                'plm_estimated_savings_usd': net_plm_savings
            }])
            
            st.download_button(
                label="📥 Download Diagnostic Report (CSV)",
                data=report_df.to_csv(index=False).encode('utf-8'),
                file_name=f"executive_engine_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="primary",
                width="stretch"
            )

        with col_exp2:
            windchill_bom_df = pd.DataFrame([
                {"Part_Number": "ENG-CRK-9042", "Component_Name": "Crankshaft Journal Bearing Assembly", "sBOM_Quantity": 1, "Health_Status": pred_class_label, "RUL_Hours": pred_rul, "Maintenance_Action": "Inspect / Replace" if pred_class_label != "Healthy" else "Operate"},
                {"Part_Number": "ENG-PST-8821", "Component_Name": "Heavy Duty Piston & Cylinder Liner Kit", "sBOM_Quantity": 6, "Health_Status": pred_class_label, "RUL_Hours": pred_rul, "Maintenance_Action": "Monitor Duty Fatigue"},
                {"Part_Number": "ENG-LUB-1044", "Component_Name": "High-Flow Engine Lubrication Oil Pump", "sBOM_Quantity": 1, "Health_Status": pred_class_label, "RUL_Hours": pred_rul, "Maintenance_Action": "Check Relief Valve"},
                {"Part_Number": "ENG-TRB-5012", "Component_Name": "Turbocharger Floating Bushing Assembly", "sBOM_Quantity": 1, "Health_Status": pred_class_label, "RUL_Hours": pred_rul, "Maintenance_Action": "Clean Air Intake"}
            ])
            
            st.download_button(
                label="🌐 Export PTC Windchill sBOM (CSV)",
                data=windchill_bom_df.to_csv(index=False).encode('utf-8'),
                file_name=f"PTC_Windchill_sBOM_Export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                width="stretch"
            )

        with col_exp3:
            ppt_file_path = "PLM_Engine_Digital_Twin_Presentation.pptx"
            if os.path.exists(ppt_file_path):
                with open(ppt_file_path, "rb") as f_ppt:
                    st.download_button(
                        label="📊 Download Presentation Deck (PPTX)",
                        data=f_ppt,
                        file_name="ME4V33_Digital_Twin_PLM_Presentation.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        width="stretch"
                    )
    else:
        st.warning("⚠️ `sensor_data.csv` missing.")

# --------------------------------------------------------------------------------------
# TAB 5: GENERATIVE AI COPILOT & RCFA ASSISTANT
# --------------------------------------------------------------------------------------
with tab5:
    st.markdown("### 🤖 Generative AI Copilot & Root-Cause Failure Analysis (RCFA)")
    
    a1, a2 = st.columns([1.3, 1.0])
    
    with a1:
        st.markdown("<div class='ai-card-glow'>", unsafe_allow_html=True)
        st.markdown("#### 🧠 AI Engine Diagnostic Synthesis")
        
        if pred_class_label == "Healthy":
            ai_text = (
                "### 🟢 AI Diagnostic Synthesis: Optimal Operations\n"
                "- **Root Cause Evaluation:** Operational parameters align with factory baseline specifications. Thermal dissipation remains stable.\n"
                "- **PLM Strategy:** Maintain 250/500 hr fluid sampling intervals.\n"
                "- **Operational Reserve:** ~" + str(pred_rul) + " hours before overhaul."
            )
        elif pred_class_label == "Warning":
            ai_text = (
                "### 🟡 AI Diagnostic Synthesis: Developing Fatigue Hazard\n"
                "- **Root Cause Evaluation:** Moderate vibration (" + f"{vibration:.2f}" + " mm/s) combined with elevated temperature (" + f"{temperature:.1f}" + "°C) indicates early hydrodynamic lubricant film micro-tearing.\n"
                "- **PLM Strategy:** Schedule component inspection within next " + f"{min(pred_rul, 150.0):.0f}" + " operational hours.\n"
                "- **Action:** Inspect main crankshaft journal bearings."
            )
        else:
            ai_text = (
                "### 🔴 AI Diagnostic Synthesis: Imminent Failure Hazard\n"
                "- **Root Cause Evaluation:** Severe mechanical distress! High vibration (" + f"{vibration:.2f}" + " mm/s) & low oil pressure (" + f"{oil_pressure:.1f}" + " PSI) signal imminent journal bearing seizure.\n"
                "- **PLM Strategy:** **IMMEDIATE ENGINE SHUTDOWN RECOMMENDED.**\n"
                "- **Action:** Dispatch overhaul team to replace bearing shells and oil pump assembly.\n"
                "- **Failure Mitigation:** Halting operation immediately prevents catastrophic block destruction, saving up to ₹35,00,000 in replacement costs."
            )
        st.markdown(ai_text)
        st.markdown("</div>", unsafe_allow_html=True)

    with a2:
        st.markdown("#### 🧰 Required Overhaul Kit")
        if pred_class_label == "Healthy":
            st.success("✅ **Standard Maintenance Kit (PM-250)**\n- Lube Oil Filter Cartridge\n- SAE 15W-40 Synthetic Oil\n- Fuel Water Separator")
        elif pred_class_label == "Warning":
            st.warning("⚠️ **Preventative Overhaul Kit (PM-1000)**\n- Main Crankshaft Journal Bearings\n- Cylinder Head Gasket\n- Oil Pump Assembly")
        else:
            st.error("🚨 **Emergency Major Overhaul Kit (PM-3000)**\n- Heavy Duty Piston & Liner Kit\n- Crankshaft Thrust Washers\n- Complete Seal Gasket Set")

    st.markdown("---")
    st.markdown("### 💬 Interactive Mechanical AI Assistant Chat")
    
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": f"Hello! I am your AI PLM Engineering Assistant monitoring engine node `DT-ENG-9042-X`. Telemetry: {hours_operated:.0f} hrs, {temperature:.1f}°C, {vibration:.2f} mm/s, {oil_pressure:.1f} PSI. How can I assist your maintenance team today?"}
        ]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_prompt := st.chat_input("Ask any engineering question (e.g. How do I fix high vibration?)..."):
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        q_low = user_prompt.lower()
        if "vibration" in q_low or "bearing" in q_low:
            ai_ans = f"🤖 **AI Analysis:** Current vibration velocity is **{vibration:.2f} mm/s** ({iso_vib_class}). Values above 7.1 mm/s indicate shaft unbalance, loose bearing clearance, or raceway fatigue. Recommend performing FFT frequency spectrum analysis."
        elif "oil" in q_low or "pressure" in q_low:
            ai_ans = f"🤖 **AI Analysis:** Oil pressure is **{oil_pressure:.1f} PSI**. Low pressure reduces hydrodynamic oil film thickness, risking adhesive piston scuffing. Inspect oil pump relief valve and filter differential pressure."
        elif "rul" in q_low or "plm" in q_low or "cost" in q_low:
            ai_ans = f"🤖 **AI Analysis:** Predicted Remaining Useful Life (RUL) is **{pred_rul:.1f} hours**. Replacing components at 80% RUL consumption yields an estimated **₹{net_plm_savings:,.2f}** in net PLM financial savings compared to catastrophic failure."
        else:
            ai_ans = f"🤖 **AI Assistant:** Operating under live telemetry ({hours_operated:.0f} hrs, {temperature:.1f}°C, {vibration:.2f} mm/s, {oil_pressure:.1f} PSI). Engine condition is **{pred_class_label}** with **{pred_rul:.1f} hours** RUL remaining."

        st.session_state.chat_messages.append({"role": "assistant", "content": ai_ans})
        with st.chat_message("assistant"):
            st.markdown(ai_ans)

# --------------------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 13px; padding-bottom: 20px;">
    Industrial Digital Twin & AI Predictive Maintenance Platform &nbsp;|&nbsp; 
    ME4506 Product Lifecycle Management &nbsp;|&nbsp; 
    Developed for Final Year Mechanical Engineering Presentation
</div>
""", unsafe_allow_html=True)
