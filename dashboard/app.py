import streamlit as st

st.set_page_config(
    page_title="IntelliTrack",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 IntelliTrack")

st.subheader(
    "IoT Vehicle Tracking & Theft Prevention System"
)

st.markdown("""
Real-Time Vehicle Monitoring • Live GPS Tracking • Theft Detection • Fleet Analytics
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
### 🚛 Fleet Monitoring

Monitor all connected vehicles in real time.

Track:
- Vehicle Status
- Driver Information
- Speed
- Location
""")

with col2:
    st.success("""
### 📍 Live Tracking

View vehicle movement on an interactive map.

Features:
- Route History
- Vehicle Position
- Live Updates
- Trip Monitoring
""")

with col3:
    st.warning("""
### 🛡 Security Center

Monitor security events.

Alerts:
- Overspeed
- Theft Alert
- Unauthorized Movement
- Risk Assessment
""")

st.divider()

st.markdown("""
## 📊 System Modules

### Fleet Overview
View fleet health, active vehicles and operational metrics.

### Live Tracking
Track all vehicles on a live map with route visualization.

### Security Center
Monitor theft alerts, overspeed events and vehicle risks.

### Analytics
Analyze fleet performance, speed trends and alert distribution.

---

### 🔧 Technology Stack

- ESP32 (Wokwi Simulation)
- Python
- SQLite
- Streamlit
- Folium Maps
- Plotly Analytics

---

### 🚀 Project Workflow

ESP32 Fleet Simulator
↓
Telemetry Generation
↓
SQLite Database
↓
Streamlit Dashboard
↓
Fleet Monitoring & Security Analytics
""")

st.success("System Status: ONLINE")