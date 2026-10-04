import pandas as pd
from prophet import Prophet


def forecast_metric(df, date_column, value_column, periods=30):

    # Prepare data for Prophet
    forecast_data = df[[date_column, value_column]].copy()

    forecast_data = forecast_data.rename(
        columns={
            date_column: "ds",
            value_column: "y"
        }
    )

    # Make sure date is datetime
    forecast_data["ds"] = pd.to_datetime(
        forecast_data["ds"]
    )

    # Remove missing values
    forecast_data = forecast_data.dropna()

    # Aggregate data by date
    forecast_data = (
        forecast_data
        .groupby("ds", as_index=False)["y"]
        .mean()
    )

    # Create Prophet model
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    # Train model
    model.fit(forecast_data)

    # Create future dates
    future = model.make_future_dataframe(
        periods=periods
    )

    # Generate forecast
    forecast = model.predict(future)

    return model, forecast