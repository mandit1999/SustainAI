import pandas as pd

from src.forecasting import forecast_metric


# Load dataset
df = pd.read_csv(
    "data/facility_data.csv"
)


# Convert date
df["date"] = pd.to_datetime(
    df["date"]
)


# Select one facility
facility = df["facility_name"].iloc[0]

facility_data = df[
    df["facility_name"] == facility
].copy()


# Run electricity forecast
model, forecast = forecast_metric(
    facility_data,
    "date",
    "electricity_kwh",
    periods=30
)


# Display forecast
print("\nFacility:")
print(facility)

print("\nLast 10 Forecast Values:")

print(
    forecast[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].tail(10)
)


print("\nForecast completed successfully!")