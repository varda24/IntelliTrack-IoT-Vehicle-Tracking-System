def calculate_risk(
    speed,
    status
):

    risk = 0

    if speed > 40:
        risk += 20

    if speed > 60:
        risk += 30

    if status == "GEOFENCE_ALERT":
        risk += 30

    if status == "THEFT_ALERT":
        risk += 50

    return min(
        risk,
        100
    )

