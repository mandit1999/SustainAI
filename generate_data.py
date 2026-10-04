import pandas as pd
import numpy as np

# For reproducible results
np.random.seed(42)

# ---------------------------------------
# FACILITY INFORMATION
# ---------------------------------------

facilities = [
    {
        "facility_id": "F001",
        "facility_name": "Government Hospital - Bhubaneswar",
        "facility_type": "Hospital",
        "city": "Bhubaneswar"
    },
    {
        "facility_id": "F002",
        "facility_name": "Government Hospital - Bengaluru",
        "facility_type": "Hospital",
        "city": "Bengaluru"
    },
    {
        "facility_id": "F003",
        "facility_name": "Engineering College - Bhubaneswar",
        "facility_type": "College",
        "city": "Bhubaneswar"
    },
    {
        "facility_id": "F004",
        "facility_name": "Municipal Facility - Delhi",
        "facility_type": "Municipal",
        "city": "Delhi"
    },
    {
        "facility_id": "F005",
        "facility_name": "Industrial Estate - Hyderabad",
        "facility_type": "Industrial",
        "city": "Hyderabad"
    },
    {
        "facility_id": "F006",
        "facility_name": "Corporate Campus - Pune",
        "facility_type": "Corporate Campus",
        "city": "Pune"
    }
]

# ---------------------------------------
# DATE RANGE
# ---------------------------------------

dates = pd.date_range(
    start="2025-10-01",
    end="2026-09-30",
    freq="D"
)

data = []

# ---------------------------------------
# GENERATE DAILY DATA
# ---------------------------------------

for facility in facilities:

    for date in dates:

        # Seasonal variation
        seasonal_factor = 1 + 0.10 * np.sin(
            2 * np.pi * date.dayofyear / 365
        )

        # Occupancy
        occupancy = np.random.normal(70, 10)
        occupancy = np.clip(occupancy, 30, 100)

        # Visitors
        visitors = int(
            occupancy * np.random.uniform(40, 70)
        )

        # Electricity consumption
        electricity = (
            np.random.normal(5000, 500)
            * seasonal_factor
            * (0.8 + occupancy / 200)
        )

        electricity = max(1000, electricity)

        # Water consumption
        water = (
            np.random.normal(45000, 5000)
            * (0.7 + occupancy / 150)
        )

        water = max(10000, water)

        # Waste
        waste = (
            np.random.normal(800, 100)
            * (0.7 + occupancy / 150)
        )

        waste = max(100, waste)

        # Temperature
        temperature = np.random.normal(28, 5)
        temperature = np.clip(temperature, 15, 45)

        # AQI
        aqi = np.random.normal(90, 25)
        aqi = np.clip(aqi, 30, 250)

        # PM2.5
        pm25 = np.random.normal(45, 12)
        pm25 = np.clip(pm25, 10, 150)

        # Equipment utilization
        equipment_utilization = (
            occupancy + np.random.normal(0, 8)
        )

        equipment_utilization = np.clip(
            equipment_utilization,
            20,
            100
        )

        # Maintenance incidents
        maintenance_incidents = np.random.poisson(1)

        # Safety incidents
        safety_incidents = np.random.poisson(0.2)

        # ---------------------------------------
        # ADD RECORD
        # ---------------------------------------

        data.append({
            "date": date,
            "facility_id": facility["facility_id"],
            "facility_name": facility["facility_name"],
            "facility_type": facility["facility_type"],
            "city": facility["city"],
            "electricity_kwh": round(electricity, 2),
            "water_liters": round(water, 2),
            "waste_kg": round(waste, 2),
            "aqi": round(aqi, 2),
            "pm25": round(pm25, 2),
            "temperature_c": round(temperature, 2),
            "occupancy_percent": round(occupancy, 2),
            "visitors": visitors,
            "equipment_utilization_percent": round(
                equipment_utilization, 2
            ),
            "maintenance_incidents": maintenance_incidents,
            "safety_incidents": safety_incidents
        })

# ---------------------------------------
# CREATE DATAFRAME
# ---------------------------------------

df = pd.DataFrame(data)

# ---------------------------------------
# CREATE SOME INTENTIONAL ANOMALIES
# ---------------------------------------

# Electricity spike
df.loc[100, "electricity_kwh"] *= 2

# Water spike
df.loc[500, "water_liters"] *= 2

# Waste spike
df.loc[1000, "waste_kg"] *= 2

# AQI spike
df.loc[1500, "aqi"] *= 2

# ---------------------------------------
# SAVE DATASET
# ---------------------------------------

df.to_csv(
    "data/facility_data.csv",
    index=False
)

print("Dataset created successfully!")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst 5 records:")
print(df.head())