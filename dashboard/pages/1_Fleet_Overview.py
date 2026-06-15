import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import pandas as pd
from pathlib import Path
import plotly.express as px

st.set_page_config(
    page_title="Fleet Overview",
    layout="wide"
)

st_autorefresh(
    interval=3000,
    key="fleet_page"
)

BASE_DIR = Path(__file__).resolve().parents[2]

db_path = BASE_DIR / "database" / "vehicle_tracking.db"

conn = sqlite3.connect(db_path)

df = pd.read_sql("""
SELECT *
FROM vehicle_logs
ORDER BY id DESC
""", conn)

st.title("🚚 Fleet Command Center")

if len(df) == 0:
    st.warning("No fleet data available")
    st.stop()

latest = (
    df.sort_values("id")
      .groupby("vehicle_id")
      .tail(1)
)

online = len(latest)

avg_speed = round(
    latest["speed"].mean(),
    1
)

active_alerts = len(
    latest[
        latest["status"] != "SAFE"
    ]
)

overspeed = len(
    latest[
        latest["status"] == "OVERSPEED"
    ]
)

theft = len(
    latest[
        latest["status"] == "THEFT_ALERT"
    ]
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "🚚 Vehicles",
        online
    )

with col2:
    st.metric(
        "⚡ Avg Speed",
        f"{avg_speed} km/h"
    )

with col3:
    st.metric(
        "🚨 Alerts",
        active_alerts
    )
    fleet_health = max(
    0,
    100 - (active_alerts * 20)
    )

    st.metric(
    "💚 Fleet Health",
    f"{fleet_health}%"
    )

with col4:
    st.metric(
        "⚠ Overspeed",
        overspeed
    )

with col5:
    st.metric(
        "🔴 Theft",
        theft
    )

st.divider()

left, right = st.columns([2, 1])

with left:

    st.subheader("Latest Vehicle Status")

    display_df = latest[
        [
            "vehicle_id",
            "driver_id",
            "speed",
            "status",
            "timestamp"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True
    )

with right:

    st.subheader("Fleet Status")

    status_counts = (
        latest["status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("Recent Activity")

recent = df.head(20)

st.dataframe(
    recent[
        [
            "vehicle_id",
            "driver_id",
            "speed",
            "status",
            "timestamp"
        ]
    ],
    use_container_width=True
)