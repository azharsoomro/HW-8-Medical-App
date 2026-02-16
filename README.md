# 🏥 AI-Based ICU Patient Monitor

A production-grade, AI-powered critical care monitoring system that provides real-time patient vital signs analysis, intelligent alerts, and evidence-based nursing interventions.

## 📋 Project Overview

This application monitors ICU patients' vital signs (ECG, Blood Pressure, Temperature, Heart Rate, SpO2) and uses AI to:
- Diagnose patient conditions in real-time
- Detect abnormalities requiring immediate attention
- Suggest evidence-based nursing interventions
- Provide comprehensive clinical decision support

## 🎯 Key Features

### 1. **Real-Time Vital Signs Monitoring**
- Heart Rate (bpm)
- Blood Oxygen Saturation (SpO2 %)
- Blood Pressure (Systolic/Diastolic mmHg)
- Body Temperature (°C)
- ECG Readings

### 2. **AI-Powered Clinical Assessment**
- Claude Sonnet 4 analyzes patient vitals
- Provides detailed medical interpretation
- Identifies severity levels (CRITICAL, WARNING, STABLE)
- Assesses primary diagnosis and risk factors

### 3. **Agentic AI Nursing Interventions**
- Evidence-based action recommendations
- Immediate interventions (within 1 minute)
- Monitoring requirements
- Notification protocols
- Medication considerations
- Equipment preparation guidance

### 4. **Critical Alert System**
- **CRITICAL Alerts** (Red flashing + audio):
  - Heart rate < 40 or > 150 bpm
  - SpO2 < 85%
  - Blood pressure < 80 mmHg systolic
  - Temperature > 39.5°C or < 35°C
  - ECG > 2.0

- **WARNING Alerts** (Orange):
  - Heart rate 50-60 or 100-130 bpm
  - SpO2 90-95%
  - Blood pressure 90-100 mmHg
  - Temperature 38.5-39.5°C
  - ECG 1.5-2.0

### 5. **AI Observability Dashboard**
- Input/Output token usage tracking
- API latency monitoring
- Model version logging
- Request purpose categorization
- Comprehensive telemetry data

### 6. **Interactive Visualizations**
- Multi-panel trend charts (Plotly)
- Real-time vital signs display
- Historical data analysis
- Normal range indicators

## 📁 Project Structure

```
ai-icu-monitor/
├── ai_patient_monitor_complete.py    # Main Streamlit application
├── patient_1_sepsis.csv               # Patient 1: Sepsis deterioration
├── patient_2_vtach.csv                # Patient 2: V-Tach arrhythmia
├── patient_3_respiratory_failure.csv  # Patient 3: Respiratory failure
├── AI_Architecture_Diagram.mermaid    # System architecture diagram
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Anthropic API Key (for AI features)

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd ai-icu-monitor
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

**Option A: Streamlit Secrets** (Recommended)
Create `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

**Option B: Environment Variable**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Step 4: Run Application
```bash
streamlit run ai_patient_monitor_complete.py
```

## 📊 Patient Data Files

### Patient 1: Sepsis-like Deterioration
**File:** `patient_1_sepsis.csv`

**Pattern:** Progressive deterioration over 60 minutes
- Rising fever (37.2°C → 39.7°C)
- Tachycardia (75 → 135 bpm)
- Declining blood pressure (125 → 80 mmHg)
- Mild hypoxemia (97 → 89% SpO2)

**Critical Moments:** Minutes 40-60 (severe sepsis indicators)

### Patient 2: Ventricular Tachycardia Episode
**File:** `patient_2_vtach.csv`

**Pattern:** V-Tach arrhythmia episode
- Normal baseline vitals (minutes 0-24)
- **V-Tach episode (minutes 25-40)**
  - Heart rate 150-180 bpm
  - ECG 2.5-3.5 (severely abnormal)
  - Decreased perfusion
  - Hypoxemia
- Recovery phase (minutes 41-60)

**Critical Moments:** Minutes 25-40 (active arrhythmia)

### Patient 3: Progressive Respiratory Failure
**File:** `patient_3_respiratory_failure.csv`

**Pattern:** Declining oxygen saturation
- Progressive SpO2 decline (96 → 84%)
- Compensatory tachycardia (85 → 120 bpm)
- Rising temperature (37.3 → 38.5°C)
- Blood pressure changes (stress response → decline)

