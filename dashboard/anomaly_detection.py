from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    model = IsolationForest(
        contamination=0.2,
        random_state=42
    )

    features = df[
        [
            "latitude",
            "longitude",
            "speed"
        ]
    ]

    df["anomaly"] = model.fit_predict(
        features
    )

    return df

