import streamlit as st

import sqlite3
import pandas as pd
import folium

from pathlib import Path
from streamlit_folium import st_folium
import sys

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.append(str(BASE_DIR))

from backend.database import initialize_database

initialize_database()

st.set_page_config(
    page_title="Live Tracking",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[2]

db_path = BASE_DIR / "database" / "vehicle_tracking.db"

db_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

conn = sqlite3.connect(
    db_path,
    check_same_thread=False
)

df = pd.read_sql(
    "SELECT * FROM vehicle_logs",
    conn
)

st.title("🛰️ Live Vehicle Tracking")
if st.button("🔄 Refresh Vehicle Locations"):
    st.rerun()

if len(df) == 0:
    st.warning("No tracking data available")
    st.stop()

latest = (
    df.sort_values("id")
      .groupby("vehicle_id")
      .tail(1)
)

center_lat = latest["latitude"].mean()
center_lon = latest["longitude"].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13
)

for _, row in latest.iterrows():

    vehicle_history = df[
        df["vehicle_id"] == row["vehicle_id"]
    ]

    points = vehicle_history.tail(15)[
        ["latitude", "longitude"]
    ].values.tolist()

    vehicle_colors = {
    "TRUCK_101": "blue",
    "TRUCK_102": "green",
    "BUS_201": "purple",
    "VAN_301": "orange"
    }

    route_color = vehicle_colors.get(
        row["vehicle_id"],
        "gray"
    )
    if len(points) > 1:

        folium.PolyLine(
            points,
            color=route_color,
            weight=3,
            opacity=0.7
        ).add_to(m)

    popup_text = f"""
    <b>{row['vehicle_id']}</b><br>
    Driver: {row['driver_id']}<br>
    Speed: {row['speed']} km/h<br>
    Status: {row['status']}<br>
    """

    folium.Marker(
        [row["latitude"], row["longitude"]],
        popup=popup_text,
        tooltip=row["vehicle_id"],
        icon=folium.Icon(
            color=route_color,
            icon="car",
            prefix="fa"
        )
    ).add_to(m)

st_folium(
    m,
    width=1400,
    height=750,
    returned_objects=[]
)

st.divider()

st.subheader("Current Vehicle Positions")

display_df = latest[
    [
        "vehicle_id",
        "driver_id",
        "latitude",
        "longitude",
        "speed",
        "status"
    ]
]

st.dataframe(
    display_df,
    use_container_width=True
)