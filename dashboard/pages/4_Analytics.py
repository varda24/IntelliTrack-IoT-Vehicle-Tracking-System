import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import pandas as pd
import plotly.express as px

from pathlib import Path

st.set_page_config(
    page_title="Fleet Analytics",
    layout="wide"
)

st_autorefresh(
    interval=3000,
    key="analytics_page"
)

BASE_DIR = Path(__file__).resolve().parents[2]

db_path = BASE_DIR / "database" / "vehicle_tracking.db"

conn = sqlite3.connect(db_path)

df = pd.read_sql(
    "SELECT * FROM vehicle_logs",
    conn
)

st.title("📈 Fleet Intelligence Dashboard")

if len(df) == 0:
    st.warning("No analytics data available")
    st.stop()

latest = (
    df.sort_values("id")
      .groupby("vehicle_id")
      .tail(1)
)

avg_speed = round(
    latest["speed"].mean(),
    1
)

max_speed = latest["speed"].max()

alerts = len(
    latest[
        latest["status"] != "SAFE"
    ]
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Average Speed",
        f"{avg_speed} km/h"
    )

with c2:
    st.metric(
        "Maximum Speed",
        f"{max_speed} km/h"
    )

with c3:
    st.metric(
        "Active Alerts",
        alerts
    )

st.divider()

left, right = st.columns(2)

with left:

    fig1 = px.bar(
        latest,
        x="vehicle_id",
        y="speed",
        color="status",
        title="Vehicle Speed Comparison"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    status_counts = (
        latest["status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    fig2 = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.5,
        title="Fleet Status Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

st.subheader("Vehicle Speed Trend")

fig3 = px.line(
    df,
    x="timestamp",
    y="speed",
    color="vehicle_id",
    title="Speed Trend Over Time"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

st.subheader("Latest Fleet Analytics")

analytics_df = latest[
    [
        "vehicle_id",
        "driver_id",
        "speed",
        "status",
        "timestamp"
    ]
]

st.dataframe(
    analytics_df,
    use_container_width=True
)
