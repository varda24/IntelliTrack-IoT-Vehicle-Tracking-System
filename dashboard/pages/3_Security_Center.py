import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Security Center",
    layout="wide"
)

st_autorefresh(
    interval=3000,
    key="security_page"
)

BASE_DIR = Path(__file__).resolve().parents[2]

db_path = BASE_DIR / "database" / "vehicle_tracking.db"

conn = sqlite3.connect(db_path)

df = pd.read_sql(
    "SELECT * FROM vehicle_logs",
    conn
)

st.title("🛡️ Security Operations Center")

if len(df) == 0:
    st.warning("No security data available")
    st.stop()

latest = (
    df.sort_values("id")
      .groupby("vehicle_id")
      .tail(1)
)

critical_alerts = len(
    latest[
        latest["status"] == "THEFT_ALERT"
    ]
)

warning_alerts = len(
    latest[
        latest["status"] == "OVERSPEED"
    ]
)

safe_vehicles = len(
    latest[
        latest["status"] == "SAFE"
    ]
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "🟢 Safe Vehicles",
        safe_vehicles
    )

with c2:
    st.metric(
        "⚠ Warning Alerts",
        warning_alerts
    )

with c3:
    st.metric(
        "🚨 Critical Alerts",
        critical_alerts
    )

st.divider()

for _, row in latest.iterrows():

    with st.container():

        col1, col2 = st.columns([2, 1])

        with col1:

            st.subheader(
                f"🚚 {row['vehicle_id']}"
            )

            st.write(
                f"Driver: {row['driver_id']}"
            )

            st.write(
                f"Speed: {row['speed']} km/h"
            )

            st.write(
                f"Ignition: {row['ignition']}"
            )

            st.write(
                f"Latitude: {row['latitude']}"
            )

            st.write(
                f"Longitude: {row['longitude']}"
            )

            maps_url = (
                f"https://maps.google.com/?q="
                f"{row['latitude']},"
                f"{row['longitude']}"
            )

            st.link_button(
                "📍 Open In Google Maps",
                maps_url
            )

        with col2:

            if row["status"] == "SAFE":

                st.success(
                    "SAFE"
                )

                reason = "Normal Fleet Operation"

                risk = 20

            elif row["status"] == "OVERSPEED":

                st.warning(
                    "OVERSPEED"
                )

                reason = "Vehicle Exceeding Speed Limit"

                risk = 70

            else:

                st.error(
                    "THEFT ALERT"
                )

                reason = "Unauthorized Vehicle Activity"

                risk = 95

            st.write(
                f"Reason: {reason}"
            )

            st.progress(
                risk / 100
            )

            st.metric(
                "Risk Score",
                f"{risk}%"
            )

        st.divider()