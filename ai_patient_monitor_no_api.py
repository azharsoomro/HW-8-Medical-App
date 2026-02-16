# ==========================================================
# AI-BASED ICU PATIENT MONITOR - NO API VERSION
# Works without Anthropic API - Enhanced Rule-Based Logic
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import json

# Page Configuration
st.set_page_config(
    page_title="ICU Patient Monitor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for medical-grade styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .critical-alert {
        background-color: #dc2626;
        color: white;
        padding: 20px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        animation: blink 1s infinite;
        margin: 20px 0;
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        25%, 75% { opacity: 0.5; }
    }
    .warning-alert {
        background-color: #f59e0b;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        margin: 10px 0;
    }
    .stable-status {
        background-color: #10b981;
        color: white;
        padding: 15px;
        border-radius: 8px;
        font-weight: bold;
        margin: 10px 0;
    }
    .action-card {
        background-color: #fef3c7;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f59e0b;
        margin: 10px 0;
    }
    .assessment-box {
        background-color: #f0f9ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced rule-based clinical assessment
def analyze_patient_vitals(patient_data):
    """Advanced rule-based clinical assessment"""
    latest_vitals = patient_data.iloc[-1]
    trend_data = patient_data.tail(10)
    
    # Calculate trends
    hr_trend = trend_data['heart_rate_bpm'].diff().mean()
    spo2_trend = trend_data['spo2_percent'].diff().mean()
    temp_trend = trend_data['temperature_c'].diff().mean()
    bp_trend = trend_data['bp_systolic_mmHg'].diff().mean()
    
    assessment = []
    severity = "STABLE"
    diagnosis = []
    risk_factors = []
    
    # Analyze heart rate
    hr = latest_vitals['heart_rate_bpm']
    if hr > 150:
        severity = "CRITICAL"
        assessment.append(f"**Severe Tachycardia** ({hr:.0f} bpm): Possible ventricular tachycardia or severe compensatory response.")
        diagnosis.append("Suspected V-Tach or Severe Tachycardia")
        risk_factors.append("Risk of cardiac arrest, hemodynamic collapse")
    elif hr > 120:
        if severity != "CRITICAL":
            severity = "WARNING"
        assessment.append(f"**Tachycardia** ({hr:.0f} bpm): Compensatory response to stress, infection, or hypovolemia.")
        diagnosis.append("Compensatory Tachycardia")
    elif hr < 40:
        severity = "CRITICAL"
        assessment.append(f"**Severe Bradycardia** ({hr:.0f} bpm): Risk of inadequate cardiac output and cardiac arrest.")
        diagnosis.append("Severe Bradycardia")
        risk_factors.append("Immediate risk of cardiac arrest")
    elif hr < 50:
        if severity != "CRITICAL":
            severity = "WARNING"
        assessment.append(f"**Bradycardia** ({hr:.0f} bpm): Monitor closely for further decline.")
    
    # Analyze SpO2
    spo2 = latest_vitals['spo2_percent']
    if spo2 < 85:
        severity = "CRITICAL"
        assessment.append(f"**Severe Hypoxemia** ({spo2:.1f}%): Critical oxygen deficiency requiring immediate intervention.")
        diagnosis.append("Severe Hypoxemia/Respiratory Failure")
        risk_factors.append("Risk of organ damage, respiratory arrest")
    elif spo2 < 90:
        if severity == "STABLE":
            severity = "WARNING"
        assessment.append(f"**Hypoxemia** ({spo2:.1f}%): Below target oxygen saturation.")
        diagnosis.append("Hypoxemia")
    
    if spo2_trend < -0.3:
        assessment.append(f"**Declining SpO2 Trend**: Oxygen saturation dropping {abs(spo2_trend):.2f}% per minute - suggests worsening respiratory function.")
        if "Respiratory Failure" not in " ".join(diagnosis):
            diagnosis.append("Progressive Respiratory Failure")
    
    # Analyze blood pressure
    bp_sys = latest_vitals['bp_systolic_mmHg']
    bp_dia = latest_vitals['bp_diastolic_mmHg']
    if bp_sys < 80:
        severity = "CRITICAL"
        assessment.append(f"**Severe Hypotension** ({bp_sys}/{bp_dia} mmHg): Risk of shock and organ hypoperfusion.")
        diagnosis.append("Hypotensive Shock")
        risk_factors.append("Risk of multi-organ failure")
    elif bp_sys < 90:
        if severity == "STABLE":
            severity = "WARNING"
        assessment.append(f"**Hypotension** ({bp_sys}/{bp_dia} mmHg): Below normal range, monitor perfusion.")
        diagnosis.append("Hypotension")
    elif bp_sys > 180:
        severity = "CRITICAL"
        assessment.append(f"**Hypertensive Crisis** ({bp_sys}/{bp_dia} mmHg): Risk of stroke, heart failure.")
        diagnosis.append("Hypertensive Emergency")
        risk_factors.append("Risk of stroke, myocardial infarction")
    
    # Analyze temperature
    temp = latest_vitals['temperature_c']
    if temp > 39.5:
        if severity == "STABLE":
            severity = "CRITICAL"
        assessment.append(f"**Severe Hyperthermia** ({temp:.1f}°C): High fever suggesting serious infection or inflammation.")
        diagnosis.append("Severe Hyperthermia/Sepsis")
    elif temp > 38.5:
        if severity == "STABLE":
            severity = "WARNING"
        assessment.append(f"**Fever** ({temp:.1f}°C): Elevated temperature, possible infection.")
        diagnosis.append("Fever/Infection")
    elif temp < 35:
        severity = "CRITICAL"
        assessment.append(f"**Hypothermia** ({temp:.1f}°C): Dangerously low body temperature.")
        diagnosis.append("Hypothermia")
        risk_factors.append("Risk of cardiac arrhythmias")
    
    # Analyze ECG
    ecg = latest_vitals['ECG']
    if ecg > 2.0:
        severity = "CRITICAL"
        assessment.append(f"**Severe ECG Abnormality** ({ecg:.2f}): Possible life-threatening arrhythmia.")
        diagnosis.append("Severe Cardiac Arrhythmia")
        risk_factors.append("Risk of sudden cardiac death")
    elif ecg > 1.5:
        if severity == "STABLE":
            severity = "WARNING"
        assessment.append(f"**ECG Abnormality** ({ecg:.2f}): Irregular cardiac rhythm detected.")
        diagnosis.append("Cardiac Arrhythmia")
    
    # Pattern recognition - Sepsis
    if temp > 38.5 and hr > 100 and bp_sys < 100:
        if "Sepsis" not in " ".join(diagnosis):
            diagnosis.insert(0, "**SEPSIS PATTERN DETECTED**")
            assessment.insert(0, "**⚠️ SEPSIS TRIAD**: Fever + Tachycardia + Hypotension suggests systemic infection with hemodynamic compromise.")
            severity = "CRITICAL"
            risk_factors.insert(0, "Progression to septic shock and multi-organ failure")
    
    # Pattern recognition - Respiratory failure
    if spo2 < 92 and hr > 100 and spo2_trend < -0.2:
        if "Respiratory" not in " ".join(diagnosis):
            diagnosis.insert(0, "**RESPIRATORY FAILURE PATTERN**")
            assessment.insert(0, "**⚠️ RESPIRATORY COMPROMISE**: Declining SpO2 with compensatory tachycardia indicates progressive respiratory failure.")
    
    # Construct summary
    if not assessment:
        assessment.append("All vital signs are within normal parameters. Patient appears stable.")
    
    summary = {
        "assessment": "\n\n".join(assessment),
        "severity": severity,
        "diagnosis": diagnosis[0] if diagnosis else "Stable - No Acute Conditions",
        "all_diagnoses": diagnosis,
        "risk_factors": risk_factors,
        "trends": {
            "hr_trend": hr_trend,
            "spo2_trend": spo2_trend,
            "temp_trend": temp_trend,
            "bp_trend": bp_trend
        }
    }
    
    return summary

# Enhanced nursing actions
def get_nursing_actions(patient_data, clinical_summary):
    """Generate evidence-based nursing interventions"""
    latest_vitals = patient_data.iloc[-1]
    severity = clinical_summary['severity']
    
    actions = {
        "immediate": [],
        "monitoring": [],
        "notifications": [],
        "medications": [],
        "equipment": []
    }
    
    # Heart rate actions
    hr = latest_vitals['heart_rate_bpm']
    if hr > 150:
        actions["immediate"].append("⚠️ **RAPID RESPONSE**: Assess patient responsiveness immediately")
        actions["immediate"].append("🔌 **ECG MONITORING**: Obtain 12-lead ECG stat")
        actions["equipment"].append("Prepare defibrillator at bedside")
        actions["equipment"].append("Prepare crash cart")
        actions["notifications"].append("🚨 **CALL CODE TEAM** - Possible V-Tach")
        actions["medications"].append("Prepare Amiodarone 150mg IV for rhythm control")
        actions["medications"].append("Have Adenosine 6mg ready if SVT suspected")
    elif hr > 120:
        actions["immediate"].append("📊 Obtain vital signs every 5 minutes")
        actions["notifications"].append("📞 Notify attending physician of tachycardia")
        actions["monitoring"].append("Continuous cardiac monitoring required")
    elif hr < 40:
        actions["immediate"].append("🚨 **PREPARE FOR CODE**: Check patient responsiveness")
        actions["equipment"].append("Prepare transcutaneous pacing")
        actions["medications"].append("Prepare Atropine 0.5mg IV")
        actions["notifications"].append("🚨 CALL CODE TEAM - Severe bradycardia")
    
    # SpO2 actions
    spo2 = latest_vitals['spo2_percent']
    if spo2 < 85:
        actions["immediate"].append("🫁 **OXYGEN THERAPY**: Place on 100% O2 via non-rebreather mask (15L/min)")
        actions["immediate"].append("📊 Obtain arterial blood gas (ABG) stat")
        actions["equipment"].append("Prepare intubation equipment")
        actions["notifications"].append("📞 CALL RESPIRATORY THERAPIST STAT")
        actions["notifications"].append("📞 Notify physician - may need intubation")
        actions["monitoring"].append("Continuous pulse oximetry")
    elif spo2 < 90:
        actions["immediate"].append("💨 Increase oxygen: Target SpO2 >92%")
        actions["immediate"].append("Position patient in high-Fowler's position")
        actions["monitoring"].append("Monitor SpO2 continuously, ABG if worsening")
        actions["notifications"].append("📞 Notify physician of hypoxemia")
    
    # Blood pressure actions
    bp_sys = latest_vitals['bp_systolic_mmHg']
    if bp_sys < 80:
        actions["immediate"].append("💉 **FLUID RESUSCITATION**: Start rapid IV fluid bolus - 500mL NS over 15 min")
        actions["immediate"].append("🩸 Establish 2nd large-bore IV (16-18 gauge)")
        actions["immediate"].append("📊 Check serum lactate stat")
        actions["equipment"].append("Prepare vasopressor infusion (Norepinephrine)")
        actions["medications"].append("Prepare Norepinephrine drip (start at 2-4 mcg/min)")
        actions["notifications"].append("🚨 NOTIFY PHYSICIAN IMMEDIATELY - Hypotensive shock")
        actions["monitoring"].append("Blood pressure every 2-3 minutes")
        actions["monitoring"].append("Consider arterial line placement")
    elif bp_sys < 90:
        actions["immediate"].append("💧 Start IV fluid bolus - 250mL NS over 15 min")
        actions["monitoring"].append("Blood pressure every 5 minutes")
        actions["notifications"].append("📞 Notify physician of hypotension")
    elif bp_sys > 180:
        actions["immediate"].append("📊 Assess for end-organ damage (headache, vision, chest pain)")
        actions["medications"].append("Prepare antihypertensive (Labetalol or Hydralazine)")
        actions["notifications"].append("📞 Notify physician - Hypertensive emergency")
    
    # Temperature actions
    temp = latest_vitals['temperature_c']
    if temp > 39.5:
        actions["immediate"].append("🩸 **SEPSIS PROTOCOL**: Draw blood cultures (2 sets from different sites)")
        actions["immediate"].append("❄️ Begin active cooling measures (cooling blanket, ice packs)")
        actions["immediate"].append("💉 Start IV fluid resuscitation")
        actions["medications"].append("Administer Acetaminophen 1000mg PO/IV for fever")
        actions["medications"].append("⚠️ **ANTIBIOTICS WITHIN 1 HOUR**: Prepare broad-spectrum antibiotics per protocol")
        actions["medications"].append("Consider: Vancomycin 15mg/kg IV + Piperacillin-Tazobactam 4.5g IV")
        actions["notifications"].append("📞 NOTIFY PHYSICIAN STAT - Severe sepsis suspected")
        actions["monitoring"].append("Temperature every 30 minutes")
    elif temp > 38.5:
        actions["immediate"].append("Give Acetaminophen 650mg PO for fever")
        actions["monitoring"].append("Monitor temperature every hour")
        actions["notifications"].append("📞 Inform physician of fever")
    
    # ECG actions
    ecg = latest_vitals['ECG']
    if ecg > 2.0:
        actions["immediate"].append("📊 **STAT 12-LEAD ECG**: Obtain immediately")
        actions["equipment"].append("Prepare defibrillator - check pads placement")
        actions["monitoring"].append("Continuous telemetry monitoring")
        actions["notifications"].append("🚨 CALL CARDIOLOGY - Severe arrhythmia")
    elif ecg > 1.5:
        actions["immediate"].append("Obtain 12-lead ECG")
        actions["monitoring"].append("Place on continuous cardiac monitoring")
    
    # Sepsis bundle
    if "SEPSIS" in clinical_summary.get('diagnosis', '').upper():
        actions["immediate"].insert(0, "🚨 **ACTIVATE SEPSIS PROTOCOL**")
        actions["immediate"].insert(1, "⏱️ **SEP-1 BUNDLE**: Complete within 3 hours:")
        actions["immediate"].append("   1️⃣ Measure lactate level")
        actions["immediate"].append("   2️⃣ Obtain blood cultures before antibiotics")
        actions["immediate"].append("   3️⃣ Administer broad-spectrum antibiotics")
        actions["immediate"].append("   4️⃣ Begin rapid fluid resuscitation (30mL/kg crystalloid)")
    
    # Respiratory failure bundle
    if "RESPIRATORY FAILURE" in clinical_summary.get('diagnosis', '').upper():
        actions["immediate"].insert(0, "🫁 **RESPIRATORY FAILURE PROTOCOL**")
        actions["immediate"].append("Consider: Non-invasive ventilation (BiPAP/CPAP)")
        actions["equipment"].insert(0, "Prepare intubation tray at bedside")
        actions["notifications"].insert(0, "📞 NOTIFY RESPIRATORY THERAPIST STAT")
    
    return actions

# Critical alerts (immediate response)
def get_critical_alerts(vitals):
    """Immediate rule-based alerts for critical conditions"""
    alerts = []
    severity = "STABLE"
    
    if vitals['heart_rate_bpm'] < 40:
        alerts.append("🚨 SEVERE BRADYCARDIA - Risk of cardiac arrest")
        severity = "CRITICAL"
    elif vitals['heart_rate_bpm'] > 150:
        alerts.append("🚨 SEVERE TACHYCARDIA - Possible V-Tach")
        severity = "CRITICAL"
    
    if vitals['spo2_percent'] < 85:
        alerts.append("🚨 SEVERE HYPOXEMIA - Immediate oxygen required")
        severity = "CRITICAL"
    elif vitals['spo2_percent'] < 90:
        alerts.append("⚠️ HYPOXEMIA - Oxygen saturation low")
        if severity != "CRITICAL":
            severity = "WARNING"
    
    if vitals['bp_systolic_mmHg'] < 80:
        alerts.append("🚨 SEVERE HYPOTENSION - Risk of shock")
        severity = "CRITICAL"
    elif vitals['bp_systolic_mmHg'] < 90:
        alerts.append("⚠️ HYPOTENSION - Blood pressure low")
        if severity != "CRITICAL":
            severity = "WARNING"
    
    if vitals['bp_systolic_mmHg'] > 180:
        alerts.append("🚨 HYPERTENSIVE CRISIS")
        severity = "CRITICAL"
    
    if vitals['temperature_c'] > 39.5:
        alerts.append("🚨 SEVERE HYPERTHERMIA")
        if severity == "STABLE":
            severity = "CRITICAL"
    elif vitals['temperature_c'] > 38.5:
        alerts.append("⚠️ FEVER - Monitor closely")
        if severity == "STABLE":
            severity = "WARNING"
    
    if vitals['temperature_c'] < 35:
        alerts.append("🚨 HYPOTHERMIA")
        severity = "CRITICAL"
    
    if vitals['ECG'] > 2.0:
        alerts.append("🚨 ABNORMAL ECG - Possible arrhythmia")
        severity = "CRITICAL"
    elif vitals['ECG'] > 1.5:
        alerts.append("⚠️ ECG ABNORMALITY - Monitor rhythm")
        if severity == "STABLE":
            severity = "WARNING"
    
    if not alerts:
        alerts.append("✅ All vital signs within normal parameters")
    
    return alerts, severity

# Visualization functions
def create_vitals_chart(df):
    """Create comprehensive vitals monitoring chart"""
    fig = make_subplots(
        rows=4, cols=2,
        subplot_titles=('Heart Rate (bpm)', 'SpO2 (%)', 
                       'Blood Pressure (mmHg)', 'Temperature (°C)',
                       'ECG Reading', 'Heart Rate Variability'),
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # Heart Rate
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['heart_rate_bpm'], 
                  name='Heart Rate', line=dict(color='#ef4444', width=2),
                  fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.1)'),
        row=1, col=1
    )
    fig.add_hline(y=60, line_dash="dash", line_color="green", opacity=0.5, row=1, col=1)
    fig.add_hline(y=100, line_dash="dash", line_color="green", opacity=0.5, row=1, col=1)
    
    # SpO2
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['spo2_percent'], 
                  name='SpO2', line=dict(color='#3b82f6', width=2),
                  fill='tozeroy', fillcolor='rgba(59, 130, 246, 0.1)'),
        row=1, col=2
    )
    fig.add_hline(y=95, line_dash="dash", line_color="green", opacity=0.5, row=1, col=2)
    fig.add_hline(y=90, line_dash="dash", line_color="orange", opacity=0.5, row=1, col=2)
    
    # Blood Pressure
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['bp_systolic_mmHg'], 
                  name='Systolic', line=dict(color='#8b5cf6', width=2)),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['bp_diastolic_mmHg'], 
                  name='Diastolic', line=dict(color='#a78bfa', width=2)),
        row=2, col=1
    )
    fig.add_hline(y=120, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
    fig.add_hline(y=80, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
    
    # Temperature
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['temperature_c'], 
                  name='Temperature', line=dict(color='#f59e0b', width=2),
                  fill='tozeroy', fillcolor='rgba(245, 158, 11, 0.1)'),
        row=2, col=2
    )
    fig.add_hline(y=37, line_dash="dash", line_color="green", opacity=0.5, row=2, col=2)
    fig.add_hline(y=38.5, line_dash="dash", line_color="orange", opacity=0.5, row=2, col=2)
    
    # ECG
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['ECG'], 
                  name='ECG', line=dict(color='#10b981', width=2)),
        row=3, col=1
    )
    fig.add_hline(y=1.0, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
    
    # Heart Rate Variability
    hr_rolling_std = df['heart_rate_bpm'].rolling(window=5, min_periods=1).std()
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=hr_rolling_std, 
                  name='HR Variability', line=dict(color='#ec4899', width=2)),
        row=3, col=2
    )
    
    fig.update_layout(
        height=1000,
        showlegend=True,
        title_text="Patient Vital Signs - Real-time Monitoring",
        title_font_size=20,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Time", row=3, col=1)
    fig.update_xaxes(title_text="Time", row=3, col=2)
    
    return fig

# Main App
def main():
    # Header
    st.markdown('<div class="main-header"><h1>🏥 AI-Based ICU Patient Monitor</h1><p>Real-time Critical Care Decision Support System</p></div>', 
                unsafe_allow_html=True)
    
    st.info("ℹ️ **Note**: This version uses enhanced rule-based clinical logic. For AI-powered analysis, use the version with Anthropic API.")
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Patient Data")
        uploaded_file = st.file_uploader("Upload Patient CSV File", type=['csv'])
        
        st.markdown("---")
        st.header("⚙️ System Settings")
        show_trends = st.checkbox("Show historical trends", value=True)
        show_detailed_actions = st.checkbox("Show detailed nursing actions", value=True)
        
        st.markdown("---")
        st.info("""
        **Normal Ranges:**
        - Heart Rate: 60-100 bpm
        - SpO2: >95%
        - BP: 120/80 mmHg
        - Temp: 36.5-37.5°C
        - ECG: <1.5
        """)
    
    # Main content
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            required_cols = ['patient_id', 'timestamp', 'ECG', 'heart_rate_bpm', 
                           'temperature_c', 'bp_systolic_mmHg', 'bp_diastolic_mmHg', 'spo2_percent']
            
            if not all(col in df.columns for col in required_cols):
                st.error("❌ Invalid CSV format. Missing required columns.")
                return
            
            patient_id = df['patient_id'].iloc[0]
            st.subheader(f"👤 Patient ID: {patient_id}")
            
            latest_vitals = df.iloc[-1]
            
            # Critical alerts
            alerts, severity = get_critical_alerts(latest_vitals)
            
            # Display alert banner
            if severity == "CRITICAL":
                st.markdown(f'<div class="critical-alert">🚨 CRITICAL ALERT - IMMEDIATE ATTENTION REQUIRED 🚨</div>', 
                          unsafe_allow_html=True)
            elif severity == "WARNING":
                st.markdown(f'<div class="warning-alert">⚠️ WARNING - Close Monitoring Required</div>', 
                          unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="stable-status">✅ Patient Stable - Continue Routine Monitoring</div>', 
                          unsafe_allow_html=True)
            
            # Display current vitals
            st.subheader("📊 Current Vital Signs")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                hr_color = "🔴" if latest_vitals['heart_rate_bpm'] > 120 or latest_vitals['heart_rate_bpm'] < 50 else "🟢"
                st.metric("Heart Rate", f"{latest_vitals['heart_rate_bpm']:.0f} bpm", 
                         delta=f"{latest_vitals['heart_rate_bpm'] - 75:.0f}")
                st.caption(f"{hr_color} Normal: 60-100 bpm")
            
            with col2:
                spo2_color = "🔴" if latest_vitals['spo2_percent'] < 90 else "🟢"
                st.metric("SpO2", f"{latest_vitals['spo2_percent']:.1f}%",
                         delta=f"{latest_vitals['spo2_percent'] - 95:.1f}")
                st.caption(f"{spo2_color} Normal: >95%")
            
            with col3:
                bp_color = "🔴" if latest_vitals['bp_systolic_mmHg'] < 90 or latest_vitals['bp_systolic_mmHg'] > 140 else "🟢"
                st.metric("Blood Pressure", 
                         f"{latest_vitals['bp_systolic_mmHg']:.0f}/{latest_vitals['bp_diastolic_mmHg']:.0f}",
                         delta=f"{latest_vitals['bp_systolic_mmHg'] - 120:.0f}")
                st.caption(f"{bp_color} Normal: 120/80 mmHg")
            
            with col4:
                temp_color = "🔴" if latest_vitals['temperature_c'] > 38.5 or latest_vitals['temperature_c'] < 35 else "🟢"
                st.metric("Temperature", f"{latest_vitals['temperature_c']:.1f}°C",
                         delta=f"{latest_vitals['temperature_c'] - 37:.1f}")
                st.caption(f"{temp_color} Normal: 36.5-37.5°C")
            
            with col5:
                ecg_color = "🔴" if latest_vitals['ECG'] > 1.5 else "🟢"
                st.metric("ECG", f"{latest_vitals['ECG']:.2f}",
                         delta=f"{latest_vitals['ECG'] - 1.0:.2f}")
                st.caption(f"{ecg_color} Normal: <1.5")
            
            # Alerts
            st.subheader("🚨 Clinical Alerts")
            for alert in alerts:
                if "🚨" in alert:
                    st.error(alert)
                elif "⚠️" in alert:
                    st.warning(alert)
                else:
                    st.success(alert)
            
            # Clinical Assessment
            st.subheader("🏥 Clinical Assessment")
            clinical_summary = analyze_patient_vitals(df)
            
            st.markdown(f"""
            <div class="assessment-box">
            <h4>Severity: {clinical_summary['severity']}</h4>
            <h4>Primary Diagnosis: {clinical_summary['diagnosis']}</h4>
            <hr>
            {clinical_summary['assessment']}
            </div>
            """, unsafe_allow_html=True)
            
            if clinical_summary['risk_factors']:
                st.warning("**⚠️ Risk Factors:**\n\n" + "\n\n".join(f"• {rf}" for rf in clinical_summary['risk_factors']))
            
            # Nursing Actions
            if severity != "STABLE" and show_detailed_actions:
                st.subheader("🎯 Evidence-Based Nursing Interventions")
                actions = get_nursing_actions(df, clinical_summary)
                
                if actions["immediate"]:
                    st.markdown("### 🚨 IMMEDIATE INTERVENTIONS (Within 1 Minute)")
                    for action in actions["immediate"]:
                        st.markdown(f"- {action}")
                
                if actions["monitoring"]:
                    st.markdown("### 📊 MONITORING REQUIREMENTS")
                    for action in actions["monitoring"]:
                        st.markdown(f"- {action}")
                
                if actions["notifications"]:
                    st.markdown("### 📞 NOTIFICATION PROTOCOL")
                    for action in actions["notifications"]:
                        st.markdown(f"- {action}")
                
                if actions["medications"]:
                    st.markdown("### 💊 MEDICATION CONSIDERATIONS")
                    for action in actions["medications"]:
                        st.markdown(f"- {action}")
                
                if actions["equipment"]:
                    st.markdown("### 🔧 EQUIPMENT PREPARATION")
                    for action in actions["equipment"]:
                        st.markdown(f"- {action}")
            
            # Visualization
            if show_trends:
                st.subheader("📈 Vital Signs Trends")
                fig = create_vitals_chart(df)
                st.plotly_chart(fig, use_container_width=True)
            
            # Data table
            with st.expander("📋 View Raw Data"):
                st.dataframe(df.tail(20), use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error loading patient data: {str(e)}")
            st.exception(e)
    
    else:
        st.info("👈 Please upload a patient CSV file to begin monitoring")
        
        st.markdown("""
        ### 📋 Required CSV Format
        
        Your patient data file should contain the following columns:
        - `patient_id`: Unique patient identifier
        - `timestamp`: Date/time of reading
        - `ECG`: ECG reading value
        - `heart_rate_bpm`: Heart rate in beats per minute
        - `temperature_c`: Body temperature in Celsius
        - `bp_systolic_mmHg`: Systolic blood pressure
        - `bp_diastolic_mmHg`: Diastolic blood pressure
        - `spo2_percent`: Blood oxygen saturation percentage
        """)

if __name__ == "__main__":
    main()
