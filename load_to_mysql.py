import pandas as pd
import mysql.connector

# ---------------------------------------
# LOAD CSV
# ---------------------------------------

df = pd.read_csv("data/facility_data.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"]).dt.date

print("CSV loaded successfully.")
print("Rows:", len(df))


# ---------------------------------------
# CONNECT TO MYSQL
# ---------------------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mandit@123",
    database="sustainai"
)

cursor = connection.cursor()

print("Connected to MySQL successfully.")


# ---------------------------------------
# INSERT DATA
# ---------------------------------------

sql = """
INSERT INTO facility_data (
    date,
    facility_id,
    facility_name,
    facility_type,
    city,
    electricity_kwh,
    water_liters,
    waste_kg,
    aqi,
    pm25,
    temperature_c,
    occupancy_percent,
    visitors,
    equipment_utilization_percent,
    maintenance_incidents,
    safety_incidents
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s
)
"""

data = [
    tuple(row)
    for row in df[
        [
            "date",
            "facility_id",
            "facility_name",
            "facility_type",
            "city",
            "electricity_kwh",
            "water_liters",
            "waste_kg",
            "aqi",
            "pm25",
            "temperature_c",
            "occupancy_percent",
            "visitors",
            "equipment_utilization_percent",
            "maintenance_incidents",
            "safety_incidents"
        ]
    ].values
]

cursor.executemany(sql, data)

connection.commit()

print("Data inserted successfully!")
print("Rows inserted:", cursor.rowcount)


# ---------------------------------------
# CLOSE CONNECTION
# ---------------------------------------

cursor.close()
connection.close()

print("MySQL connection closed.")