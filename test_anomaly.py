import pandas as pd

from src.anomaly_detection import detect_anomalies


# Load data
df = pd.read_csv("data/facility_data.csv")


metrics = [
    "electricity_kwh",
    "water_liters",
    "waste_kg",
    "aqi"
]


print("======================================")
print("SUSTAINAI ANOMALY DETECTION")
print("======================================")


for metric in metrics:

    result = detect_anomalies(
        df,
        metric
    )

    anomalies = result[
        result[f"{metric}_status"] == "Anomaly"
    ]

    print(
        f"\n{metric}: "
        f"{len(anomalies)} anomalies detected"
    )