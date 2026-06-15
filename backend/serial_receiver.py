from database import initialize_database
from database import get_connection

import random
import time

initialize_database()

vehicles = [

    {
        "vehicle": "TRUCK_101",
        "driver": "DRIVER_01",
        "lat": 19.9975,
        "lon": 73.7898,
        "base_lat": 19.9975,
        "base_lon": 73.7898,
        "route": "Warehouse → City Center"
    },

    {
        "vehicle": "TRUCK_102",
        "driver": "DRIVER_02",
        "lat": 19.9990,
        "lon": 73.7910,
        "base_lat": 19.9990,
        "base_lon": 73.7910,
        "route": "Warehouse → Airport"
    },

    {
        "vehicle": "BUS_201",
        "driver": "DRIVER_03",
        "lat": 20.0010,
        "lon": 73.7930,
        "base_lat": 20.0010,
        "base_lon": 73.7930,
        "route": "School Route"
    },

    {
        "vehicle": "VAN_301",
        "driver": "DRIVER_04",
        "lat": 20.0020,
        "lon": 73.7940,
        "base_lat": 20.0020,
        "base_lon": 73.7940,
        "route": "Delivery Route"
    }

]

conn = get_connection()
cursor = conn.cursor()

print("Live Fleet Simulator Started")

while True:

    for v in vehicles:

        # Move around home location
        v["lat"] = v["base_lat"] + random.uniform(-0.002, 0.002)
        v["lon"] = v["base_lon"] + random.uniform(-0.002, 0.002)

        speed = random.randint(20, 100)

        ignition = "ON"

        status = "SAFE"

        if speed > 80:
            status = "OVERSPEED"

        # Rare theft event
        if random.randint(1, 200) == 150:
            status = "THEFT_ALERT"

        cursor.execute(
            """
            INSERT INTO vehicle_logs(
                vehicle_id,
                driver_id,
                latitude,
                longitude,
                speed,
                ignition,
                status
            )
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                v["vehicle"],
                v["driver"],
                round(v["lat"], 6),
                round(v["lon"], 6),
                speed,
                ignition,
                status
            )
        )

        conn.commit()

        print(
            f"{v['vehicle']} | "
            f"{round(v['lat'],6)} | "
            f"{round(v['lon'],6)} | "
            f"{speed} km/h | "
            f"{status}"
        )

    time.sleep(3)