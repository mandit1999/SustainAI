import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df, column, contamination=0.02):

    result = df.copy()

    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    model.fit(result[[column]])

    prediction = model.predict(result[[column]])

    result[f"{column}_anomaly"] = prediction

    result[f"{column}_status"] = result[
        f"{column}_anomaly"
    ].apply(
        lambda x: "Anomaly" if x == -1 else "Normal"
    )

    return result