**Critical Moments:** Minutes 45-60 (severe hypoxemia)

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DATA INPUT LAYER                        │
│  Patient CSV → Validation → Pandas DataFrame                │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              REAL-TIME MONITORING LAYER                     │
│  • Extract Latest Vitals                                    │
│  • Analyze Historical Trends                                │
│  • Rule-Based Critical Alert System                         │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  AI ANALYSIS LAYER                          │
│  ┌──────────────────────────────────────────────┐           │
│  │   Anthropic Claude Sonnet 4 API              │           │
│  ├──────────────────────────────────────────────┤           │
│  │  1. Clinical Assessment & Diagnosis          │           │
│  │  2. Agentic Nursing Action Recommendations   │           │
│  └──────────────────────────────────────────────┘           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              AI OBSERVABILITY LAYER                         │
│  • Token Usage (Input/Output)                               │
│  • API Latency Tracking                                     │
│  • Model Version Logging                                    │
│  • Request Purpose Categorization                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              VISUALIZATION LAYER                            │
│  • Current Vitals Metrics                                   │
│  • Multi-Panel Trend Charts (Plotly)                        │
│  • Alert Banners (Critical/Warning/Stable)                  │
│  • Nursing Action Recommendations                           │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Usage Guide

### 1. Upload Patient Data
- Click "Upload Patient CSV File" in the sidebar
- Select one of the provided patient files or your own

### 2. Monitor Vital Signs
- View current vitals in the metrics dashboard
- Check color-coded indicators (🔴 Critical, 🟢 Normal)

### 3. Review Alerts
- Critical alerts trigger red flashing banner + audio
- Warning alerts show orange banner
- Stable status shows green confirmation

### 4. AI Clinical Assessment
- Automatic AI analysis of patient condition
- Detailed medical interpretation
- Severity classification
- Risk factor identification

### 5. Follow Nursing Actions
- AI-generated evidence-based interventions
- Prioritized action steps
- Protocol-based recommendations

### 6. Analyze Trends
- Interactive Plotly charts show 60-minute history
- Normal range indicators on all charts
- Multi-panel view for comprehensive analysis

### 7. View AI Telemetry
- Click "View AI Telemetry" in sidebar
- Monitor token usage and API performance
- Track all AI interactions

## 📈 AI Observability Metrics

The system tracks comprehensive AI telemetry:

| Metric | Description |
|--------|-------------|
| **Total AI Calls** | Number of API requests made |
| **Input Tokens** | Tokens sent to the AI model |
| **Output Tokens** | Tokens generated by AI |
| **Average Latency** | Mean response time in milliseconds |
| **Model Version** | Claude model used (Sonnet 4) |
| **Purpose** | Context of each AI call |

## 🎨 User Interface Components

### Alert Levels
1. **🚨 CRITICAL** - Red flashing banner with audio alert
2. **⚠️ WARNING** - Orange banner, close monitoring required
3. **✅ STABLE** - Green banner, routine monitoring

### Dashboard Panels
- **Vital Signs Metrics** - Current readings with delta indicators
- **Clinical Alerts** - Color-coded alert messages
- **AI Assessment** - Detailed clinical interpretation
- **Nursing Actions** - Evidence-based intervention steps
- **Trend Visualization** - Interactive 6-panel chart
- **Raw Data Table** - Expandable data view
- **Telemetry Dashboard** - AI performance metrics

## 🔐 Security & Privacy

- Patient data processed locally
- No data stored permanently
- API calls encrypted (HTTPS)
- Anthropic API complies with HIPAA requirements
- Session-based data management

## 📚 Medical Context

### Normal Vital Sign Ranges
- **Heart Rate:** 60-100 bpm
- **SpO2:** >95%
- **Blood Pressure:** 120/80 mmHg (systolic/diastolic)
- **Temperature:** 36.5-37.5°C
- **ECG:** <1.5 (normalized scale)

### Critical Thresholds
- **Severe Bradycardia:** <40 bpm
- **Severe Tachycardia:** >150 bpm
- **Severe Hypoxemia:** <85% SpO2
- **Severe Hypotension:** <80 mmHg systolic
- **Severe Hyperthermia:** >39.5°C
- **Hypothermia:** <35°C

## 🛠️ Technical Stack

- **Frontend:** Streamlit
- **Visualization:** Plotly
- **Data Processing:** Pandas, NumPy
- **AI Engine:** Anthropic Claude Sonnet 4
- **Language:** Python 3.8+



## 📄 License

This project is for educational purposes. Not for clinical use without proper medical validation and regulatory approval.

## ⚠️ Disclaimer

**This is a prototype for educational purposes only.**

This application is NOT approved for clinical use. It should not be used for:
- Actual patient care decisions
- Medical diagnosis
- Treatment planning
- Emergency response

Always consult qualified healthcare professionals for medical decisions.

## 🆘 Support

For issues or questions:
1. Check the documentation
2. Review sample patient files
3. Verify API key configuration
4. Check system requirements



**Built with ❤️ for ICU Patient Safety**

*Empowering healthcare professionals with AI-driven clinical decision support*
